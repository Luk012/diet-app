from openai import AzureOpenAI
import os
import dotenv

dotenv.load_dotenv()

client = AzureOpenAI(
    azure_endpoint='https://dietplanner.openai.azure.com/',
    api_key="0ac2308b825d49f18cd7b3482f8c9f09",
    api_version="2023-10-01-preview"
)

deployment = 'gpt-35'

def collect_user_input():
    user_data = {}
    user_data['biological_sex'] = input("Biological Sex (Male/Female): ")
    user_data['goal'] = input("Goal (Lose weight, Gain muscle, Stay healthy): ")
    user_data['height'] = float(input("Height (in cm): "))
    user_data['body_mass'] = float(input("Body Mass (in kg): "))
    user_data['age'] = int(input("Age: "))
    user_data['activity_level'] = input("How active are you as a person (Sedentary, Slightly active, Active, Very active): ")
    user_data['workout_frequency'] = input("Do you work out? (I don’t exercise, I go to the gym 1-2 times a week, I go to the gym 3-4 times a week, I go to the gym almost every day): ")
    user_data['sleep'] = input("How much do you usually sleep? (Less than 5 hours, 5-6 hours, 7-8 hours, More than 8 hours): ")
    user_data['water_intake'] = input("How much water do you drink daily? (Only coffee or tea, Less than 0.5 L, 0.5 - 1.5 L, 1.5 - 2.5 L, I don't count; it depends): ")
    user_data['meal_preparation_time'] = input("How much time can you spend preparing your meal? (I’m busy, Depends on my schedule, I have time): ")
    user_data['health_issues'] = input("Do you have any health issues? (List any that apply or 'None'): ")
    user_data['specific_diet'] = input("Do you have any specific food diets? (List any that apply or 'None'): ")
    user_data['food_allergies'] = input("Do you have any food allergies? (List any that apply or 'None'): ")
    user_data['disliked_foods'] = input("Do you have any food items that you don’t like? (Yes/No): ")
    if user_data['disliked_foods'].lower() == 'yes':
        user_data['disliked_foods_list'] = input("Please list the food items you don’t like: ")
    else:
        user_data['disliked_foods_list'] = "None"
    user_data['liked_foods'] = input("What do you like to eat? (List your preferred foods from different categories): ")
    user_data['diet_duration'] = input("On what period of time would you like your diet to extend for? (1 month, 1-3 months, 3-6 months, 1 year): ")
    return user_data

user_data = collect_user_input()

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
print(modified_diet_plan)

