# Importing built-in Python modules required for the project
import os
import re
import datetime

# ==========================================
# FUNCTIONS AND REGULAR EXPRESSIONS (REGEX)
# ==========================================

# Function to validate date format using Regular Expressions
def validate_date(date_str):
    # Regex pattern strictly enforces the format YYYY-MM-DD (4 digits - 2 digits - 2 digits)
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    # re.match checks if the string matches the pattern; returns True or False
    return bool(re.match(pattern, date_str))

# Function to append system actions to a log file
def log_action (action_text):
    try:
        # Opening file in 'a' (append) mode so new data is added without overwriting the old logs
        with open("action_log.txt", "a", encoding="utf-8") as file:
            # Getting current date and time and formatting it
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Writing formatted string (f-string) to the file
            file.write(f"[{timestamp}] {action_text}\n")
    except Exception as e:
        print(f"File Error: {e}")

# ==========================================
# WORKING WITH FILES (SAVE AND LOAD)
# ==========================================

# Function to write all resources from the dictionary into a text file
def save_resources(resources_map):
    try:
        # Opening file in 'w' (write) mode to overwrite the file with the latest state
        with open("resources.txt", "w", encoding="utf-8") as file:
            # Iterating through the dictionary
            for r_id, res in resources_map.items():
                # Checking if the object is an instance of the Equipment subclass to save its specific attributes
                if isinstance(res, Equipment):
                    file.write(f"{r_id}|{res.name}|{res.r_type}|{res.is_aval}|{res.condition}\n")
                else:
                    file.write(f"{r_id}|{res.name}|{res.r_type}|{res.is_aval}\n")
    except Exception as e:
        print(f"Error saving resources: {e}")

# Function to write all events to a text file
def save_events(events_map):
    try:
        with open("events.txt", "w", encoding="utf-8") as file:
            for e_id, ev in events_map.items():
                # Joining the list of resource IDs into a single string separated by spaces
                res_ids_str = " ".join(ev.resource_ids)
                file.write(f"{e_id}|{ev.title}|{ev.date}|{ev.time}|{ev.duration}|{res_ids_str}\n")
    except Exception as e:
        print(f"Error saving events: {e}")

# Function to read and restore resources from the text file into the dictionary
def load_resources(resources_map):
    # If the file does not exist yet, just return and do nothing
    if not os.path.exists("resources.txt"):
        return
    try:
        # Opening file in 'r' (read) mode
        with open("resources.txt", "r", encoding="utf-8") as file:
            # Reading the file line by line using a for loop
            for line in file:
                # Removing trailing newlines (.strip()) and splitting the string by the '|' character
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    # Assigning extracted values to variables
                    r_id, name, r_type = parts[0], parts[1], parts[2]
                    is_aval = (parts[3] == "True")
                    
                    # If there are 5 parts, it means it's an Equipment object (contains 'condition')
                    if len(parts) == 5:
                        resources_map[r_id] = Equipment(name, r_type, is_aval, parts[4])
                    else:
                        resources_map[r_id] = Resource(name, r_type, is_aval)
    except Exception as e:
        print(f"Error loading resources: {e}")

