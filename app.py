from typing import List

import streamlit as st
from streamlit.components.v1 import html

from utils.folium_map import generate_map
from utils.google_sheets import fetch_google_sheet_data

st.title("Expected Flood Activations")


# Cache the data fetching function
@st.cache_data
def get_cached_google_sheet_data(sheet_url):
    return fetch_google_sheet_data(sheet_url)


# Fetch data from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1n7-vsmqASOU6lTc9GVB6Gl4yWA19BC7f60CqT3VI-8k"
data = get_cached_google_sheet_data(sheet_url)

# Dropdown to select the month
month: List[str] | str = st.multiselect("Select a month or months:", data.columns[2:])
print(month)

# Generate and display the map
map = generate_map(data, month)
map_html = map._repr_html_()

html(map_html, height=1200, width=1200)  # Embed the map in Streamlit
