from db import get_connection
from datetime import date

def get_admin_stats():
    conn = get_connection()
    cur = conn.cursor()

    # total users
    cur.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = cur.fetchone()[0]

    # active meal plans
    cur.execute("""
        SELECT COUNT(*) FROM meal_plans
        WHERE end_plan_date >= %s
    """, (date.today(),))
    active_plans = cur.fetchone()[0]

    # total blogs
    # cur.execute("SELECT COUNT(*) FROM blogs")
    # total_blogs = cur.fetchone()[0]

    # today signups
    # cur.execute("""
    #     SELECT COUNT(*) FROM users
    #     WHERE DATE(created_at) = %s
    # """, (date.today(),))
    # today_users = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "total_users": total_users,
        "active_plans": active_plans,
        "total_blogs": 100,
        "today_users": 150
    }

def get_all_users_with_details():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, age, gender, height, weight,
               activity_level, goal, diet_type, disease, allergies,
               created_at, is_active
        FROM users
        WHERE role='user'
        ORDER BY created_at DESC
    """)

    row = cur.fetchall()
    users = []
    for r in row:
        users.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "age" : r[3],
            "gender": r[4],
            "height": r[5],
            "weight": r[6],
            "activity": r[7],
            "goal": r[8],
            "diet": r[9],
            "disease": r[10],
            "allergies": r[11],
            "created_at": r[12],
            "is_active": r[13]
        })

    cur.execute("""
        SELECT user_id, start_plan_date, end_plan_date,
               daily_calories, daily_protein, daily_carbs, daily_fat
        FROM meal_plans
        WHERE is_active= true
        ORDER BY start_plan_date DESC
    """)

    rows = cur.fetchall()
    plans = []
    for r in rows:
        plans.append({
            "user_id": r[0],
            "start_plan_date": r[1],
            "end_plan_date": r[2],
            "daily_calories" : r[3],
            "daily_protein": r[4],
            "daily_carbs": r[5],
            "daily_fat": r[6],
        })

    cur.close()
    conn.close()

    return users, plans

def get_active_meal_plans():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            m.plan_id,
            m.user_id,
            u.name,
            u.email,
            m.start_plan_date,
            m.end_plan_date,
            m.daily_calories,
            m.daily_protein,
            m.daily_carbs,
            m.daily_fat
        FROM meal_plans m
        JOIN users u ON u.id = m.user_id
        WHERE m.start_plan_date <= CURRENT_DATE
          AND m.end_plan_date >= CURRENT_DATE
        ORDER BY m.end_plan_date ASC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    plans = []
    for r in rows:
        plans.append({
            "plan_id": r[0],
            "user_id": r[1],
            "name": r[2],
            "email": r[3],
            "start": r[4],
            "end": r[5],
            "calories": r[6],
            "protein": r[7],
            "carbs": r[8],
            "fat": r[9],
        })

    return plans

def get_all_meal_plans():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            m.plan_id,
            m.user_id,
            u.name,
            u.email,
            m.start_plan_date,
            m.end_plan_date,
            m.daily_calories,
            m.daily_protein,
            m.daily_carbs,
            m.daily_fat
        FROM meal_plans m
        JOIN users u ON u.id = m.user_id
        ORDER BY m.end_plan_date ASC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    plans = []
    for r in rows:
        plans.append({
            "plan_id": r[0],
            "user_id": r[1],
            "name": r[2],
            "email": r[3],
            "start": r[4],
            "end": r[5],
            "calories": r[6],
            "protein": r[7],
            "carbs": r[8],
            "fat": r[9],
        })

    return plans