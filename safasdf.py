import json
import requests
import mysql.connector
from datetime import datetime

# Function to connect to MySQL database and insert data
def insert_data(stocks, trigger_prices, triggered_at, scan_name, scan_url, alert_name, webhook_url):
    # Connect to the MySQL database (replace the placeholders with your actual database details)
    conn = mysql.connector.connect(
        host='your_mysql_host',
        user='your_mysql_user',
        password='your_mysql_password',
        database='your_mysql_database'
    )
    cursor = conn.cursor()

    # Extract current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert data into the database
    cursor.execute("""
        INSERT INTO your_table (stocks, trigger_prices, triggered_at, scan_name, scan_url, alert_name, webhook_url, datetime_column, flag_column)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (','.join(stocks), ','.join(map(str, trigger_prices)), triggered_at, scan_name, scan_url, alert_name, webhook_url, current_datetime, 1))

    # Commit the transaction and close the database connection
    conn.commit()
    conn.close()

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
        # Insert data into the MySQL database
        insert_data(stocks, trigger_prices, triggered_at, scan_name, scan_url, alert_name, webhook_url)


    # Send the message to the specified webhook URL
    # if webhook_url:
    #     send_webhook(message, webhook_url)


    return {
        'statusCode': 200,
        'body': json.dumps('Alert processed successfully and data inserted into the MySQL database!')
    }

# Rest of the code (send_webhook and __main__) remains unchanged
