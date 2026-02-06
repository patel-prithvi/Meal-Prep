import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "prithvitpatel@gmail.com"      # YOUR gmail
SENDER_PASSWORD = "dtfe uzgl fmjk rczd"     # app password

def send_welcome_email(to_email, name):
    subject = "🎉 Welcome to Meal Planner!"
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background:#f5f5f5; padding:20px;">
        <div style="max-width:600px; background:white; padding:20px; border-radius:10px;">
          <h2 style="color:#4B5320;">Welcome to Meal Planner, {name}! 🥗</h2>
          <p>
            Your email has been successfully verified.<br><br>
            You are now part of <strong>India’s 1st Free Indian Meal Planner</strong>.
          </p>
          <p>
            ✔ Personalized meal plans<br>
            ✔ Nutrition-focused guidance<br>
            ✔ Dietician-recommended planning
          </p>
          <p style="margin-top:20px;">
            👉 Login and start your healthy journey today!
          </p>
          <br>
          <p style="color:#777;">
            — Team Meal Planner
          </p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = f"Meal Planner <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
