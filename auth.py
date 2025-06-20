import streamlit as st
import hashlib
import json
import os

USER_DB = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def signup_user(name, username, email, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = {
        "name": name,
        "email": email,
        "password": hash_password(password)
    }
    save_users(users)
    return True, "User registered successfully!"

def login_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return True, users[username]["name"]
    return False, None
