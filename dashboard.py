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
import folium

#warnings.simplefilter(action="ignore", category=FutureWarning)

# set page layout configs
st.set_page_config(
    page_title='Encuentra tus puntos fijos',
    layout='wide',
    page_icon=':rocket:'
    )

set_page_container_style(
    max_width = 1100, max_width_100_percent = True,
    padding_top = 0, padding_right = 10, padding_left = 5, padding_bottom = 10
    )

st.markdown(
    f'''
    <style>
        .reportview-container .sidebar-content {{
        padding-top: {1}rem;
    }}
        .reportview-container .main .block-container {{
        padding-top: {1}rem;
        }}
    </style>
   ''', unsafe_allow_html=True)


# authorized users 
names = ['Agrimensura UPE']
usernames = ['agrimUPE']
passwords = ['1540']

# convert plain text to hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'pf_gis', 'agrimensura', cookie_expiry_days=7)

name, authentication_status, username = authenticator.login('Login','main')

# if authentication is passed
if authentication_status:

    authenticator.logout('Logout', 'main')
    st.write('Bienvenido *%s*' % (name))

    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    st.title("¿Donde están materializados los puntos fijos?")
    
    # get path
    path = Path.cwd()

    # open files
    manzanas = gpd.read_file(str(path) + "/datos_GIS/shapefiles/poligono_manzanas.gpkg")
    exterior = gpd.read_file(str(path) + "/datos_GIS/shapefiles/poligono_exterior.gpkg")

    # for every record there must be a corresponding geometry.
    def create_shapefile(shp_path, csv_path):
        """Creates a shapefile from a csv file and saves it on the shp_path determined.

        Parameters:
        -----------
            shp_path (str): path where to save shapefile.
            csv_path (str): path where csv file is saved.

        Returns:
        --------
            shapefile: a shapefile of points with csv coordinates in crs CABA 2019. 
        """
        puntosFijos = shapefile.Writer(shp_path, shapefile.POINT) 
        
        # create a point shapefile
        puntosFijos.autoBalance = 1

        # create the field names and data type for each.
        puntosFijos.field("ID", "C")
        puntosFijos.field("N", "F", 10, 4)
        puntosFijos.field("E", "F", 10, 4)
        puntosFijos.field("COTA", "F", 10, 4)
        puntosFijos.field("OBS", "C")
        puntosFijos.field("IMAGEN", "C", 70)
        puntosFijos.field("FECHA", "C")

        # open csv file with point data 
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            # skip header
            next(reader, None)
        
            #loop through each of the rows and assign the attributes to variables
            for row in reader:
                id = row[0]
                norte = row[1]
                este = row[2]
                cota = row[3]
                observacion = row[7]
                imagen = row[8]
                fecha = row[9]

                # create the point geometry
                puntosFijos.point(float(este),float(norte))

                # add attribute data
                puntosFijos.record(id, norte, este, cota, observacion, imagen, fecha)

        puntosFijos.close()

        return puntosFijos

    # create shapefile from csv file
    shp_path = str(path) + "/datos_GIS/shapefiles/PF_mugica"
    csv_path = str(path) + '/datos_GIS/PF_mugica.csv'
    puntosFijos = create_shapefile(shp_path, csv_path)

    # read new shapefile with point attributes
    puntosFijos = gpd.read_file(str(path) + '/datos_GIS/shapefiles/PF_mugica.shp')

    # set WGS84 as crs
    puntosFijos_WGS84 = puntosFijos.to_crs(epsg=4326)
    manzanas_WGS84 = manzanas.to_crs(epsg=4326)
    exterior_WGS84 = exterior.to_crs(epsg=4326)

    # open map
    m = folium.Map(location=[-34.582083, -58.379722], tiles='OpenStreetMap', zoom_start=15, control_scale=True)

    #puntosFijos = folium.GeoJson(data=puntosFijos_WGS84["geometry"], name='Puntos')
    manzanas_bordes = folium.GeoJson(data=manzanas_WGS84["geometry"], name='Poligonos manzanas')
    exterior_bordes = folium.GeoJson(data=exterior_WGS84["geometry"], name='Poligonos exterior')

    # add features to map
    #puntosFijos.add_to(m)
    manzanas_bordes.add_to(m)
    exterior_bordes.add_to(m)

    # parse points from the points shapefile with data to pop up.
    for point in puntosFijos_WGS84.index:
        name = puntosFijos_WGS84["ID"].iloc[point]
        coords =  (puntosFijos_WGS84["N"].iloc[point],  puntosFijos_WGS84["E"].iloc[point],  puntosFijos_WGS84["COTA"].iloc[point])
        fecha = puntosFijos_WGS84["FECHA"].iloc[point]
        obs = puntosFijos_WGS84["OBS"].iloc[point]

        # Define html inside marker pop-up
        if puntosFijos_WGS84["IMAGEN"].iloc[point] != None:
            website = puntosFijos_WGS84["IMAGEN"].iloc[point]   
            pop_html = folium.Html(
                            f"""
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 20px;">Punto {name}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">Fecha: {fecha}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">Coords en GK CABA 2019: {coords}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">Observaciones: {obs}</span></p>
                            <p style="text-align: center;"><a href={website} target="_blank" title="Imagen"><span style="font-family: Arial, serif; font-size: 15px;">Ir a la imagen</span></a></p>
                            """, script=True)
        else:
            website = 'No tiene imagen'
            pop_html = folium.Html(
                            f"""
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 20px;">Punto {name}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">Fecha: {fecha}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">Coords en GK CABA 2019: {coords}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">Observaciones: {obs}</span></p>
                            <p style="text-align: center;"><span style="font-family: Arial, serif; font-size: 15px;">{website}</span></p>
                            """, script=True)
        
        # Create pop-up with html content
        popup = folium.Popup(pop_html, max_width=700)
        custom_marker = folium.Marker(location=(puntosFijos_WGS84["geometry"].iloc[point].y, puntosFijos_WGS84["geometry"].iloc[point].x), tooltip=name, popup=popup)
        custom_marker.add_to(m)

    # show static folium map on streamlit app
    folium_static(m, width=1200, height=1000)   

# if authentication is not passed
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

# FOLLOW INST https://towardsdatascience.com/creating-interactive-maps-for-instagram-with-python-and-folium-68bc4691d075
