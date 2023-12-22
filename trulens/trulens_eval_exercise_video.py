from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval import Provider
from trulens_eval import Feedback
from trulens_eval import Select

import requests

tru = Tru()
tru.reset_database()

# Custom class to instrument

def gemini_pro_video(prompt, video_url, file_type):
    data = {
            "prompt": prompt,
            "videoUrl": video_url,
            "fileType": file_type
        }

        # Adjust the URL accordingly
    url = "http://localhost:8080/api/v1/gemini/video"

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
    def complete(self, prompt, video_url, file_type):
        # Backend expects JSON data
        data = {
            "prompt": prompt,
            "videoUrl": video_url,
            "fileType": file_type
        }

        # Adjust the URL accordingly
        url = "http://localhost:8080/api/v1/gemini/video"

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
    def exercise_video_analysis(self, video_prompt, video_to_analyze, video_file_type) -> float:
        exercise_correctness_score = float(gemini_pro_video(prompt = video_prompt, video_url = video_to_analyze, file_type = video_file_type).text),
        return exercise_correctness_score

gemini_provider = Gemini_Provider()

f_custom_function = Feedback(gemini_provider.exercise_video_analysis, name = "Exercise Analysis").on(Select.Record.calls[0].args.video_url)

from trulens_eval import TruCustomApp
tru_gemini = TruCustomApp(gemini, app_id = "gemini", feedbacks = [f_custom_function])

with tru_gemini as recording:
    gemini.complete(
    prompt="Rate the correctness of the exercise done in the video. The output should be a number between 0 and 100.",
    video_url="",
    file_type="video/mp4"
    )