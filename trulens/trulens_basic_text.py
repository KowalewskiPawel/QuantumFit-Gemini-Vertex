from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from trulens_eval import Select

import requests

tru = Tru()
tru.reset_database()

# Custom class to instrument

def gemini_pro_text(prompt):
    data = {
            "prompt": prompt,
        }

        # Adjust the URL accordingly
    url = "http://localhost:8080/api/v1/gemini/text"

        # Make a POST request to the backend
    response = requests.post(url, json=data)

        # Check if the request was successful
    if response.status_code == 200:
        completion = response.json()
        return completion['message']
    else:
            # Handle errors here, raise an exception or return an error message
        raise Exception(f"Failed to complete: {response.status_code} - {response.text}")

class Gemini:
    @instrument
    def complete(self, prompt):
        # Backend expects JSON data
        data = {
            "prompt": prompt,
        }

        # Adjust the URL accordingly
        url = "http://localhost:8080/api/v1/gemini/text"

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

# Create a custom gemini feedback provider
class Gemini_Provider(Provider):
    def sentence_completion(self, first_sentence_part) -> float:
        result = float(gemini_pro_text(prompt = first_sentence_part)),
        return result

gemini_provider = Gemini_Provider()

f_custom_function = Feedback(gemini_provider.sentence_completion, name = "Sentence Completion").on(Select.Record.calls[0].args.prompt)


gemini_provider.sentence_completion(first_sentence_part = "Please complete this sentence: I love to eat ice cream because it's, and rate it from 1 to 5. Output: it as a pure number without anything else.")

from trulens_eval import TruCustomApp
tru_gemini = TruCustomApp(gemini, app_id = "gemini", feedbacks = [f_custom_function])

with tru_gemini as recording:
    gemini.complete(
    prompt="Please complete this sentence: I love to eat ice cream because it's, and rate it from 1 to 5. Output: it as a pure number without anything else.",
    )