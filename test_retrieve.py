import requests

def get_user_data(username, token):
    url = f'http://127.0.0.1:4546/id/{username}:{token}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Failed to retrieve data, status code {response.status_code}'}

if __name__ == '__main__':
    username = 'datadudedev'  # Replace this with the actual username
    token = '12321'    # Replace this with the actual token
    user_data = get_user_data(username, token)
    print(user_data)

 