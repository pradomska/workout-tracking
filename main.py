import requests
from datetime import datetime
import os

# My personal data. Used by Nutritionix to calculate calories.
GENDER = "male"
WEIGHT_KG = 69
HEIGHT_CM = 169
AGE = 24

# Nutritionix APP ID and API Key. Actual values are stored as environment variables.
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]
SHEETY_TOKEN = os.environ["ENV_SHEETY_TOKEN"]
GOOGLE_SHEET_NAME = 'workout'

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

# Nutritionix API Call
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(f"Nutritionix API call: \n {result} \n")

# Adding date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]

# Sheety API Call & Authentication
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    bearer_headers = {
        "Authorization": f"Bearer {SHEETY_TOKEN}"
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )

    print(f"Sheety Response: \n {sheet_response.text}")
