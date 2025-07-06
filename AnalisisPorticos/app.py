import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'AnalisisPorticos')))

import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt
from Analizadores.analizador_portico_2D import analizar_portico
from Graficos.grafico import graficar_resultados # type: ignore
from PIL import Image

st.set_page_config(page_title="Análisis de Pórticos 2D", layout="wide")

st.title("🔍 Análisis de Pórticos 2D")
st.markdown("Sube tu archivo JSON con la estructura del pórtico.")
st.markdown("🎓 _Universidad Técnica Particular de Loja_")

# 👉 Redes personales o créditos
st.markdown("---")
st.markdown("📌 Desarrollado por Jordi Ocampo - Jhonatan Giron - Juan Chamba")
st.markdown("📧 Contacto: jordijavi2016@gmail.com")
st.markdown("📱 Instagram: [@jordiocamp8](https://instagram.com/jordiocamp8)")
st.markdown("💼 LinkedIn: [Jordi Ocampo](https://linkedin.com/in/jordiocamp8)")
st.markdown("---")

# 🔹 Ingreso manual de nodos
st.header("🔹 Ingreso manual de nodos")
n_nodos = st.number_input("Número de nodos", min_value=1, step=1)

nodos = []
for i in range(int(n_nodos)):
    st.subheader(f"Nodo {i+1}")
    x = st.number_input(f"Coordenada X del Nodo {i+1}", key=f"x_{i}")
    y = st.number_input(f"Coordenada Y del Nodo {i+1}", key=f"y_{i}")
    nodos.append({"id": f"N{i+1}", "x": x, "y": y})

if nodos:
    st.success("✅ Nodos ingresados:")
    st.json(nodos)

# 🔷 Ingreso manual de elementos
st.markdown("## 🔷 Ingreso manual de elementos")
num_elementos = st.number_input("Número de elementos", min_value=1, step=1)

elementos = []
for i in range(num_elementos):
    with st.expander(f"Elemento {i+1}"):
        nodo_inicio = st.text_input(f"Nodo de inicio del Elemento {i+1}", key=f"ni_{i}")
        nodo_fin = st.text_input(f"Nodo de fin del Elemento {i+1}", key=f"nf_{i}")
        area = st.number_input(f"Área (A) del Elemento {i+1} [m²]", min_value=0.0, format="%.3f", key=f"a_{i}")
        momento_inercia = st.number_input(f"Momento de inercia (I) del Elemento {i+1} [m⁴]", min_value=0.0, format="%.6f", key=f"i_{i}")
        modulo_elasticidad = st.number_input(f"Módulo de elasticidad (E) del Elemento {i+1} [Pa]", min_value=0.0, format="%.0f", key=f"e_{i}")

        elementos.append({
            "id": f"E{i+1}",
            "nodo_inicio": nodo_inicio,
            "nodo_fin": nodo_fin,
            "A": area,
            "I": momento_inercia,
            "E": modulo_elasticidad
        })

if elementos:
    st.success("✅ Elementos ingresados:")
    st.json(elementos)

# 🔷 Ingreso de apoyos
st.markdown("### 🔷 Ingreso de apoyos (condiciones de frontera)")
num_apoyos = st.number_input("Número de apoyos", min_value=0, step=1)

apoyos = []
for i in range(num_apoyos):
    with st.expander(f"Apoyo en Nodo {i+1}"):
        nodo = st.text_input(f"ID del nodo con apoyo {i+1}", key=f"nodo_apoyo_{i}")
        dx = st.checkbox("Restringir desplazamiento en X", key=f"dx_{i}")
        dy = st.checkbox("Restringir desplazamiento en Y", key=f"dy_{i}")
        rotacion = st.checkbox("Restringir rotación", key=f"rot_{i}")
        apoyos.append({
            "nodo": nodo,
            "dx": dx,
            "dy": dy,
            "rot": rotacion
        })

