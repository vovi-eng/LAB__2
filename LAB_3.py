import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataInsight Analytics", layout="wide")

st.title("DataInsight Analytics")
st.write("Analisis de cuatro datasets: Vehiculos Electricos, Gimnasio, Steam, Netflix.")


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


if seccion == "1. Exploracion inicial":
    st.header("Seccion 1 - Lectura y exploracion inicial")

    datasets = {
        "Vehiculos Electricos": df_ev,
        "Gimnasio": df_gym,
        "Steam Store 2024": df_steam,
        "Netflix Titulos": df_netflix,
    }

    for nombre, df in datasets.items():
        st.subheader(nombre)
        filas, columnas = df.shape
        st.write(f"Filas: {filas}    Columnas: {columnas}")
        st.write("Columnas: " + ", ".join(df.columns.tolist()))
        st.write("Primeras 6 filas:")
        st.dataframe(df.head(6))
        st.write("Estadisticas numericas:")
        st.dataframe(df.describe(include="all"))
        st.write("---")


elif seccion == "2. Ingreso de nuevos datos":
    st.header("Seccion 2 - Ingreso de nuevos datos")

    st.subheader("Nuevo registro - Vehiculos Electricos")

    with st.form("form_ev"):
        vin = st.text_input("VIN (primeros 10 caracteres)")
        ciudad = st.text_input("Ciudad")
        anio = st.number_input("Año del modelo", 2000, 2025)
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        tipo_ev = st.selectbox("Tipo EV", ["BEV", "PHEV"])
        rango = st.number_input("Rango electrico", 0)
        msrp = st.number_input("Precio base", 0)
        submit_ev = st.form_submit_button("Agregar vehiculo")

    if submit_ev:
        nuevo = {
            "VIN (1-10)": vin,
            "City": ciudad,
            "Model Year": anio,
            "Make": marca,
            "Model": modelo,
            "Electric_Vehicle_Type": tipo_ev,
            "Electric_Range": rango,
            "Base_MSRP": msrp,
        }
        st.session_state.df_ev = pd.concat([df_ev, pd.DataFrame([nuevo])], ignore_index=True)
        st.success("Vehiculo agregado")


elif seccion == "3. Filtrado de datos":
    st.header("Filtros")

    anio_lim = st.number_input("Año menor a", 2000, 2025, 2015)
    st.dataframe(df_ev[df_ev["Model Year"] < anio_lim])


elif seccion == "4. Exploracion avanzada":
    st.header("Exploracion avanzada")

    df_ev2 = df_ev.copy()
    df_ev2["RangoCategoria"] = df_ev2["Electric_Range"].apply(
        lambda x: "Bajo" if x < 100 else "Medio" if x <= 250 else "Alto"
    )

    conteo_ev = df_ev2["RangoCategoria"].value_counts()
    st.dataframe(conteo_ev)

    st.subheader("Graficas de barras")
    st.bar_chart(conteo_ev)

elif seccion == "5. Preguntas clave":
    st.header("Preguntas")

    corr = df_ev[["Electric_Range", "Model Year"]].corr().iloc[0, 1]
    st.write(f"Correlacion: {corr:.4f}")



st.sidebar.markdown("---")

if st.sidebar.button("Guardar CSV actualizados"):
    df_ev.to_csv("Electric_Vehicle_Population_Actualizado.csv", index=False)
    df_gym.to_csv("GymExerciseTracking_Actualizado.csv", index=False)
    df_steam.to_csv("steam_store_data_2024_Actualizado.csv", index=False)
    df_netflix.to_csv("netflix_titles_Actualizado.csv", index=False)

    st.sidebar.success("Archivos guardados correctamente")