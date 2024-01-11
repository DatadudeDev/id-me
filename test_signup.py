import requests
import getpass
from datetime import datetime
import json

# API endpoint URL
api_url = 'http://127.0.0.1:4546/signup'

# Prompt for user data
data = {
    'firstName': input('Enter first name: '),
    'lastName': input('Enter last name: '),
    # Convert the DOB to a string in the format 'YYYY-MM-DD'
    'DOB': datetime.strptime(input('Enter Date of Birth (YYYY-MM-DD): '), '%Y-%m-%d').date().isoformat(),
    'Location': input('Enter location: '),
    'Career': input('Enter career: '),
    'hobbies': input('Enter hobbies (comma-separated): ').split(','),
    'joinDate': datetime.now().isoformat(),
}

# Prompt for social media handles
linkedin = input('Enter LinkedIn handle: ')
twitter = input('Enter Twitter handle: ')
meta = input('Enter Meta handle: ')
instagram = input('Enter Instagram handle: ')

# Add social media handles to data
data['socials'] = {
    'linkedin': linkedin,
    'twitter': twitter,
    'meta': meta,
    'instagram': instagram
}

# Continue prompting for the rest of the data
data['Description'] = input('Enter description: ')
data['Username'] = input('Enter username: ')
data['Password'] = getpass.getpass('Enter password: ')

# Send data to the API
response = requests.post(api_url, json=data)

# Print response
print(response.json())
