import streamlit as st
import pandas as pd
# Cargar Excel
excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None)
# Extraer nombres de modelos y características
model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:23, 1].tolist()
feature_values = df_raw.iloc[2:23, 2:12]
feature_values.columns = model_names
feature_values.index = features
# SIN transponer: modelos son columnas, características son filas
df_models = feature_values
df_models = df_models.apply(pd.to_numeric, errors="coerce")
# Título
st.title("FortiGate Model Selector")
st.markdown("Primero selecciona el parámetro principal a filtrar. Luego puedes aplicar filtros adicionales opcionales.")
# FILTRO PRINCIPAL
selected_feature = st.selectbox("Selecciona el parámetro principal:", df_models.index)
if pd.notna(df_models.loc[selected_feature].min()) and pd.notna(df_models.loc[selected_feature].max()):
   min_val = float(df_models.loc[selected_feature].min())
   max_val = float(df_models.loc[selected_feature].max())
   selected_value = st.slider(
       f"Selecciona el valor mínimo para '{selected_feature}'",
       min_value=min_val,
       max_value=max_val,
       value=min_val
   )
# FILTROS ADICIONALES OPCIONALES
st.markdown("### Filtros adicionales (opcionales)")
additional_filters = {}
# Lista de características secundarias (deben coincidir con filas reales del Excel)
optional_features = [
   "New Sessions/Sec",
   "Firewall Policies",
   "Firewall Latency (µs)",
   "Concurrent Sessions"
]
for feature in optional_features:
   if feature in df_models.index:
       min_val = float(df_models.loc[feature].min())
       max_val = float(df_models.loc[feature].max())
       selected = st.slider(
           f"Valor mínimo para '{feature}'",
           min_value=min_val,
           max_value=max_val,
           value=min_val
       )
       additional_filters[feature] = selected
# FILTRAR MODELOS (columnas que cumplen los requisitos)
# Empieza filtrando columnas por el parámetro principal
filtered_df = df_models.loc[:, df_models.loc[selected_feature] >= selected_value]
# Aplica filtros adicionales (manteniendo solo columnas que cumplan todos)
for feature, min_val in additional_filters.items():
   filtered_df = filtered_df.loc[:, filtered_df.loc[feature] >= min_val]
# MOSTRAR RESULTADOS
st.subheader("Matching FortiGate Models")
if not filtered_df.empty:
   # Formatear con 2 decimales
   filtered_df = filtered_df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (float, int)) else x)
   # Mostrar tabla con scroll
   st.dataframe(
       filtered_df
   )
else:
   st.warning("No hay modelos que cumplan con los criterios seleccionados.")
