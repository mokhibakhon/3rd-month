import json
from datetime import datetime


class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions


class Transaction:
    def __init__(self, amount, timestamp):
        self.amount = amount
        self.timestamp = timestamp


class User:
    def __init__(self, username, password, language):
        self.username = username
        self.password = password
        self.language = language
        self.card_details = {}
        self.transactions = []

    def add_card_details(self, card_name, card_number, expiry_date):
        self.card_details = {
            "card_name": card_name,
            "card_number": card_number,
            "expiry_date": expiry_date,
            "balance": 0  # Initial balance is set to 0
        }

    def make_payment(self, amount):
        if amount <= self.card_details.get("balance", 0):
            self.card_details["balance"] -= amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transactions.append(Transaction(amount, timestamp))
            return True
        else:
            return False


class BakingApp:
    def __init__(self):
        self.recipes = []
        self.users = []
        self.load_user_data()

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def search_recipe(self, keyword):
        results = []
        for recipe in self.recipes:
            if keyword.lower() in recipe.name.lower():
                results.append(recipe)
        return results

    def register_user(self, username, password, language):
        new_user = User(username, password, language)
        self.users.append(new_user)
        self.save_user_data()

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def save_user_data(self):
        with open("user_data.json", "w") as file:
            user_data = []
            for user in self.users:
                user_data.append({
                    "username": user.username,
                    "password": user.password,
                    "language": user.language,
                    "card_details": user.card_details,
                    "transactions": [(t.amount, t.timestamp) for t in user.transactions]
                })
            json.dump(user_data, file, indent=4)

    def load_user_data(self):
        try:
            with open("user_data.json", "r") as file:
                user_data = json.load(file)
                for data in user_data:
                    user = User(data["username"], data["password"], data["language"])
                    user.card_details = data["card_details"]
                    user.transactions = [Transaction(amount, timestamp) for amount, timestamp in data["transactions"]]
                    self.users.append(user)
        except FileNotFoundError:
            pass


# Example usage:
if __name__ == "__main__":
    app = BakingApp()

    # Language selection
    print("Choose your language:")
    print("1. English")
    print("2. Russian")
    print("3. Uzbek")
    language_choice = input("Enter your choice: ")

    if language_choice == "1":
        language = "English"
    elif language_choice == "2":
        language = "Russian"
    elif language_choice == "3":
        language = "Uzbek"
    else:
        print("Invalid choice. Defaulting to English.")
        language = "English"

    # Registration
    print("\nRegistration:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    app.register_user(username, password, language)
    print("Registration successful!")


    # Login
    print("\nLogin:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user = app.login(username, password)
    if user:
        print(f"Welcome, {user.username}!")
    else:
        print("Invalid username or password. Please try again.")

    # Adding card details
    if user:
        print("\nAdd Card Details:")
        card_name = input("Enter card holder's name: ")
        card_number = input("Enter card number: ")
        expiry_date = input("Enter expiry date: ")
        user.add_card_details(card_name, card_number, expiry_date)
        app.save_user_data()
        print("Card details saved successfully!")

    # Payment
    if user:
        print("\nMake Payment:")
        amount = float(input("Enter the amount to pay: "))
        if user.make_payment(amount):
            print("Payment successful!")
        else:
            print("Insufficient balance. Payment failed!")

    # Monitoring
    if user:
        print("\nTransaction History:")
        for transaction in user.transactions:
            print(f"Amount: {transaction.amount}, Time: {transaction.timestamp}")
