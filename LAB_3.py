import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataInsight Analytics", layout="wide")

st.title("DataInsight Analytics")
st.write("Analisis de cuatro datasets: Vehiculos Electricos, Gimnasio, Steam, Netflix.")

# =============================================================================
# CARGA DE DATOS
# =============================================================================

@st.cache_data
def cargar_datos():
    df_ev      = pd.read_csv("Electric_Vehicle_Population-2.csv")
    df_gym     = pd.read_csv("GymExerciseTracking.csv")
    df_steam   = pd.read_csv("steam_store_data_2024.csv")
    df_netflix = pd.read_csv("netflix_titles.csv")

    df_steam["precio_num"] = (
        df_steam["price"]
        .str.replace("$", "", regex=False)
        .astype(float)
    )
    df_steam["descuento_num"] = (
        pd.to_numeric(
            df_steam["salePercentage"].str.replace("%", "", regex=False),
            errors="coerce"
        )
        .abs()
        .fillna(0)
        .astype(int)
    )

    df_netflix["anio_agregado"] = pd.to_datetime(
        df_netflix["date_added"].str.strip(),
        format="%B %d, %Y",
        errors="coerce"
    ).dt.year

    df_netflix["duracion_min"] = (
        df_netflix["duration"]
        .str.extract(r"(\d+) min")
        .astype(float)
    )

    return df_ev, df_gym, df_steam, df_netflix


try:
    df_ev, df_gym, df_steam, df_netflix = cargar_datos()
    datos_cargados = True
except FileNotFoundError as e:
    st.error(f"Archivo no encontrado: {e}.")
    datos_cargados = False

if not datos_cargados:
    st.stop()

if "df_ev" not in st.session_state:
    st.session_state.df_ev = df_ev.copy()
if "df_gym" not in st.session_state:
    st.session_state.df_gym = df_gym.copy()

df_ev    = st.session_state.df_ev
df_gym   = st.session_state.df_gym

# =============================================================================
# NAVEGACION
# =============================================================================

seccion = st.sidebar.radio(
    "Seccion",
    [
        "1. Exploracion inicial",
        "2. Ingreso de nuevos datos",
        "3. Filtrado de datos",
        "4. Exploracion avanzada",
        "5. Preguntas clave",
    ]
)