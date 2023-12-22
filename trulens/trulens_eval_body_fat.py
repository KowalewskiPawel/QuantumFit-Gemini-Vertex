from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from trulens_eval import Select

import requests

tru = Tru()
tru.reset_database()

# Custom class to instrument

def gemini_pro_image(prompt, image_url):
    data = {
            "prompt": prompt,
            "photos": [image_url]
        }

        # Adjust the URL accordingly
    url = "http://localhost:8080/api/v1/gemini/image"

        # Make a POST request to the backend
    response = requests.post(url, json=data)

        # Check if the request was successful
    if response.status_code == 200:
            # Assuming your backend returns the completion in JSON format
        completion = response.json()
        return completion['message']
    else:
            # Handle errors here, raise an exception or return an error message
        raise Exception(f"Failed to complete: {response.status_code} - {response.text}")

class Gemini:
    @instrument
    def complete(self, prompt, image_url):
        # Backend expects JSON data
        data = {
            "prompt": prompt,
            "photos": [image_url]
        }

        # Adjust the URL accordingly
        url = "http://localhost:8080/api/v1/gemini/image"

        # Make a POST request to the backend
        response = requests.post(url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            completion = response.json()
            return completion['message']
        else:
            # Handle errors here, raise an exception or return an error message
            raise Exception(f"Failed to complete: {response.status_code} - {response.text}")

gemini = Gemini()

# custom gemini feedback provider
class Gemini_Provider(Provider):
    def body_fat_analysis(self, image_prompt, image_to_analyze) -> float:
        body_fat_result = float(gemini_pro_image(prompt = image_prompt, image_url = image_to_analyze).text),
        return body_fat_result

gemini_provider = Gemini_Provider()

f_custom_function = Feedback(gemini_provider.body_fat_analysis, name = "Body Fat Analysis").on(Select.Record.calls[0].args.image_url)

from trulens_eval import TruCustomApp
tru_gemini = TruCustomApp(gemini, app_id = "gemini", feedbacks = [f_custom_function])

with tru_gemini as recording:
    gemini.complete(
    prompt="What is the body fat percentage of this person? Please express the result as a percentage. The output should be a number between 0 and 100.",
    image_url=""
    )