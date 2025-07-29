import streamlit as st
import pandas as pd
# Configurar layout de página en ancho completo
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
# Separar en numérico y texto
df_all = feature_values.copy()
df_models_num = df_all.apply(pd.to_numeric, errors="coerce")
df_models_text = df_all[df_all.applymap(lambda x: isinstance(x, str))]
# Usaremos df_models_num como base
df_models = df_models_num
# TÍTULO
st.title("FortiGate Model Selector")
# SIDEBAR – FILTROS
st.sidebar.header("Filtrado de Parámetros")
# Filtro principal
selected_feature = st.sidebar.selectbox("Parámetro principal:", df_models.index)
if pd.notna(df_models.loc[selected_feature].min()) and pd.notna(df_models.loc[selected_feature].max()):
   min_val = float(df_models.loc[selected_feature].min())
   max_val = float(df_models.loc[selected_feature].max())
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
   if feature in df_models.index:
       min_val = float(df_models.loc[feature].min())
       max_val = float(df_models.loc[feature].max())
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
   if feature in df_models_text.index:
       opciones = df_models_text.loc[feature].dropna().unique().tolist()
       seleccion = st.sidebar.selectbox(f"{feature}", [""] + sorted(opciones))
       if seleccion != "":
           text_filters[feature] = seleccion
# RESULTADOS
st.subheader("Modelos FortiGate compatibles", divider="blue")
# Filtrado numérico
filtered_df = df_models.loc[:, df_models.loc[selected_feature] >= selected_value]
for feature, min_val in additional_filters.items():
   filtered_df = filtered_df.loc[:, filtered_df.loc[feature] >= min_val]
# Filtrado por texto
for feature, required_text in text_filters.items():
   filtered_df = filtered_df.loc[:, df_models_text.loc[feature].str.contains(required_text, case=False, na=False)]
# Mostrar resultados
if not filtered_df.empty:
   # Unir filas de texto como Interfaces, etc.
   extra_rows = df_models_text.loc[text_filters.keys(), filtered_df.columns]
   final_combined = pd.concat([filtered_df, extra_rows], axis=0)
   # Formato bonito
   final_combined = final_combined.applymap(lambda x: f"{x:.2f}" if isinstance(x, (float, int)) else x)
   df_final = final_combined.reset_index().rename(columns={"index": "Feature"}).set_index("Feature")
   st.dataframe(df_final, use_container_width=True, height=600)
else:
   st.warning("No hay modelos que cumplan con los criterios seleccionados.")
