import requests
import getpass

def get_session_id(username, password):
    # Define the API URL and payload
    url = "https://eventretrieval.one/api/v2/login"
    payload = {
        "username": username,
        "password": password
    }

    try:
        # Send the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Get the sessionId from the response
        session_id = data.get("sessionId")
        if session_id:
            return session_id
        else:
            print("Session ID not found in the response.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

