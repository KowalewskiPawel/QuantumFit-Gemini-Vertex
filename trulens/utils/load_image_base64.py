import requests
import base64
from llama_index.schema import ImageDocument
from typing import List

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