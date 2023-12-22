from trulens_eval import TruCustomApp
from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from trulens_eval import Select

import requests

tru = Tru()
tru.reset_database()

# create a custom class to instrument

def gemini_pro(prompt):
    data = {
            "prompt": prompt,
        }

        # Adjust the URL accordingly
    url = "http://localhost:8080/api/v1/gemini/text"

        # Make a POST request to your backend
    response = requests.post(url, json=data)

        # Check if the request was successful
    if response.status_code == 200:
            # Assuming your backend returns the completion in JSON format
        completion = response.json()
        return completion
    else:
            # Handle errors here, raise an exception or return an error message
        raise Exception(f"Failed to complete: {response.status_code} - {response.text}")

class Gemini:
    @instrument
    def complete(self, prompt):
        # Assuming your backend expects JSON data
        data = {
            "prompt": prompt,
        }

        # Adjust the URL accordingly
        url = "http://localhost:8080/api/v1/gemini/text"

        # Make a POST request to your backend
        response = requests.post(url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Assuming your backend returns the completion in JSON format
            completion = response.json()
            return completion
        else:
            # Handle errors here, raise an exception or return an error message
            raise Exception(f"Failed to complete: {response.status_code} - {response.text}")

gemini = Gemini()

# create a custom gemini feedback provider
class Gemini_Provider(Provider):
    def sentence_completion(self, first_sentence_part) -> float:
        result = gemini_pro(prompt = first_sentence_part),
        return result

gemini_provider = Gemini_Provider()

f_custom_function = Feedback(gemini_provider.sentence_completion, name = "Sentence Completion").on(Select.Record.calls[0].args.prompt)


gemini_provider.sentence_completion(first_sentence_part = "Please complete this sentence: I love to eat ice cream because it's")