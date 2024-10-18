import requests

def get_evaluation_id(session_id):
    # Define the URL for fetching evaluations and the session parameter
    url = "https://eventretrieval.one/api/v2/client/evaluation/list"
    params = {"session": session_id}

    try:
        # Send the GET request to retrieve evaluations
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        evaluations = response.json()

        # # Loop through the evaluations and print their details
        # for evaluation in evaluations:
        #     evaluation_id = evaluation.get("id")
        #     print(f"Evaluation ID: {evaluation_id}")

        # If you want to return the first evaluation ID for further use
        if evaluations:
            return evaluations[0].get("id")
        else:
            print("No evaluations found.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None