if apoyos:
    st.success("✅ Apoyos ingresados:")
    st.json(apoyos)

# 🧲 Ingreso de cargas puntuales
st.markdown("### 🧲 Ingreso de cargas puntuales")
num_cargas = st.number_input("Número de cargas puntuales", min_value=0, step=1)

cargas = []
for i in range(num_cargas):
    with st.expander(f"Carga puntual {i+1}"):
        nodo_aplicacion = st.text_input(f"Nodo donde se aplica la carga {i+1}", key=f"nodo_carga_{i}")
        fx = st.number_input(f"Componente Fx (kN) de la carga {i+1}", value=0.0, step=0.1, key=f"fx_{i}")
        fy = st.number_input(f"Componente Fy (kN) de la carga {i+1}", value=0.0, step=0.1, key=f"fy_{i}")
        mz = st.number_input(f"Momento Mz (kN·m) de la carga {i+1}", value=0.0, step=0.1, key=f"mz_{i}")

        cargas.append({
            "nodo": nodo_aplicacion,
            "Fx": fx,
            "Fy": fy,
            "Mz": mz
        })

if cargas:
    st.success("💥 Cargas ingresadas:")
    st.json(cargas)

# 💾 Generar archivo JSON
if st.button("💾 Generar archivo JSON con los datos"):
    if not (nodos and elementos and apoyos and cargas):
        st.warning("⚠️ Debes ingresar todos los datos: nodos, elementos, apoyos y cargas.")
    else:
        datos_estructura = {
            "nodos": nodos,
            "elementos": elementos,
            "apoyos": apoyos,
            "cargas": cargas
        }
        json_data = json.dumps(datos_estructura, indent=4)
        st.download_button(
            label="📥 Descargar archivo JSON",
            data=json_data,
            file_name="estructura_generada.json",
            mime="application/json"
        )

# ---------------------------
# CARGA Y ANÁLISIS DE ARCHIVO
# ---------------------------
datos_json = None
archivo = st.file_uploader("Selecciona un archivo JSON", type=["json"])

if archivo is not None:
    datos_json = json.load(archivo)

    # Transformar listas a diccionarios si es necesario
    if isinstance(datos_json["nodos"], list):
        datos_json["nodos"] = {
            str(i + 1): {"x": nodo["x"], "y": nodo["y"]}
            for i, nodo in enumerate(datos_json["nodos"])
        }

    if isinstance(datos_json["elementos"], list):
        datos_json["elementos"] = {
            str(i + 1): {
                "nodo_i": elem["nodo_i"],
                "nodo_j": elem["nodo_j"],
                "E": elem["E"],
                "A": elem["A"],
                "I": elem["I"]
            }
            for i, elem in enumerate(datos_json["elementos"])
        }

    if isinstance(datos_json["apoyos"], list):
        datos_json["apoyos"] = {
            str(i + 1): apoyo for i, apoyo in enumerate(datos_json["apoyos"])
        }

    if isinstance(datos_json["cargas"], list):
        datos_json["cargas"] = [carga for carga in datos_json["cargas"]]

    st.success("✅ Archivo cargado correctamente. Ya puedes ejecutar el análisis.")

# ---------------------------
# BOTÓN DE ANÁLISIS FINAL
# ---------------------------
boton_analizar = st.button("🔍 Ejecutar análisis", key="boton_analisis_principal")

if boton_analizar:
    if not datos_json:
        st.error("⚠️ Por favor, ingresa datos válidos o sube un archivo JSON.")
    else:
        resultados = analizar_portico(datos_json)

        st.markdown("### 📊 Resultados del Análisis")
        st.subheader("📎 Reacciones en apoyos (kN)")
        st.write(resultados["reacciones"])

        figura = graficar_resultados(resultados["nodos"], resultados["elementos"], resultados["desplazamientos"])
        st.pyplot(figura)

        st.success("✅ Análisis completado exitosamente.")
