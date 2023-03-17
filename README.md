# PF_GIS
![example](https://user-images.githubusercontent.com/62706597/185153860-53c8b376-aacf-48fd-bc47-1c111162e447.png)

Simple salida gráfica que permite visualizar donde se encuentran los puntos fijos materializados en el terreno. Los puntos y poligonos se representan en el sistema WGS84.

LINK: https://share.streamlit.io/rcammi/pf_gis/main/dashboard.py

## Instalación

Clona el repo

```bash
git clone https://github.com/rcammi/PF_GIS.git
```

### Dependencias y environment:

cd a la carpeta donde se encuentra el dashboard

```bash
virtualenv -p python3.10 env3
. env3/Script/activate
pip install -r requirements.txt
```

### Construir y correr la aplicación localmente

cd a la carpeta donde se encuentra el dashboard

```bash
streamlit run dashboard.py
```

Luego visitar a visitar http://localhost:8501 en tu browser.

## Deployment

El deployment se hace sobre la nube de Streamlit. Ya esta todo armado. Si queres ver más informacion ir al siguiente link:

https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app

Para que se efectuen los cambios, por ejemplo, actualizaciones del csv file, hay que pushear las modificaciones al git y automaticamente se actualiza el dashboard cuando se ingresa a la pagina principal.

## Como actualizar el dashboard

Esta todo armado para que solo haya que editar el archivo csv file y pushearlo al repo. El archivo dashboard.py contiene una función que abre el archivo csv y lo transforma en un shapefile, que después es el que utiliza para mapear. 

Es indispensable que el archivo csv se llame PF_mugica.csv y debe estar guardado en la dir: "/datos_GIS/shapefiles/".

Eejemplo de formato de archivo csv: https://github.com/rcammi/PF_GIS/blob/main/datos_GIS/PF_mugica.csv
