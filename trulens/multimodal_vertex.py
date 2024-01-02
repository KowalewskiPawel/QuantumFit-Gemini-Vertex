from trulens_eval import TruCustomApp
from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from trulens_eval import Select
from llama_index.llms.vertex import Vertex
from google.oauth2 import service_account
import requests
import base64
from typing import List
from llama_index.llms import ChatMessage
from llama_index.multi_modal_llms.generic_utils import (
    load_image_urls,
)
from llama_index.schema import ImageDocument

image_urls = [
    "https://storage.googleapis.com/generativeai-downloads/data/scene.jpg",
    # Add yours here!
]

image_documents = load_image_urls(image_urls)

def load_image_base64(image_urls: List[ImageDocument]) -> List[str]:
    # load remote image urls into image documents
    image_documents = []
    for i in range(len(image_urls)):
        response = requests.get(image_urls[i].image_url)
        image_content = response.content

        # Convert the image data to base64
        image_base64 = base64.b64encode(image_content)

        # Convert to string and prepend with appropriate format for use in HTML/CSS
        image_base64_str = "data:image/jpeg;base64," + image_base64.decode("utf-8")
        image_object = {"type": "image_url", "image_url": image_base64_str}
        image_documents.append(image_object)
    return image_documents

filename = "../gcp.json"
credentials: service_account.Credentials = (
    service_account.Credentials.from_service_account_file(filename)
)

gemini_pro = Vertex(
    model="gemini-pro-vision",
    project=credentials.project_id,
    credentials=credentials,
)

tru = Tru()
tru.reset_database()


# create a custom class to instrument
class Gemini:
    @instrument
    def complete(self, prompt, image_documents):
        image_documents_base64 = load_image_base64(image_documents)

        history = [
            ChatMessage(
                role="user",
                content=[
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ] + image_documents_base64,
            ),
        ]

        completion = gemini_pro.chat(history).message.content
        return completion


gemini = Gemini()

# create a custom gemini feedback provider
class Gemini_Provider(Provider):
    def city_rating(self, image_url) -> float:
        image_documents = load_image_urls([image_url])

        image_documents_base64 = load_image_base64(image_documents)

        history = [
            ChatMessage(
                role="user",
                content=[
                    {
                        "type": "text",
                        "text": "Is the image of a city? Respond with the float likelihood from 0.0 (not city) to 1.0 (city):",
                    },
                ] + image_documents_base64,
            ),
        ]

        city_score = float(gemini_pro.chat(history).message.content)

        return city_score


gemini_provider = Gemini_Provider()

f_custom_function = Feedback(gemini_provider.city_rating, name="City Likelihood").on(
    Select.Record.calls[0].args.image_documents[0].image_url
)

gemini_provider.city_rating(
    image_url="https://storage.googleapis.com/generativeai-downloads/data/scene.jpg"
)

from trulens_eval import TruCustomApp
tru_gemini = TruCustomApp(gemini, app_id = "gemini", feedbacks = [f_custom_function])

with tru_gemini as recording:
    gemini.complete(
    prompt="Identify the city where this photo was taken.",
    image_documents=image_documents
    )

    tru.run_dashboard(port=8024)