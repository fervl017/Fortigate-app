import streamlit as st
import pandas as pd
# Cargar Excel
excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None)
# Extraer nombres y datos
model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:23, 1].tolist()
feature_values = df_raw.iloc[2:23, 2:12]
feature_values.columns = model_names
feature_values.index = features
df_models = feature_values.T
df_models = df_models.apply(pd.to_numeric, errors="coerce")
# Título principal
st.title("FortiGate Model Selector")
st.markdown("Primero selecciona el parámetro principal a filtrar. Luego puedes aplicar filtros adicionales opcionales.")
# ---------------------------------------------
# 🎯 FILTRO PRINCIPAL
# ---------------------------------------------
selected_feature = st.selectbox("Selecciona el parámetro principal:", df_models.columns)
if pd.notna(df_models[selected_feature].min()) and pd.notna(df_models[selected_feature].max()):
   min_val = float(df_models[selected_feature].min())
   max_val = float(df_models[selected_feature].max())
   selected_value = st.slider(
       f"Selecciona el valor mínimo para '{selected_feature}'",
       min_value=min_val,
       max_value=max_val,
       value=min_val
   )
# ---------------------------------------------
# 🧩 FILTROS ADICIONALES OPCIONALES
# ---------------------------------------------
st.markdown("### Filtros adicionales (opcionales)")
additional_filters = {}
# Lista de filtros secundarios que te interesan
optional_features = [
   "New Sessions/Sec",
   "Firewall Policies",
   "Firewall Latency (µs)",
   "Concurrent Sessions"
]
for feature in optional_features:
   if feature in df_models.columns:
       min_val = float(df_models[feature].min())
       max_val = float(df_models[feature].max())
       selected = st.slider(
           f"Valor mínimo para '{feature}'",
           min_value=min_val,
           max_value=max_val,
           value=min_val
       )
       additional_filters[feature] = selected
# ---------------------------------------------
# 📊 FILTRAR MODELOS
# ---------------------------------------------
filtered_df = df_models[df_models[selected_feature] >= selected_value]
# Aplicar filtros adicionales
for feature, min_val in additional_filters.items():
   filtered_df = filtered_df[filtered_df[feature] >= min_val]
# ---------------------------------------------
# 📋 MOSTRAR RESULTADOS
# ---------------------------------------------
st.subheader("Matching FortiGate Models")
   if not filtered_df.empty:
       st.dataframe(filtered_df)
   else:
       st.warning("No hay modelos que cumplan con el criterio.")
