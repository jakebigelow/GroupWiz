import os
import sys
import argparse
import requests
import json
import random
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
GoPhish_API = os.getenv('GoPhish_API')
auth_header = {"Authorization": f"Bearer {GoPhish_API}"}

HEADER_MAP = {
    "first_name": ["first_name","firstname","fname","First Name","first name","FirstName"],
    "last_name": ["last_name", "lastname","lname","Last Name","last name","LastName"],
    "email": ["email", "email_address","e-mail","Email Address"],
    "position:": ["Title", "title", "Position", "position"]
}

def find_header(headers, possible_names, required=False):
    for name in possible_names:
        if name.lower() in [h.lower() for h in headers]:
            return name
    if required:
        raise ValueError(f"Missing required header. Expected one of {possible_names}")
    return None

def process_file(file_path, delimiter):
    with open(file_path,"r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        
        headers = reader.fieldnames
        print(f"Detected headers: {headers}")

        email_header = find_header(headers, HEADER_MAP['email'], required=True)
        first_name_header = find_header(headers, HEADER_MAP['first_name'])
        last_name_header = find_header(headers, HEADER_MAP['last_name'])
        position_header = find_header(headers, HEADER_MAP['position'])

        contacts =[]
        for i, row in enumerate(reader):
            try:
                contact = {
                    "email": row[email_header].strip(),
                    "first_name": row[first_name_header].strip() if first_name_header else "",
                    "last_name": row[last_name_header].strip() if last_name_header else "",
                    "position": row[position_header].strip() if position_header else "" 
                }
                contacts.append(contact)
            except KeyError as e:
                print(f"Missing key on line {i+2}: {e}")
            except Exception as e:
                print(f"Error on line {i+2}: {e}")
        return contacts

def get_contacts(contacts, randomize, target_count=None):
    if randomize:
        if target_count is None:
            target_count = random.randint(1, len(contacts))
        target_count = min(target_count, len(contacts))
        return random.sample(contacts, target_count)
    return contacts

def create_group(api_url, group_name, contacts):
    url = f"https://{api_url}:3333/api/groups/"

    target_group ={
        "name": f"{group_name}",
        "targets": contacts
    }
 
    json_data = json.dumps(target_group, indent=4)
    response = requests.post(url, headers=auth_header, data=json_data)

    if response.status_code == 201:
        print(f"Group created successfully! Group created with the name: {group_name}")
    elif response.status_code == 409:
        print(f"The group {group_name} already exists. Please rerun the command with a new Group Name")
    else:
        print("An error occured when creating the group please review your command and try again.")

def check_groups(api_url):
    url = f"https://{api_url}:3333/api/groups"

    response = requests.get(url, headers=auth_header)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch groups: {response.status_code} - {response.text}")
    
    groups = response.json()

    print("Existing Groups:")
    for group in groups:
        group_id = group.get("id")
        group_name = group.get("name")
        group_mod_date = group.get("modified_date")
        targets = group.get("targets", [])

        unique_targets = {target.get("email") for target in targets if target.get("email")}
        unique_count = len(unique_targets)
        
        print("----")
        print(f"id:{group_id}")
        print(f"Group Name: {group_name}")
        print(f"Last Modified: {group_mod_date}")
        print(f"Number of Unique Targets: {unique_count}")
    print("----")

def check_group_details(api_url, group_name):
    url = f"https://{api_url}:3333/api/groups"
    target_group = group_name

    print(f"Details for target group: {target_group}")
    response = requests.get(url, headers=auth_header)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch groups: {response.status_code} - {response.text}")

    groups = response.json()
    
    matching_group = next((group for group in groups if group.get("name") == target_group), None)

    if not matching_group:
        print(f"Group '{target_group}' not found")
        return
    
    group_id = matching_group.get("id")
    targets = matching_group.get("targets",[])
    mod_date = matching_group.get("modified_date")

    print("----")
    print(f"id:{group_id}")
    print(f"Group Name: {target_group}")
    print(f"Last Modified: {mod_date}")
    print("Targets:")
    print(json.dumps(targets, indent=4, sort_keys=True))
    print("----")

def contact_search(api_url, first_name=None, last_name=None, email=None):
    if not (first_name and last_name) and not email:
        print("You must specifiy either a Frist Name/Last Name or an Email addres.")
        return
    url = f"https://{api_url}:3333/api/groups/"
    
    response = requests.get(url, headers=auth_header)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch groups: {response.status_code} - {response.text}")

    groups = response.json()
    found_matches = False

    if (first_name and last_name):
        print(f"Searching groups for: {first_name} {last_name}")
    else:
        print(f"Searching groups for: {email}")
    
    for group in groups:
        group_name = group.get("name")
        group_id = group.get("id")
        targets = group.get("targets", [])

        for target in targets:
            if email and target.get("email") == email:
                print(f"Found target in Group: {group_name} (ID: {group_id})")
                print(f"- Email: {target.get('email')}, FristName: {target.get('first_name')} Last Name: {target.get('last_name')}")
                found_matches = True
            elif first_name and last_name and target.get("first_name") == first_name and target.get("last_name") == last_name:
                print(f"Found target in Group: {group_name} (ID: {group_id})")
                print(f"- Email: {target.get('email')}, Frist Name: {target.get('first_name')}, Last Name: {target.get('last_name')}")
                found_matches = True
    if not found_matches:
        print("No contact matching the target given.")

def delete_group(api_url, group_id):
    url = f"https://{api_url}:3333/api/groups/{group_id}"

    response = requests.delete(url, headers=auth_header)
    if response.status_code == 200:
        print(f"Group {group_id} has been successfully delete.")
    elif response.status_code == 404:
        print(f"The group {group_id} does not exist on this instance. To list the groups please use -l")
    else:
        raise Exception("An error has occred.")

    

def main():
    parser = argparse.ArgumentParser(description = 'This is a tool that will parse and upload a csv file to the given GoPhish instance')
    new_group = parser.add_mutually_exclusive_group(required=True)
    #Upload the a target list to a given GoPhish instance
    parser.add_argument('-u', type=str, required=True, help='The URL of the GoPhish instance. Example format: https://<your_domain>:3333')
    new_group.add_argument('-f', type=str, help='The path to the CSV file containing the target list')
    parser.add_argument('-n', type=str, help='The name of the Sending Group that either exists or would like to create on the GoPhish instance')

    #Optional tags that add / change the functionality of the application
    new_group.add_argument('-l', action="store_true", help="List exisiting sending groups instead of creating a new group.")
    parser.add_argument('-rand', action="store_true", help="Randmize the size of the target list that is used to create a new sending group.")
    parser.add_argument('-c', type=int, help="Specify the exact number of targets to select (used with -rand)")
    parser.add_argument('-d', type=str, default=",", help="The type of delmiter that the file uses to seperate rows. Defualt is: , ")

    #Functionality for the searching of contacts.
    parser.add_argument('-e', type=str, help="Email address of the contact search for in existing groups (used with -l)")
    parser.add_argument('-fn', type=str, help="First name of the contact to search for in existing groups (used with -l)")
    parser.add_argument('-ln', type=str, help="Last name of the contact to search for in existing groups (used with -l)")

    #Deletes an exisiting group
    new_group.add_argument('--delete', type=int, help="Deletes a group by its ID")

    args = parser.parse_args()

    try: 
        if args.l and args.n:
            check_group_details(args.u, args.n)
        elif args.l and (args.fn and args.ln or args.e):
            contact_search(args.u, first_name=args.fn, last_name=args.ln, email=args.e)
        elif args.l:
            check_groups(args.u)
        elif args.f:
            contacts = process_file(args.f, args.d)
            selected_contacts = get_contacts(contacts, args.rand, args.c)
            group_name = args.n
            print(f"Creating group: {group_name}")
            create_group(args.u, group_name, selected_contacts)
        elif args.delete:
            delete_group(args.u, args.delete)
        else:
            print("Error: You must specify either a file using -f or use -l to list existing groups")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
