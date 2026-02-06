# ai_service.py
from google import genai

def generate_health_tip(
    client,
    calories, protein, carbs, fat,
    target_calories, target_protein, target_carbs, target_fat,
    goal
):
    prompt = f"""
You are an expert Indian nutrition coach.

User goal: {goal}

TARGET intake for the day:
- Calories: {target_calories}
- Protein: {target_protein} g
- Carbs: {target_carbs} g
- Fat: {target_fat} g

ACTUAL intake today:
- Calories: {calories}
- Protein: {protein} g
- Carbs: {carbs} g
- Fat: {fat} g

Your task:
Analyze the gap between ACTUAL vs TARGET intake and give ONE corrective, actionable tip.

STRICT RULES:
- Tip MUST reference at least one comparison (higher/lower than target)
- Focus on TODAY or TOMORROW action
- Align advice with the user's goal
- Indian lifestyle friendly
- Max 20 words
- Simple English
- No emojis
- No medical claims
- No generic advice (ban: stay hydrated, eat balanced food, exercise regularly)
- No markdown

Examples of GOOD tips:
- "Protein is 25g below target; add paneer or curd at dinner to support muscle."
- "Calories exceeded target; reduce roti by one tomorrow to support fat loss."
- "Carbs are high for weight loss; replace rice with vegetables at night."

Now generate the tip.
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()

def generate_grocery_list(client, ingredients_text):
    prompt = f"""
        You are an Indian grocery planning assistant.

        Ingredients used today:
        {ingredients_text}

        Task:
        Create a grocery list WITH quantities for ONE person for ONE day.

        FORMAT RULES (STRICT):
        - Plain text only
        - NO markdown
        - NO *, -, bullets
        - Use headings like: Vegetables:, Grains:, Proteins:
        - Each item on new line: Onion – 2 medium

        Rules:
        - Group items by category
        - Add practical quantities
        - Avoid grams for vegetables
        - Remove duplicates
        - No emojis
        - No explanations
        """

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()
