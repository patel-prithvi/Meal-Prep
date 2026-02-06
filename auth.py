from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

def user_exists(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, is_active FROM users WHERE email = %s ", (email,))
    result= cur.fetchone()
    
    cur.close()
    conn.close()
    if not result:
        return None
    return result


def create_user(data):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = generate_password_hash(data["password"])

    cur.execute("""
        INSERT INTO users
        (name, email, password_hash, age, gender, height, weight,
         activity_level, goal, disease, diet_type, allergies)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["name"],
        data["email"],
        password_hash,
        data["age"],
        data["gender"],
        data["height"],
        data["weight"],
        data["activity_level"],
        data["goal"],
        data["disease"],
        data["diet_type"],
        data["allergies"]
    ))
    conn.commit()   # commit first

    cur.execute(
        "SELECT id FROM users WHERE email = %s",
        (data["email"],)
    )
    user_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return user_id

def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                SELECT name, email, age, gender, height, weight, activity_level, goal, disease, diet_type, allergies 
                FROM users WHERE id=%s
                """, (user_id,))
    u = cur.fetchone()

    user={"name":u[0], "email":u[1], "age":u[2], "gender":u[3], "height":u[4], "weight":u[5], 
          "activity":u[6], "goal":u[7], "disease":u[8], "diet":u[9], "allergy":u[10]}

    cur.close()
    conn.close()
    return user

def authenticate_user_with_role(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password_hash, role, is_active FROM users WHERE email=%s",
        (email,)
    )
    u = cur.fetchone()
    cur.close()
    conn.close()

    if not u[3]:
        return "DISABLED"
    
    if u and check_password_hash(u[1], password):
        return {"id": u[0], "role": u[2]}
    return None

def get_user_name(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row[0] if row else "User"