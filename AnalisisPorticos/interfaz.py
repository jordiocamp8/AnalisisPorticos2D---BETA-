import streamlit as st
from analizador_multiportico import procesar_archivo_csv

st.set_page_config(page_title="Análisis de Pórticos Múltiples", layout="wide")
st.title("🏗️ Análisis de Pórticos Múltiples desde CSV")

st.markdown("### 📂 Cargar archivo CSV con los datos de los pórticos")

archivo = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

if archivo is not None:
    st.success("✅ Archivo cargado correctamente. Procesando...")
    
    resultados = procesar_archivo_csv(archivo)

    for resultado in resultados:
        st.markdown(f"### 📊 Resultados para {resultado['nombre']}")
        st.write("**Reacciones (kN):**", resultado["reacciones"])
        st.write("**Desplazamientos (mm):**", resultado["desplazamientos"])
        st.write("**Fuerzas internas (kN):**", resultado["fuerzas_internas"])
