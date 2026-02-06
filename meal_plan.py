import random
from datetime import date, timedelta
from db import get_connection
from meal_service import fetch_all_meals, save_meal_plan

ACTIVITY_MULTIPLIER = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725
}

MEAL_SPLIT = {
    "breakfast": 0.25,
    "lunch": 0.40,
    "dinner": 0.35
}

def calculate_bmr(user):
    if user["gender"] == "male":
        return 10*user["weight"] + 6.25*user["height"] - 5*user["age"] + 5
    return 10*user["weight"] + 6.25*user["height"] - 5*user["age"] - 161

def calculate_daily_calories(user):
    calories = calculate_bmr(user) * ACTIVITY_MULTIPLIER[user["activity"]]
    if user["goal"] == "Lose Weight":
        calories -= 500
    elif user["goal"] == "Gain Weight":
        calories += 500
    return int(calories)

def calculate_macros(cal):
    return {
        "carbs_g": int(cal * 0.5 / 4),
        "protein_g": int(cal * 0.2 / 4),
        "fat_g": int(cal * 0.3 / 9),
        "sodium_mg": 2000
    }

def filter_meals(meals, user, meal_type, max_cal):
    result = []
    for m in meals:
        if m["meal_type"] != meal_type:
            continue
        if m["diet_type"] != user["diet"]:
            continue
        if any(d in m["disease"] for d in user["disease"]):
            continue
        if any(a in m["ingredients"] for a in user["allergy"]):
            continue
        if m["calories"] > max_cal:
            continue
        result.append(m)
    return result

def generate_7_day_meal_plan(user, user_id):
    meals = fetch_all_meals()
    used_meals = set()

    total_cal = calculate_daily_calories(user)
    macros = calculate_macros(total_cal)

    start_date = date.today()
    end_date = start_date + timedelta(days=6)

    final_plan = {}

    for i in range(7):
        current_day = start_date + timedelta(days=i)
        day_key = current_day.strftime("%d-%m-%Y")
        final_plan[day_key] = {}

        for meal_type in ["breakfast", "lunch", "dinner"]:
            limit = int(total_cal * MEAL_SPLIT[meal_type])
            available = filter_meals(meals, user, meal_type, limit)
            random.shuffle(available)

            for meal in available:
                if meal["meal_id"] not in used_meals:
                    used_meals.add(meal["meal_id"])
                    final_plan[day_key][meal_type] = meal
                    break

    save_meal_plan(
        user_id,
        start_date,
        end_date,
        total_cal,
        macros["carbs_g"],
        macros["protein_g"],
        macros["fat_g"],
        macros["sodium_mg"],
        final_plan
    )

    return final_plan
