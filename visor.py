from pathlib import Path
from re import M

from click import style

import streamlit as st
import streamlit_authenticator as stauth

#import warnings
from layout import set_page_container_style

import geopandas as gpd
import shapefile
import csv
#from shapely.geometry import Point

from streamlit_folium import folium_static
from streamlit_folium import st_folium
from folium.plugins import MousePosition
import folium

# set page layout configs
st.set_page_config(
    page_title='Encuentra tus puntos fijos',
    layout='wide',
    page_icon=':rocket:'
    )

st.title("Barrios Populares CABA")
    
# get path
path = Path.cwd()

# open files
barrios_pop = gpd.read_file(str(path) + "/datos_GIS/shapefiles/poligono_barrios_populares_renabap.gpkg")

# set WGS84 as crs
barrios_pop_WGS84 = barrios_pop.to_crs(epsg=4326)

start_zoom = 12

# open map
m = folium.Map(location=[-34.62, -58.38], tiles='OpenStreetMap', zoom_start=start_zoom, control_scale=True) 

# Add the full-screen control to the map
m.add_child(folium.plugins.Fullscreen())

barrios_pop_bordes = folium.GeoJson(
    data=barrios_pop_WGS84, 
    name='Barrios populares RENABAP', 
    show=True  # This parameter will show the GeoJson layer by default
)   

fields = ['NOMBRE','Localidad','Departamen','SECCIÓN','MANZANA','Superficie','SIT_DOMINI','LEYES','Link_Ley','VIVI_AROX','Familias','CREACIÓN','TIPO','GAS','AGUA','CLOACAS','ELECTRICID']
folium.features.GeoJsonPopup(
        fields=fields,
        aliases=[s.upper() for s in fields],
        labels=True,
        localize=True,
        max_width=500,
    ).add_to(barrios_pop_bordes)

# add base layers to map
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)

# add the GeoJson layer to the map
barrios_pop_bordes.add_to(m)

# add the tile layers to the layer control
folium.LayerControl(position='topright', 
                    ).add_to(m)
    
# Create a MousePosition plugin and add it to the map
mp = MousePosition(position='bottomright', separator=' | ')
mp.add_to(m)

# Define a function that resets the zoom level to the starting value
def reset_zoom():
    m.fit_bounds(m.get_bounds())

# Create a Streamlit button that calls the reset_zoom() function when clicked
st.button("Reset Zoom", on_click=reset_zoom)

# show static folium map on streamlit app
folium_static(m, width=1800, height=800)