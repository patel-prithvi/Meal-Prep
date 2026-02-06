from db import get_connection
import json

def fetch_all_meals():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT meal_id, name, ingredients, disease, meal_type, diet_type,
               calories, protein, carbs, fat, sodium,
               recipe_youtube_link, photo
        FROM meals
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    meals = []
    for r in rows:
        meals.append({
            "meal_id": r[0],
            "name": r[1],
            "ingredients": r[2].lower(),
            "disease": r[3] or [],
            "meal_type": r[4],
            "diet_type": r[5],
            "calories": r[6],
            "protein": r[7],
            "carbs": r[8],
            "fat": r[9],
            "sodium": r[10],
            "youtube": r[11],
            "photo": r[12]
        })
    return meals

def save_meal_plan(user_id, start, end, calories, carbs, protein, fat, sodium, plan):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO meal_plans
        (user_id, start_plan_date, end_plan_date, daily_calories, 
                daily_protein, daily_carbs, daily_fat, daily_sodium, plan)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        start,
        end,
        calories,
        protein,
        carbs,
        fat,
        sodium,
        json.dumps(plan)
    ))

    conn.commit()
    cur.close()
    conn.close()

def get_meal_plan(user_id):
    """
    Returns:
    {
      start_date: date,
      end_date: date,
      final_meal: dict
    }
    or None if no plan
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT start_plan_date, end_plan_date, daily_calories, daily_protein, daily_carbs, 
        daily_fat, plan, nutrition_chart
        FROM meal_plans
        WHERE user_id = %s AND is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    start_date, end_date, daily_calories, daily_protein, daily_carbs, daily_fat, final_meal, chart = row

    return {
        "start_date": start_date,
        "end_date": end_date,
        "daily_calories": daily_calories,
        "daily_protein": daily_protein,
        "daily_carbs": daily_carbs,
        "daily_fat": daily_fat,
        "final_meal": final_meal,
        "chart": chart
    }

def save_nutrition_chart(chart_bytes, user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE meal_plans
        SET nutrition_chart = %s
        WHERE user_id = %s
    """, (chart_bytes, user_id))

    conn.commit()
    cur.close()
    conn.close()