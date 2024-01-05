from trulens_eval import TruCustomApp
from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from llama_index.llms.vertex import Vertex
from google.oauth2 import service_account
from prompts.exercise_plan import generate_training_prompt
import json

filename = "../gcp.json"
credentials: service_account.Credentials = (
    service_account.Credentials.from_service_account_file(filename)
)

gemini_pro = Vertex(
    model="gemini-pro",
    project=credentials.project_id,
    credentials=credentials,
    temperature=0.5,
    max_tokens=8192,
)

tru = Tru()
tru.reset_database()
  # Run the TruLens dashboard.
tru.run_dashboard(port=8024)


# create a custom class to instrument
class Gemini:
    @instrument
    def complete(self, prompt):
        completion = gemini_pro.complete(prompt).text
        return completion


gemini = Gemini()


class Gemini_Provider(Provider):
    def training_count(self, training_plan_response) -> float:
        try:
            trainings = json.loads(training_plan_response)
            trainings_counted = len(trainings)
        except json.JSONDecodeError:
            return 0.0
        
        trainings_length = float(
            gemini_pro.complete(
                f"""Rate the number. It should be 7, and the results is: {trainings_counted}. Respond with the float likelihood from 0.0 (number far from 7) to 1.0 (7) """
            ).text
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
