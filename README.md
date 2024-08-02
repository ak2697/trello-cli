# Trello CLI

This CLI program allows you to add a card to a specified Trello board list with labels and a comment. It uses the Trello API to perform the operations.

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)
- Trello API key and token

## Usage

### Example CLI Command

```bash
python trello_cli.py --api_key YOUR_API_KEY --token YOUR_TOKEN --board_name "Board Name" --list_name "List Name" --card_name "Card Name" --labels "Label1,Label2" --comment "This is a comment"
