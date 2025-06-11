import gspread
import pandas as pd


def fetch_google_sheet_data(sheet_url):
    # Authenticate and open the sheet
    gc = gspread.service_account(
        filename=r"C:\e\24\_prj\solution-delivery-development\meteorology_targeting\flood_seasonality_app\creds.json"
    )
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Get the first sheet

    # Convert sheet data to a Pandas DataFrame
    data = pd.DataFrame(worksheet.get_all_records())
    return data
