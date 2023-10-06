import gspread
import os
import google.auth 
import time
from twilio.rest import Client 
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up Google Sheets API
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
credentials = service_account.Credentials.from_service_account_file(
    'impactful-hawk-401006-13c9a65db6ff.json', scopes=scopes
)

client = gspread.authorize(credentials)
# spreadsheet = client.open('1VbWrt3tgdCc-MXk0FqOhng53Evcpzfqcj6p12tkYa-g')
# Build the Google Sheets API service
service = build('sheets', 'v4', credentials=credentials)
spreadsheet = service.spreadsheets()
result = spreadsheet.values().get(spreadsheetId="1VbWrt3tgdCc-MXk0FqOhng53Evcpzfqcj6p12tkYa-g",
                                    range="Sheet1!A1:D11").execute()




# Set up WhatsApp API
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
client = Client(account_sid, auth_token)


# Function to post messages and pictures to WhatsApp
# Function to post messages and pictures to WhatsApp
def post_to_whatsapp(row):
    if len(row) >= 2:
        message = row[0]
        media_url = row[3]

        try:
            # Send the message and media to the WhatsApp group
            # Replace with your WhatsApp API library's method for sending messages and media
            message = client.messages.create(
                to='whatsapp:+2348131542720',
                from_='whatsapp:+14155238886',
                body=message,
                media_url=media_url
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {e}")


# Main function to check for new rows and post to WhatsApp
def main():
    last_row_processed = 1  # Start from the second row to avoid processing the first row
    print(last_row_processed)

    while True:
        try:
            # Get the data from the Google Sheet in every iteration
            result = spreadsheet.values().get(spreadsheetId="1VbWrt3tgdCc-MXk0FqOhng53Evcpzfqcj6p12tkYa-g", 
                                              range="Sheet1!A1:D11").execute()
            values = result.get('values', [])

            if last_row_processed < len(values):
                row = values[last_row_processed]
                print("Processing new row:")
                print(row)
                post_to_whatsapp(row)
                last_row_processed += 1
            else:
                print("No new data found in Google Sheet. Last row processed:", last_row_processed)

        except Exception as e:
            print("Error in main loop:", e)

        # Sleep for a while to avoid constant checking
        print("Sleeping for 60 seconds...")
        time.sleep(60)  # Sleep for 60 seconds

if __name__ == '__main__':
    main()
