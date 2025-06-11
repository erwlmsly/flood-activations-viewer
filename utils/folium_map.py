from json import load
from typing import List

from branca.colormap import LinearColormap
from folium import GeoJson, Map
from folium.plugins import Fullscreen
from pandas import to_numeric


def generate_map(
    data, month: str | List[str], geojson_path: str = "data/countries.geojson"
):
    # if month has been selected
    if month:
        if isinstance(month, list):
            # Create a new column in the DataFrame that sums the values for the selected months
            data["Total"] = data.loc[:, month].sum(axis=1)
            month = "Total"  # Use the new column for visualization

        # Filter data for the selected month
        filtered_data = data[["Country", month]]

        # Ensure the column contains numeric values
        filtered_data[month] = to_numeric(filtered_data[month], errors="coerce")

        # Create a map centered on the world
        m = Map(location=[20, 0], zoom_start=2, max_bounds=True)

        # allow full screen mode
        Fullscreen().add_to(m)

        # Load GeoJSON data
        with open(geojson_path, "r") as f:
            geojson_data = load(f)

        # Determine the range of values for the selected month
        min_value = filtered_data[month].min()
        max_value = filtered_data[month].max()

        if min_value == max_value:
            min_value -= 1
            max_value += 1

        # Create a green-to-red colormap
        colormap = LinearColormap(
            ["green", "yellow", "red"], vmin=min_value, vmax=max_value
        )
        colormap.caption = "Forecasted Activations"  # Add a caption for the legend

        # Add country polygons to the map
        for feature in geojson_data["features"]:
            country_name = feature["properties"][
                "name"
            ]  # Adjust based on GeoJSON properties
            geometry = feature["geometry"]

            # Check if the country exists in the filtered data
            if country_name in filtered_data["Country"].values:
                value = filtered_data.loc[
                    filtered_data["Country"] == country_name, month
                ].values[0]

                GeoJson(
                    geometry,
                    style_function=lambda x, value=value: {
                        "fillColor": colormap(value),
                        # "color": "black",
                        "weight": 0,
                        "fillOpacity": 0.8,
                    },
                    tooltip=f"{country_name}: {round(value, 1)} Activations expected",
                ).add_to(m)

        # Add the colormap legend to the map
        colormap.add_to(m)

        return m
    return None
