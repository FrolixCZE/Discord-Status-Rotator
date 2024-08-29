import requests
import time
import yaml

# Function to split text into chunks of max_length
def split_text(text, max_length=40):
    # Splits text into chunks, but only if the text length is within the limit
    return [text[i:i + max_length] for i in range(0, len(text), max_length)] if len(text) <= max_length else []

def load_config():
    # Load the config from config.yaml
    with open('config.yaml', 'r') as config_file:
        return yaml.safe_load(config_file)

def change_status(status_text):
    # Check if the status text length exceeds the limit
    if len(status_text) > 40:
        print(f"Skipped status '{status_text}' (exceeds 40 characters)")
        return

    full_status = f"{status_text} {url_to_append}"
    payload = {
        "custom_status": {
            "text": status_text
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Status changed to: '{status_text}'")
    else:
        print(f"Failed to change status. Response: {response.status_code}, Error: {response.text} | https://dsc.gg/rezont00ls")
    time.sleep(interval)

print("Discord Status Rotator by Frolix. https://github.com/FrolixCZE")
print("")

while True:
    # Load the config from config.yaml
    config = load_config()

    DISCORD_TOKEN = config['discord_token']
    statuses = config['statuses']
    interval = config.get('interval', 3)  # Default to 3 seconds if not set
    url = "https://discord.com/api/v9/users/@me/settings"

    headers = {
        "Authorization": DISCORD_TOKEN,
        "Content-Type": "application/json"
    }

    # Filter out statuses that are too long
    valid_statuses = [status for status in statuses if len(status) <= 40]
    invalid_statuses = [status for status in statuses if len(status) > 40]

    if invalid_statuses:
        print(f"Ignoring statuses: {invalid_statuses} Due to the texts having more than 40 characters.")
        print("")
        time.sleep(2.5)

    if not valid_statuses:
        print("No valid statuses available.")
        break

    for status in valid_statuses:
        change_status(status)
        time.sleep(interval)
