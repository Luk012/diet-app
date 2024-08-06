from flask import Flask, request, jsonify
from openai import AzureOpenAI
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

dotenv.load_dotenv()

client = AzureOpenAI(
    azure_endpoint='https://dietplanner.openai.azure.com/',
    api_key="0ac2308b825d49f18cd7b3482f8c9f09",
    api_version="2023-10-01-preview"
)

deployment = 'gpt-35'

@app.route('/api/generate-diet-plan', methods=['POST'])
def generate_diet_plan():
    user_data = request.json

    diet_prompt = (
        f"As an experienced nutritionist, generate a comprehensive diet plan for a {user_data['biological_sex']} aiming to {user_data['goal']}. Below are the detailed characteristics and preferences of the individual:\n\n"
        f"Height: {user_data['height']} cm\n"
        f"Body Mass: {user_data['body_mass']} kg\n"
        f"Age: {user_data['age']} years\n"
        f"Activity Level: {user_data['activity_level']}\n"
        f"Workout Frequency: {user_data['workout_frequency']}\n"
        f"Sleep: {user_data['sleep']} hours per night\n"
        f"Water Intake: {user_data['water_intake']} liters per day\n"
        f"Meal Preparation Time: {user_data['meal_preparation_time']} minutes per day\n"
        f"Health Issues: {user_data['health_issues']}\n"
        f"Specific Diet: {user_data['specific_diet']}\n"
        f"Food Allergies: {user_data['food_allergies']}\n"
        f"Disliked Foods: {user_data['disliked_foods_list']}\n"
        f"Liked Foods: {user_data['liked_foods']}\n"
        f"Diet Duration: {user_data['diet_duration']}\n\n"
        f"Ensure the diet plan is tailored to the user's specific needs and goals, providing balanced nutrition throughout the day. Include 7 meal examples for each time of day (breakfast, lunch, dinner, and snacks) to offer variety. Each meal example should consider the user’s dietary preferences, allergies, and available meal preparation time. Make sure the diet plan is practical and sustainable over the specified diet duration. PLEASE GENERATE ONLY THE DIET PLAN, WITHOUT FURTHER INFORMATION"
    )

    messages = [{"role": "user", "content": diet_prompt}]
    completion = client.chat.completions.create(model=deployment, messages=messages, max_tokens=1000, temperature=0.5)

    diet_plan = completion.choices[0].message.content

    check_and_modify_prompt = (
        f"Given the following diet plan:\n\n{diet_plan}\n\n"
        f"Check if it contains any of the following allergens: {user_data['food_allergies']}. "
        f"Also, check if it contains any of the following disliked foods: {user_data['disliked_foods_list']}."
        f"Modify the diet plan accordingly to avoid these items and print the modified diet plan. PLEASE GENERATE ONLY THE DIET PLAN, WITHOUT FURTHER INFORMATION"
    )

    messages = [{"role": "user", "content": check_and_modify_prompt}]
    completion_check_and_modify = client.chat.completions.create(model=deployment, messages=messages, max_tokens=1000, temperature=0.5)

    modified_diet_plan = completion_check_and_modify.choices[0].message.content

    return jsonify({"diet_plan": modified_diet_plan})

if __name__ == '__main__':
    app.run(debug=True)