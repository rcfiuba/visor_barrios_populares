# PF_GIS
![example](https://user-images.githubusercontent.com/62706597/185153860-53c8b376-aacf-48fd-bc47-1c111162e447.png)

Simple salida gráfica que permite visualizar donde se encuentran los poligonos de barrios populares segun ReNaBaP.

LINK: https://rcfiuba-visor-barrios-populares-visor-qns2qj.streamlit.app/

## Instalación

Clona el repo

```bash
git clone https://github.com/rcfiuba/visor_barrios_populares.git
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

Para que se efectuen los cambios hay que pushear las modificaciones al git y automaticamente se actualiza el dashboard cuando se ingresa a la pagina principal.