import json
import os
import openai
import requests
import time
import logging
from recetas.templates_recetas import plantilla_receta_html

from dotenv import load_dotenv


import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")

cliente = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
cliente_img = openai.Client(
    api_key = os.getenv("TOGETHER_API_KEY"),
    base_url= os.getenv("TOGETHER_API_URL")
    )

SYSTEM = """
Eres un chef experto en cocina internacional,
solo respondes preguntas relacionadas con recetas de cocina.
las respuestas dalas en en json, con los siguientes campos:
- "titulo": Titulo del plato
- "descripcion": Descropcion del plato no mas de 2 parrafos.
- "ingredientes": una lista de ingredientes necesarios con emoticones en lo posible
- "pasos": una lista de pasos a seguir
- "Prompt" : un jsson de 3 prompts para generar imagenes ilustrativas
  - "imagen_plato" : "prompt del plato con detalles del mismo"
  - "imagen_ingredientes" : "prompt para la lista de ingredientes"
  - "imagen_pasos" : "prompt para los pasos a seguir una sola imagen la mas relevante del proceso"
- "pregunta indevida" : Booleano Verdadeo o falso
"""

CARPETA_IMAGENES = os.path.join("static", "recetas", "img")
CARPETA_HTMLS = os.path.join("templates", "recetas")

def imagenes(prompt, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response = cliente_img.images.generate(
        prompt = prompt,
        model  = "black-forest-labs/FLUX.1-schnell-Free",
        n      = 1,
    )
    url = response.data[0].url
    img_data = requests.get(url).content
    with open(path, 'wb') as handler:
        handler.write(img_data)

def consulta(pregunta):
    response     = cliente.chat.completions.create(
        model    = "gpt-4o-mini",
        messages = [
            {
            "role": "system",
            "content": SYSTEM
        },
            {
            "role": "user",
            "content": f"{pregunta}"
        }
            ],
        response_format= { "type": "json_object" }    
    )
    datos = json.loads(response.choices[0].message.content)
    
    return datos

def crear_receta_con_ia(pregunta):
    datos = consulta(pregunta)
    # print("Datos obtenidos de la IA:")
    # print(json.dumps(datos, indent=4, ensure_ascii=False))
    if datos.get("pregunta indevida", False):
        return None  # O manejar error

    # titulo    = datos["titulo"].replace(" ", "_").lower()
    # url_plato = os.path.join(CARPETA_IMAGENES, f"{titulo}.png")
    # url_ingredientes = os.path.join(CARPETA_IMAGENES, f"{titulo}_ingredientes.png")
    # url_pasos = os.path.join(CARPETA_IMAGENES, f"{titulo}_pasos.png")

    titulo = datos["titulo"].replace(" ", "_").lower()

    nombre_plato = f"{titulo}.png"
    nombre_ingredientes = f"{titulo}_ingredientes.png"
    nombre_pasos = f"{titulo}_pasos.png"

    ruta_plato = os.path.join(CARPETA_IMAGENES, nombre_plato)
    ruta_ingredientes = os.path.join(CARPETA_IMAGENES, nombre_ingredientes)
    ruta_pasos = os.path.join(CARPETA_IMAGENES, nombre_pasos)

    logger.info("Generando imagenes...")
    logger.info(f"Generando imagen para el plato: {ruta_plato}")
    imagenes(datos["Prompt"]["imagen_plato"], ruta_plato)
    logger.info("OK")
    time.sleep(60)  # Esperar un minuto para evitar posibles límites de tasa
    logger.info(f"Generando imagen para los ingredientes: {ruta_ingredientes}")
    imagenes(datos["Prompt"]["imagen_ingredientes"], ruta_ingredientes)
    logger.info("OK")
    time.sleep(60)  # Esperar un minuto para evitar posibles límites de tasa
    logger.info(f"Generando imagen para los pasos: {ruta_pasos}")
    imagenes(datos["Prompt"]["imagen_pasos"], ruta_pasos)
    logger.info("OK")

    # Generar HTML y guardar en templates/recetas/
    nombre_html = f"{titulo}.html"
    ruta_html = os.path.join(CARPETA_HTMLS, nombre_html)
    logger.info("Generando HTML...")
    logger.info(f"Ruta HTML: {ruta_html}")
    html = plantilla_receta_html(
        datos["titulo"],
        datos["descripcion"],
        datos["ingredientes"],
        datos["pasos"],
        f"/{ruta_plato}",
        f"/{ruta_ingredientes}",
        f"/{ruta_pasos}"
    )
    os.makedirs(os.path.dirname(ruta_html), exist_ok=True)
    with open(ruta_html, "w", encoding="utf-8") as f:
       f.write(html)
    logger.info("OK")
    return ruta_html
