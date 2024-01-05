from datetime import datetime


def generate_training_prompt(
    aim, exercise_frequency, gym_experience, sex, target_weight, year_of_birth
):
    age = datetime.now().year - year_of_birth

    def filtered_aim(aim):
        if "lose" in aim:
            return "lose weight"
        if "gain" in aim:
            return "gain weight and muscle mass"
        if "maintain" in aim:
            return "maintain their current physique"
        return "improve their overall fitness"

    def filtered_experience(experience):
        if experience < 3:
            return "novice"
        if experience < 6:
            return "intermediate"
        if experience < 10:
            return "advanced"
        if experience < 14:
            return "expert"
        return "unknown"

    corrected_aim = filtered_aim(aim)
    corrected_experience = filtered_experience(gym_experience)

    return f"""Please strictly follow the requirements below THIS IS NOT A MEDICAL ADVICE!!!:

You are to create a 7 day training plan for a person who is looking to {corrected_aim}. This person 
is a {age} year old {sex} who exercises about {exercise_frequency} times per week at the gym. They have {corrected_experience} experience in gym workouts.

Based on the given information, you are to create a training plan that will help them to {corrected_aim} in order 
for them to achieve their target weight of {target_weight}kg. 
The training plan should focus on exercises that align with the person's goals and fitness level.

I need the training plan to be in JSON and in this shape.

Example response:

[
    {{
        "trainingSummary": "Biceps, Triceps, Shoulders",
        "trainings": [
            {{
                "training": "Biceps Curls",
                "name": "Biceps",
                "description":
                    "To perform biceps curls, stand with your feet shoulder-width apart, holding a dumbbell in each hand with an underhand grip. Bend your elbows and curl the dumbbells up towards your shoulders, keeping your upper arms stationary. Lower the dumbbells back down to the starting position.",
                "reps": "10",
                "sets": "3",
                "weight": "light to moderate",
            }},
            {{
                "training": "Triceps Pushdowns",
                "name": "Triceps",
                "description":
                    "To perform triceps pushdowns, attach a rope or bar to a cable machine and select a weight. Grasp the rope or bar with an overhand grip, then extend your arms overhead. Bend your elbows and lower the rope or bar towards your chest, keeping your upper arms close to your body. Push back up to the starting position.",
                "reps": "10",
                "sets": "3",
                "weight": "light to moderate",
            }},
            {{
                "training": "Shoulder Press",
                "name": "Shoulders",
                "description":
                    "To perform shoulder press, sit on a bench with a barbell resting across the front of your shoulders. Unrack the barbell and press it overhead until your arms are fully extended. Lower the barbell back down to the starting position.",
                "reps": "8",
                "sets": "3",
                "weight": "moderate",
            }},
        ]}},
        # follow the same pattern and format for the remaining 6 days
]

Here are some other tips about the response for various fields.

    trainingSummary: This should provide a brief summary of the training plan for each day.

    trainings: This should be an array of objects, each representing a day in the training plan.

    if there is a rest day, the trainingSummary should be "Rest" and the trainings array should be empty.

    like in this example:

    {{
        "trainingSummary": "Rest Day",
        "trainings": [],
    }},

    day: Specifies the day of the training plan.

    type: Indicates the type of training for the day (e.g., cardio, strength training, rest).

    exercises: This should be an array of exercises for the day.

    Concluding remarks:
    - Output: JSON object
    - The JSON object should match the exact format as in the example above. There should be no spaces in the response
    - Do not reply with any words! Do not put "/\n" in the output.
    - There should be some variety in terms of exercises and what the person does. The training plan should not be 
    identical every day. It's okay for exercises to repeat 2-4 times over a 7 day period. A few exercises will 
  only be 1-2 times in a week. Likewise, a few will be 5-6 times in a week. The key is to have a balanced and 
  effective training plan. 
  """
