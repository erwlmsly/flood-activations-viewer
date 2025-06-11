import gspread
import pandas as pd
import streamlit as st


def fetch_google_sheet_data(sheet_url):
    # Authenticate and open the sheet
    creds = st.secrets["google_sheets"]
    gc = gspread.service_account_from_dict(creds)
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Get the first sheet

    # Convert sheet data to a Pandas DataFrame
    return pd.DataFrame(worksheet.get_all_records())
