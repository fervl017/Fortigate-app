import streamlit as st
import pandas as pd
# Configurar layout
st.set_page_config(page_title="FortiGate Model Selector", layout="wide")
# Cargar Excel
excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None)
# Preparar datos
model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:, 1].tolist()
feature_values = df_raw.iloc[2:, 2:12]
feature_values.columns = model_names
feature_values.index = features
# Guardar copia completa (texto + números)
df_all = feature_values.copy()
# Crear DataFrame numérico
df_models_num = df_all.apply(pd.to_numeric, errors="coerce")
# TÍTULO
st.title("FortiGate Model Selector")
# SIDEBAR – FILTROS
st.sidebar.header("Filtrado de Parámetros")
# Filtro principal
selected_feature = st.sidebar.selectbox("Parámetro principal:", df_models_num.index)
min_val = float(df_models_num.loc[selected_feature].min())
max_val = float(df_models_num.loc[selected_feature].max())
selected_value = st.sidebar.number_input(
   f"Valor mínimo para '{selected_feature}'",
   min_value=min_val,
   max_value=max_val,
   value=min_val,
   step=1.0 if max_val - min_val < 100 else 100.0
)
# Filtros adicionales
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros adicionales")
additional_filters = {}
optional_features = [
   "New Sessions/Sec",
   "Firewall Policies",
   "Firewall Latency (micro seconds)",
   "Concurrent Sessions",
   "Max G/W to GIW IPSEC Tunnels",
   "Max Client to GIW IPSEC Tunnels"
]
for feature in optional_features:
   if feature in df_models_num.index:
       min_val = float(df_models_num.loc[feature].min())
       max_val = float(df_models_num.loc[feature].max())
       val = st.sidebar.number_input(
           f"{feature}",
           min_value=min_val,
           max_value=max_val,
           value=min_val,
           step=1.0 if max_val - min_val < 100 else 100.0
       )
       additional_filters[feature] = val
# Filtros por texto (Interfaces, Local Storage…)
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros por texto (opcionales)")
text_filters = {}
text_features = ["Interfaces", "Local Storage", "Power Supplies", "Form Factor", "Variants"]
for feature in text_features:
   if feature in df_all.index:
       # Limpiar valores: quedarnos solo con lo que está antes del paréntesis
       opciones_originales = df_all.loc[feature].dropna().unique().tolist()
       opciones_limpias = [str(x).split(" (")[0] for x in opciones_originales]
       opciones_limpias = sorted(set(opciones_limpias))
       seleccion = st.sidebar.selectbox(f"{feature}", [""] + opciones_limpias)
       if seleccion != "":
           # Filtro: que la celda contenga ese texto limpio (ignorando lo que hay entre paréntesis)
           text_filters[feature] = seleccion
# Filtrar modelos por valores numéricos
filtered_columns = df_models_num.columns
filtered_columns = df_models_num.columns[df_models_num.loc[selected_feature] >= selected_value]
for feature, min_val in additional_filters.items():
   filtered_columns = filtered_columns.intersection(df_models_num.columns[df_models_num.loc[feature] >= min_val])
# Filtrar por texto
for feature, required_text in text_filters.items():
   filtered_columns = filtered_columns.intersection(
       df_all.columns[df_all.loc[feature].str.contains(required_text, case=False, na=False)]
   )
# Mostrar resultados
st.subheader("Modelos FortiGate compatibles", divider="blue")
if len(filtered_columns) > 0:
   df_final = df_all[filtered_columns]  # Usar df_all para incluir texto y números
   df_final = df_final.reset_index().rename(columns={"index": "Feature"}).set_index("Feature")
   st.dataframe(df_final, use_container_width=True, height=600)
else:
   st.warning("No hay modelos que cumplan con los criterios seleccionados.")
