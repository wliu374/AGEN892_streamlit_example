import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype

# 📌 Load your shapefile (adjust this path to your actual file)
@st.cache_data
def load_data():
    gdf = gpd.read_file("/content/drive/MyDrive/Colab Notebooks/Lab9_Data/Lab9_Grower.shp")
    return gdf

gdf = load_data()

# 📌 Convert datetime columns to strings
for col in gdf.columns:
    if col == gdf.geometry.name:
        continue
    if is_datetime64_any_dtype(gdf[col]):
        gdf[col] = gdf[col].astype(str)

# 📌 Get centroid of first polygon for initial map view
centroid = gdf.geometry.centroid.iloc[0]
center_latlon = [centroid.y, centroid.x]

# 📌 Create the folium map (avoid using `map` as variable name)
folium_map = folium.Map(location=center_latlon, zoom_start=15, width="100%")

# 📌 Add satellite basemap
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite'
).add_to(folium_map)

# 📌 Add GeoJson layer
folium.GeoJson(
    gdf.to_json(),
    name="Grower Polygon",
    marker=folium.Circle(
        radius=4,
        fill_color="red",
        fill_opacity=0.4,
        color="black",
        weight=1
    )
).add_to(folium_map)

# 📌 Display the map in Streamlit
st.title("Folium Map in Streamlit")
st_data = st_folium(folium_map, width=1000, height=600)
