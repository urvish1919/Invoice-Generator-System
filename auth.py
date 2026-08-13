import os

USER_FILE = "users.txt"


def initialize_user_file():
    """Create users.txt if it doesn't exist."""
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            pass


def signup(username, password):
    """
    Register a new user.
    Returns (True, message) if successful,
    otherwise (False, message).
    """
    initialize_user_file()

    username = username.strip().lower()
    password = password.strip()

    if username == "" or password == "":
        return False, "Username and Password cannot be empty."

    with open(USER_FILE, "r") as file:
        users = file.readlines()

    for user in users:
        saved_username = user.strip().split(",")[0]
        if saved_username == username:
            return False, "Username already exists."

    with open(USER_FILE, "a") as file:
        file.write(f"{username},{password}\n")

    return True, "Signup Successful."


def login(username, password):
    """
    Authenticate an existing user.
    Returns (True, message) if credentials are valid,
    otherwise (False, message).
    """
    initialize_user_file()

    username = username.strip().lower()
    password = password.strip()

    with open(USER_FILE, "r") as file:
        users = file.readlines()

    for user in users:
        data = user.strip().split(",")

        if len(data) != 2:
            continue

        saved_username, saved_password = data

        if saved_username == username and saved_password == password:
            return True, "Login Successful."

    return False, "Invalid Username or Password."