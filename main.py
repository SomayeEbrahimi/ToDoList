from colorama import init, Fore
from datetime import datetime
import json
import sys

def main():
    init() # Initialize colorama
    
    while True:
        show_help_menu()
        user_input = input(Fore.WHITE + "Please Enter a Letter: ").upper()
        
        do_action(user_input)

""" Show letters to do an action """
def show_help_menu():
    print("To Do List Commands:")
    display_message("L: Show All Items","L")
    display_message("A: Add New Item", "A")
    display_message("U: Update An Item", "U")
    display_message("R: Remove An Item", "R")
    display_message("C: Clear All", "C")
    display_message("E: Exit", "E")

""" Based on the user_input do the proper action """
def do_action(user_input):
    if user_input == 'A':
        description = input("Enter the description for the new item: ")
        todo_datetime = input("Enter the to-do datetime (e.g., 2024-08-11T10:00:00): ")
        add_new_item(description, todo_datetime)
        display_message("Item added successfully!\n", user_input)

    elif user_input == 'U':
        target_id = input("Enter the ID of the item to update: ")
        description = input("Enter the new description: ")
        todo_datetime = input("Enter the new to-do datetime (e.g., 2024-08-11T10:00:00): ")
        result = update_item(target_id, description, todo_datetime)

        if result:
            display_message("Item updated successfully!\n", user_input)
        else:
            display_message("Id is invalid!\n", user_input)

    elif user_input == 'R':
        target_id = input("Enter the ID of the item to remove: ")
        result = remove_item(target_id)
        
        if result:
            display_message("Item removed successfully!\n", user_input)
        else:
            display_message("Id is invalid!\n", user_input)

    elif user_input == 'C':
        result = clear_all_items()

        if result:
            display_message("All items cleared successfully!\n", user_input)

    elif user_input == 'E':
        exit_program()

    elif user_input == 'L':
        show_all_items()

    else:
        print(Fore.RED + "Invalid input. Please try again. \n")

""" Show all items in json file """
def show_all_items():

    try:
        with open("to-do-list.json", "r", encoding="utf8") as file:
            data = json.load(file)
            print(f"{json.dumps(data, indent=2)} \n")
            
    except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "File not found. \n")
            return
    
""" Add new object to json file, that contains auto generated id, description and datetime """
def add_new_item(description, todo_datetime):
    try:
        with open("to-do-list.json", "r", encoding="utf8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
            print("File is empty. Initializing with an empty list. \n")
            data = []
    except FileNotFoundError:
        data = []

    last_id = data[-1]["id"] if data else 0

    formatted_date = format_datetime(todo_datetime)

    new_item = {
        "id": last_id + 1,
        "description": description,
        "datetime": formatted_date
    }

    data.append(new_item)
        
    with open("to-do-list.json", "w", encoding="utf8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

""" Update the selected object and update json file, that contains description and datetime """
def update_item(target_id, description, todo_datetime):
    try:
        with open("to-do-list.json", "r", encoding="utf8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "File is empty. \n")
            return
    except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "File not found. \n")
            return
        
    formatted_date = format_datetime(todo_datetime)

    for item in data:
        if item['id'] == int(target_id):
            item['description'] = description
            item['datetime'] = formatted_date
            break

    with open("to-do-list.json", "w", encoding="utf8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        return True

""" Remove the selected object from json list """
def remove_item(target_id):
    try:
        with open("to-do-list.json", "r", encoding="utf8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "File is empty. \n")
            return
    except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "File not found. \n")
            return
        
    for item in data:
        if item['id'] == int(target_id):
            data = [item for item in data if item['id'] != int(target_id)]

            with open("to-do-list.json", "w", encoding="utf8") as file:
                json.dump(data, file, indent=2)
                return True

""" Clear all objects in josn list """
def clear_all_items():
    try:    
        with open("to-do-list.json", "w", encoding="utf8") as file:
            json.dump([], file)
            return True

    except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "File is empty. \n")
            return
    except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "File not found. \n")
            return

""" Exit the program """
def exit_program():
    print("Exiting the program...")
    sys.exit(0)

""" Show messages in defined color based on action type (input_user) """
def display_message(text, action_type):
    message_color_map = {
        'R': Fore.RED,
        'U': Fore.YELLOW,
        'A': Fore.GREEN,
        'C': Fore.LIGHTBLACK_EX,
        'L': Fore.BLUE,
        'E': Fore.CYAN
    }

    print(message_color_map[action_type] + text)

""" Format user date time input to something like: 24 Sep 2025 12:02"""
def format_datetime(tododatetime_str):
    tododatetime = datetime.strptime(tododatetime_str, "%Y-%m-%dT%H:%M:%S")
    formatted_date = tododatetime.strftime("%d %b %Y %H:%M")

    return formatted_date

main()