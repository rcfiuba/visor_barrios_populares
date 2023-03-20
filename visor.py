import os

import streamlit as st

import geopandas as gpd

from streamlit_folium import folium_static
from folium.plugins import MousePosition
import folium

# set page layout configs
st.set_page_config(
    page_title='Barrios Populares CABA',
    layout='wide',
    page_icon=':rocket:'
    )

st.title("Barrios Populares CABA")
    
# get path
path = os.getcwd()
data_path = str(path) + "/datos_GIS/shapefiles/poligono_barrios_populares_renabap.gpkg"

# open files
barrios_pop = gpd.read_file(data_path)
    
# Create a list to store the links
links = [f"<a href='{link}' target='_blank'>{link}</a>" if link != '-' else '-' for link in barrios_pop['Link_Ley']]

# Add the links to the dataframe as a new column
barrios_pop['Link_Ley'] = links

# set WGS84 as crs
barrios_pop_WGS84 = barrios_pop.to_crs(epsg=4326)

# set initial zoom
start_zoom = 12

# open map
m = folium.Map(location=[-34.62, -58.38], tiles='OpenStreetMap', zoom_start=start_zoom, control_scale=True) # 

# Add the full-screen control to the map
m.add_child(folium.plugins.Fullscreen())

# set folium feature
barrios_pop_bordes = folium.FeatureGroup(name='Barrios populares RENABAP', show=True)

fields = ['NOMBRE','Localidad','Departamen','SECCIÓN','MANZANA','Superficie','SIT_DOMINI','LEYES','Link_Ley','VIVI_AROX','Familias','CREACIÓN','TIPO','GAS','AGUA','CLOACAS','ELECTRICID']
aliases = ['NOMBRE','Localidad','Departamento','SECCIÓN','MANZANA','Superficie [m2]','SITUACIÓN DOMINIAL','LEYES','Link Ley','VIVIENDAS APROX.','Familias','CREACIÓN','TIPO','GAS','AGUA','CLOACAS','ELECTRICIDAD']

# add geojson data to map
folium.GeoJson(
    data=barrios_pop_WGS84, 
    popup=folium.features.GeoJsonPopup(
        fields=fields,
        aliases=[s.upper() for s in aliases],
        labels=True,
        localize=True,
        max_width=500,
        style="font-size:12px",
    ),
).add_to(barrios_pop_bordes)

# add base layers to map
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
tile_url = 'http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}'
attribution = 'google satellite'
folium.TileLayer(tile_url, name=attribution, attr=attribution).add_to(m)

# add the GeoJson layer to the map
barrios_pop_bordes.add_to(m)

# add the tile layers to the layer control
folium.LayerControl(position='topright',
                    collapsed=True 
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