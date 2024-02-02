import os
import csv
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json


def get_service():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if creds_json is None:
        raise Exception("Google credentials not found")

    creds_info = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_info)
    service = build("sheets", "v4", credentials=creds)
    return service


def update_sheet(service, sheet_id, range_name, values):
    sheet = service.spreadsheets()
    body = {"values": values}
    result = (
        sheet.values()
        .update(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")


def read_csv_data(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    return data


SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
RANGE_NAME = "Sheet1"
CSV_FILE_PATH = "data/contributors.csv"

service = get_service()
csv_data = read_csv_data(CSV_FILE_PATH)
update_sheet(service, SHEET_ID, RANGE_NAME, csv_data)

print("Google Sheet was successfully updated!")
