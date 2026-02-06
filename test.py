from werkzeug.security import generate_password_hash

password = "Admin@123Mealprep"
print(generate_password_hash(password))
