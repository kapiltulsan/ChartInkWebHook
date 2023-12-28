import json
import requests

def lambda_handler(event, context):
    # Extract data from the incoming JSON
    stocks = event.get('stocks', '').split(',')
    trigger_prices = list(map(float, event.get('trigger_prices', '').split(',')))
    triggered_at = event.get('triggered_at', '')
    scan_name = event.get('scan_name', '')
    scan_url = event.get('scan_url', '')
    alert_name = event.get('alert_name', '')
    webhook_url = event.get('webhook_url', '')

    # Process the data or perform any desired logic
    # For example, you can construct a message to be sent in the webhook
    message = f"Alert: {alert_name}\nScan: {scan_name}\nTriggered at: {triggered_at}\n\n"

    for stock, price in zip(stocks, trigger_prices):
        message += f"{stock}: {price}\n"

    # Send the message to the specified webhook URL
    # if webhook_url:
    #     send_webhook(message, webhook_url)

    return {
        'statusCode': 200,
        'body': json.dumps('Alert processed successfully!')
    }

def send_webhook(message, webhook_url):
    # Send a POST request to the webhook URL with the constructed message
    payload = {'text': message}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to send webhook. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # For local testing
    test_event = {
        "stocks": "SEPOWER,ASTEC,EDUCOMP,KSERASERA,IOLCP,GUJAPOLLO,EMCO",
        "trigger_prices": "3.75,541.8,2.1,0.2,329.6,166.8,1.25",
        "triggered_at": "2:34 pm",
        "scan_name": "Short term breakouts",
        "scan_url": "short-term-breakouts",
        "alert_name": "Alert for Short term breakouts",
        "webhook_url": "http://your-web-hook-url.com"
    }

    lambda_handler(test_event, None)