# Function to read and restore events from the text file
def load_events(events_map):
    if not os.path.exists("events.txt"):
        return
    try:
        with open("events.txt", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 5:
                    e_id, title, date, time, duration = parts[0], parts[1], parts[2], parts[3], parts[4]
                    # Creating a new Event object
                    ev = Event(title, date, time, duration)
                    
                    # If a 6th part exists, it contains the assigned resource IDs
                    if len(parts) == 6 and parts[5] != "":
                        # Splitting the string back into a list of IDs
                        ev.resource_ids = parts[5].split(" ")
                        
                    # Adding the restored object to the dictionary
                    events_map[e_id] = ev
    except Exception as e:
        print(f"Error loading events: {e}")


# ==========================================
# OBJECTS / CLASSES / OOP
# ==========================================

# Base class representing a standard resource
class Resource:
    # Constructor method to initialize attributes
    def __init__(self, name, r_type, is_aval):
        self.name = name
        self.r_type = r_type
        self.is_aval = is_aval

    # Method to format and return the resource's information
    def get_info(self):
        # Using conditional operator (ternary) to set status string
        status = "Available" if self.is_aval else "Not available"
        # Using string manipulation (.upper()) and f-strings for formatting
        return f"[{self.r_type.upper()}] {self.name} - {status}"

# Subclass that inherits from the Resource class (Demonstrating Inheritance)
class Equipment(Resource):
    def __init__ (self, name, r_type, is_aval, condition):
        # Calling the parent class constructor using super()
        super().__init__(name, r_type, is_aval)
        # Adding a specific attribute for the subclass
        self.condition = condition
    
    # Overriding the parent's get_info method to include the condition attribute
    def get_info(self):
        status = "Available" if self.is_aval else "Not available"
        return f"[{self.r_type.upper()}] {self.name} (Condition: {self.condition}) - {status}"

# Class representing an Event
class Event:
    def __init__(self, title, date, time, duration):
        self.title = title
        self.date = date
        self.time = time
        # Type casting string to integer
        self.duration = int(duration)
        # Initializing an empty list to hold resource IDs assigned to this event
        self.resource_ids = []


# ==========================================
# MAIN PROGRAM LOGIC (CONDITIONALS AND LOOPS)
# ==========================================

def main():
    # Creating empty dictionaries to store resources and events
    resources_map = {} 
    events_map = {}

    # Loading existing data from files before starting the menu
    load_resources(resources_map)
    load_events(events_map)

    # Infinite while loop to keep the program running until the user exits
    while True:
        print("\n=== Resource & Event Management System ===")
        print("1 - Add resource")
        print("2 - Update resource")
        print("3 - Delete resource")
        print("4 - View resources")
        print("5 - Add event")
        print("6 - Update event")
        print("7 - Delete event")
        print("8 - View events")
        print("9 - Delete all resources")
        print("10 - Delete all events")
        print("11 - Delete all logs")
        print("12 - Exit")

        # Getting user input and removing any extra whitespace
        ch = input("What do you want to do? : ").strip()

        # Using if/elif/else conditional statements to route menu choices
        if ch == "1":
            r_id = input("Enter resource unique ID: ")
            name = input("Enter name: ")
            r_type = input("Enter type (e.g. standart, equipment): ")
            # Converting input to lowercase for easier comparison
            aval_input = input("Available? (1/yes or 0/no): ").lower()
            # Conditional expression to evaluate boolean availability
            is_aval = True if aval_input in ['1', 'yes', 'true'] else False

            # Nested conditional to instantiate either Equipment subclass or Resource base class
            if r_type.lower() == "equipment":
                condition = input("Enter condition (e.g., Good, Broken): ")
                resources_map[r_id] = Equipment(name, r_type, is_aval, condition)
            else:
                resources_map[r_id] = Resource(name, r_type, is_aval)
            
            print("Resource successfully added")
            log_action(f"Added resource: {r_id} ({name})")

        elif ch=="2":
            r_id = input("Enter the ID of the resource to update: ")

            # Checking if the key exists in the dictionary
            if r_id in resources_map:
                name = input("Enter new name: ")
                r_type = input("Enter new type: ")
                is_aval = input("Available? (1/0): ") == '1'
                # Updating the object in the dictionary
                resources_map[r_id] = Resource(name, r_type, is_aval)
                print("Resource successfully updated!")
                log_action(f"Updated resource: {r_id}")
            else:
                print("Resource not found!")
        
        elif ch == "3":
            r_id = input("Enter the ID of the resource to delete: ")

            if r_id in resources_map:
                # Using 'del' to remove an item from the dictionary
                del resources_map[r_id]
                print("Resource successfully deleted!")
                log_action(f"Deleted resource: {r_id}")
            else:
                print ("Resource not found!")

        elif ch == "4":
            print("\n----------Resource list----------")
            # Using a for loop to iterate through dictionary items (key-value pairs)
            for r_id, res in resources_map.items():
                print(f"ID: {r_id} | {res.get_info()}")
        
        elif ch == "5":
            e_id = input("Enter event unique ID: ")
            title = input("Enter event title: ")

            # Nested while loop to continuously ask for input until validation passes
            while True:
                date = input ("Enter event date (YYYY-MM-DD): ")
                if validate_date(date):
                    break # Exits the inner loop if regex validation is successful
                print("Invalid date format! Try again.")
            time = input("Enter event time: ")
            duration = input("Enter event duration (in minutes): ")

            # Creating the Event object
            new_event = Event(title, date, time, duration)

            print("Write resource ID (press -1 to finish): ")
            # Another nested loop for repeated list appending
            while True:
                rid = input("> ")
                if rid == "-1":
                    break

                # List manipulation: appending elements to the list
                new_event.resource_ids.append(rid)
            
            events_map[e_id] = new_event
            print("Event successfully added!")
            log_action(f"Added event: {e_id}")
        
        elif ch == "6":
            e_id = input("Enter the ID of the event to update: ")
            if e_id in events_map:
                print("------Enter new event details------")
                title = input("Enter new title: ")

                while True:
                    date = input("Enter new date (YYYY-MM-DD): ")
                    if validate_date(date):
                        break
                    print("Invalid date format! Try again.")
                time = input("Enter new time: ")
                duration = input("Enter new duration (in minutes): ")

                # Directly modifying the attributes of the existing object
                events_map[e_id].title = title
                events_map[e_id].date = date
                events_map[e_id].time = time
                events_map[e_id].duration = int(duration)

                print("Write new resource IDs (press -1 to finish): ")
                # List manipulation: clearing the existing list before adding new IDs
                events_map[e_id].resource_ids.clear()

                while True:
                    rid = input("> ")
                    if rid == "-1":
                        break
                    events_map[e_id].resource_ids.append(rid)
                    
                print("Event successfully updated!")
                log_action(f"Updated event: {e_id}")
            else:
                print("Event not found!")
        
        elif ch == "7":
            e_id = input("Enter the ID of the event to delete: ")
            if e_id in events_map:
                del events_map[e_id]
                print("Event successfully deleted!")
                log_action(f"Deleted event: {e_id}")
            else:
                print("Event not found!")

        elif ch == "8":
            print("\n-----------Event list----------")
            # Sorting the dictionary by keys to display them in alphabetical/numerical order
            sorted_events = sorted(events_map.items())

            for e_id, ev in sorted_events:
                print(f"\nEvent ID: {e_id}")
                print(f"Title: {ev.title} | Date: {ev.date} | Time: {ev.time} | Duration: {ev.duration}m")
                print("Assigned resources: ")

                # Iterating through the list of resource IDs attached to this event
                for rid in ev.resource_ids:
                    # Checking if the referenced resource ID actually exists in the resources dictionary
                    if rid in resources_map:
                        res = resources_map[rid]
                        print(f"  -> [{rid}] {res.name} (Type: {res.r_type}) - {'Avail' if res.is_aval else 'Not Avail'}")
                    else:
                        print(f"  -> [{rid}] (Resource deleted or missing)")
                
        elif ch == "9":
            yn = input("Delete all resources? (1 - YES; 0 - NO): ")
            if yn == "1":
                # Dictionary manipulation: removing all items from the dictionary
                resources_map.clear()
                print("Success! Your resources are deleted.")
                log_action("Deleted ALL resources")
        
        elif ch == "10":
            yn = input("Are you sure you want to delete all events? (1 - YES; 0 - NO): ")

            if yn == "1":
                events_map.clear()
                print("Success! Your events are deleted.")
                log_action("Deleted ALL events")

        elif ch == "11":
            yn = input("Are you sure you want to delete all logs? (1 - YES; 0 - NO): ")
            if yn == "1":
                try:
                    # Opening the file in 'w' (write) mode automatically erases all its existing content
                    with open("action_log.txt", "w", encoding = "utf-8") as file:
                        pass # 'pass' means do nothing inside the block; the file is just opened (cleared) and closed
                    print("Success! All logs have been deleted.")
                    log_action("Log file was cleared by the user.") # Writing the first line to the empty file
                except Exception as e:
                    print(f"Error clearing logs: {e}")
                    
        elif ch == "12":
            yn = input("Do you want to save changes? (1 - YES; 0 - NO): ")
            if yn == "1":
                # Calling file save functions before exiting
                save_resources(resources_map)
                save_events(events_map)
                print("Success! Changes saved.")
            else:
                print("Exited without saving.")
            # 'break' terminates the main while loop, ending the program
            break

        else:
            # Handles any invalid user input in the main menu
            print("Not implemented in this demo or invalid choice.")

# Standard Python entry point check.
# Ensures the main() function runs only if this script is executed directly (not imported as a module).
if __name__ == "__main__":
    main()