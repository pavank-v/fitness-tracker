from rest_framework.exceptions import NotFound
from datetime import timedelta
import requests
import json
import os


# Helper function to get the nutritional facts
def nutritional_facts(food_name, quantity):
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    api_key = os.environ.get('CALORIE_NINJA_API')

    query = f"{quantity} grams of {food_name}"

    response = requests.get(api_url + query, headers={"X-Api-Key": api_key})

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        return data["items"][0]
    else:
        raise NotFound(detail="Food Info is not found")


# Helper function to get the recipes
def recipe_recommendation(food_name):
    api_url = "https://api.api-ninjas.com/v1/recipe?query="
    api_key = os.environ.get('API_NINJA')

    response = requests.get(api_url + food_name, headers={"X-Api-Key": api_key})

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        return data
    else:
        raise NotFound(detail="Recipe not found")


# Helper function to return the calories of a specified food
def calories_finder(food_name, quantity):
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    api_key = os.environ.get('CALORIE_NINJA_API')
    query = f"{quantity} grams of {food_name}"

    response = requests.get(api_url + query, headers={"X-Api-Key": api_key})
    print(response)

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        return data["items"][0]
    else:
        return {
            "calories": 0,
            "protein_g": 0,
            "carbohydrates_total_g": 0,
            "fat_total_g": 0,
        }


# Helper Function to calculate end date
# of a diet plan or workout plan
def calculate_end_date(start_date, duration_days=30):
    return start_date + timedelta(days=duration_days)
