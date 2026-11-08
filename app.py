
import streamlit as st
import pandas as pd
import joblib

# Configuración de la aplicación
st.set_page_config(
    page_title="Predicción de Accidentes Medellín",
    page_icon="🚦",
    layout="centered"
)

# Cargar modelo
modelo = joblib.load("modelo_accidentes_medellin.pkl")

# Título
st.title("🚦 Predicción de gravedad de accidentes")
st.subheader("Medellín - Antioquia")

st.write(
    "Ingrese las características del accidente "
    "para predecir su gravedad."
)

# Formulario
with st.form("formulario_accidente"):

    fecha = st.date_input("Fecha del accidente")

    hora = st.time_input("Hora del accidente")

    dias = [
        "lunes", "martes", "miércoles",
        "jueves", "viernes", "sábado", "domingo"
    ]

    dia = st.selectbox("Día", dias)

    meses = [
        "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto",
        "septiembre", "octubre", "noviembre", "diciembre"
    ]

    mes = st.selectbox("Mes", meses)

    anio = st.number_input(
        "Año",
        min_value=2019,
        max_value=2030,
        value=2025
    )

    clases = [
        "CHOQUE", "OTRO", "ATROPELLO",
        "VOLCAMIENTO", "CAIDA OCUPANTE", "INCENDIO"
    ]

    clase = st.selectbox("Clase de accidente", clases)

    barrio = st.text_input("Barrio", value="El Poblado")

    comunas = [
        "Popular", "Santa Cruz", "Manrique",
        "Aranjuez", "Castilla", "Doce de Octubre",
        "Robledo", "Villa Hermosa", "Buenos Aires",
        "La Candelaria", "Laureles Estadio",
        "La América", "San Javier", "El Poblado",
        "Guayabal", "Belén"
    ]

    comuna = st.selectbox("Comuna", comunas)

    latitud = st.number_input(
        "Latitud",
        value=6.2088,
        format="%.6f"
    )

    longitud = st.number_input(
        "Longitud",
        value=-75.5670,
        format="%.6f"
    )

    enviar = st.form_submit_button("Predecir gravedad")

# Realizar predicción
if enviar:

    datos = pd.DataFrame([{
        "fecha_siniestro": pd.Timestamp(fecha),
        "hora_siniestro": hora.strftime("%H:%M:%S"),
        "hora": hora.hour,
        "dia": dia,
        "mes": mes,
        "anio": anio,
        "clase_siniestro": clase,
        "barrio": barrio,
        "nom_comuna": comuna,
        "latitud": latitud,
        "longitud": longitud
    }])

    prediccion = modelo.predict(datos)[0]

    st.divider()

    st.subheader("Resultado de la predicción")

    if prediccion == "HERIDOS":
        st.error("Predicción: ACCIDENTE CON PERSONAS HERIDAS")
    else:
        st.success("Predicción: ACCIDENTE CON DAÑOS MATERIALES")

    st.info(
        "Esta predicción es una estimación del modelo "
        "y no representa una confirmación de la gravedad real."
    )
