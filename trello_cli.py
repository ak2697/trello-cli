import requests
import argparse

BASE_URL = "https://api.trello.com/1"

def get_board_id(api_key, token, board_name):
    url = f"{BASE_URL}/members/me/boards"
    query = {
        'key': api_key,
        'token': token
    }
    response = requests.get(url, params=query)
    response.raise_for_status()
    boards = response.json()
    for board in boards:
        if board['name'] == board_name:
            return board['id']
    raise ValueError(f"Board '{board_name}' not found.")

def get_list_id(api_key, token, board_id, list_name):
    url = f"{BASE_URL}/boards/{board_id}/lists"
    query = {
        'key': api_key,
        'token': token
    }
    response = requests.get(url, params=query)
    response.raise_for_status()
    lists = response.json()
    for lst in lists:
        if lst['name'] == list_name:
            return lst['id']
    raise ValueError(f"List '{list_name}' not found on board '{board_id}'.")

def get_label_ids(api_key, token, board_id, label_names):
    url = f"{BASE_URL}/boards/{board_id}/labels"
    query = {
        'key': api_key,
        'token': token
    }
    response = requests.get(url, params=query)
    response.raise_for_status()
    labels = response.json()
    label_ids = []
    label_names_set = set(label_names.split(","))
    for label in labels:
        if label['name'] in label_names_set:
            label_ids.append(label['id'])
    if not label_ids:
        raise ValueError(f"Labels '{label_names}' not found on board '{board_id}'.")
    return ",".join(label_ids)

def add_card(api_key, token, list_id, card_name, labels, comment):
    url = f"{BASE_URL}/cards"
    query = {
        'key': api_key,
        'token': token,
        'idList': list_id,
        'name': card_name,
        'idLabels': labels
    }
    response = requests.post(url, params=query)
    response.raise_for_status()
    card = response.json()

    if comment:
        url = f"{BASE_URL}/cards/{card['id']}/actions/comments"
        query = {
            'key': api_key,
            'token': token,
            'text': comment
        }
        response = requests.post(url, params=query)
        response.raise_for_status()

    print(f"Card '{card_name}' added successfully with labels '{labels}' and comment '{comment}'.")

def main():
    parser = argparse.ArgumentParser(description="Add a card to a Trello board.")
    parser.add_argument('--api_key', required=True, help="Trello API Key")
    parser.add_argument('--token', required=True, help="Trello Token")
    parser.add_argument('--board_name', required=True, help="Trello Board Name")
    parser.add_argument('--list_name', required=True, help="Trello List Name")
    parser.add_argument('--card_name', required=True, help="Name of the card")
    parser.add_argument('--labels', help="Comma-separated list of label names")
    parser.add_argument('--comment', help="Comment to add to the card")

    args = parser.parse_args()

    try:
        board_id = get_board_id(args.api_key, args.token, args.board_name)
        list_id = get_list_id(args.api_key, args.token, board_id, args.list_name)
        labels = get_label_ids(args.api_key, args.token, board_id, args.labels) if args.labels else ""
        add_card(args.api_key, args.token, list_id, args.card_name, labels, args.comment)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
