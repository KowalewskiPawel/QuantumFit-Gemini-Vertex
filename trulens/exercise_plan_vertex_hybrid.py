from trulens_eval import TruCustomApp
from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from prompts.exercise_plan import generate_training_prompt
import json
import requests

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

tru = Tru()
tru.reset_database()

 # Run the TruLens dashboard.
tru.run_dashboard(port=8024)


# create a custom class to instrument
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


class Gemini_Provider(Provider):
    def training_count(self, training_plan_response) -> float:
        try:
            trainings = json.loads(training_plan_response)
            trainings_counted = len(trainings)
        except json.JSONDecodeError:
            return 0.0

        trainings_length = trainings_length = float(
            gemini_pro_text.complete(
                f"""Rate the number. It should be 7, and the results is: {trainings_counted}. Respond with the float likelihood from 0.0 (number far from 7) to 1.0 (7) """
            )
        )

        return trainings_length


gemini_provider = Gemini_Provider()

f_custom_function = Feedback(
    gemini_provider.training_count, name="Training Count"
).on_response()

from trulens_eval import TruCustomApp

tru_gemini = TruCustomApp(
    gemini, app_id="gemini_exercise_plan", feedbacks=[f_custom_function]
)

from flask import Flask, request

app = Flask(__name__)

@app.route('/generate_plans', methods=['POST'])
def generate_plans():
    aim = request.json.get('aim')
    exercise_frequency = request.json.get('exerciseFrequency')
    experience = request.json.get('experience')
    gender = request.json.get('gender')
    target_weight = request.json.get('targetWeight')
    birth_year = request.json.get('birthYear')

    exercise_plan_prompt = generate_training_prompt(aim, exercise_frequency, experience, gender, target_weight, birth_year)

    # Use the prompt with your TruLens application.
    with tru_gemini as recording:
        result = gemini.complete(prompt=exercise_plan_prompt)

    return {'message': result }, 200

if __name__ == '__main__':
    app.run(port=5000)
