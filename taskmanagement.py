import hashlib
import os
import json

users_file = "users.json"
tasks_folder = "tasks"

# Ensure tasks directory exists
os.makedirs(tasks_folder, exist_ok=True)

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(users_file):
        return {}
    with open(users_file, "r") as f:
        return json.load(f)

def save_users(users):
    with open(users_file, "w") as f:
        json.dump(users, f)

def get_task_file(username):
    return os.path.join(tasks_folder, f"{username}_tasks.json")

def load_tasks(username):
    task_file = get_task_file(username)
    if not os.path.exists(task_file):
        return []
    with open(task_file, "r") as f:
        return json.load(f)

def save_tasks(username, tasks):
    task_file = get_task_file(username)
    with open(task_file, "w") as f:
        json.dump(tasks, f)

# Authentication functions
def register():
    users = load_users()
    username = input("Choose a username: ")
    if username in users:
        print("❌ Username already exists!")
        return None
    password = input("Choose a password: ")
    users[username] = hash_password(password)
    save_users(users)
    print("✅ Registration successful!")
    return username

def login():
    users = load_users()
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username] == hash_password(password):
        print("✅ Login successful!")
        return username
    else:
        print("❌ Invalid credentials.")
        return None

# Task management
def add_task(username):
    tasks = load_tasks(username)
    description = input("Enter task description: ")
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "status": "Pending"})
    save_tasks(username, tasks)
    print("✅ Task added.")

def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("📭 No tasks found.")
        return
    for task in tasks:
        print(f"{task['id']}. {task['description']} - {task['status']}")

def mark_task_completed(username):
    tasks = load_tasks(username)
    view_tasks(username)
    try:
        task_id = int(input("Enter task ID to mark as completed: "))
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "Completed"
                save_tasks(username, tasks)
                print("✅ Task marked as completed.")
                return
        print("❌ Task ID not found.")
    except ValueError:
        print("❌ Invalid input.")

def delete_task(username):
    tasks = load_tasks(username)
    view_tasks(username)
    try:
        task_id = int(input("Enter task ID to delete: "))
        tasks = [task for task in tasks if task["id"] != task_id]
        # Reassign IDs
        for idx, task in enumerate(tasks, start=1):
            task["id"] = idx
        save_tasks(username, tasks)
        print("🗑️ Task deleted.")
    except ValueError:
        print("❌ Invalid input.")

# Main menu
def task_menu(username):
    while True:
        print(f"\n📋 Task Menu - Logged in as {username}")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("👋 Logged out.")
            break
        else:
            print("❌ Invalid option.")

# App start
def main():
    while True:
        print("\n🔐 Task Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            user = register()
            if user:
                task_menu(user)
        elif choice == "2":
            user = login()
            if user:
                task_menu(user)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
