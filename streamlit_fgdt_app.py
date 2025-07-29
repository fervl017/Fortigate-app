import streamlit as st
import pandas as pd
# Configurar layout de página en ancho completo
st.set_page_config(page_title="FortiGate Model Selector", layout="wide")
# Cargar Excel
excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None)
# Preparar datos
model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:23, 1].tolist()
feature_values = df_raw.iloc[2:23, 2:12]
feature_values.columns = model_names
feature_values.index = features
df_models = feature_values.apply(pd.to_numeric, errors="coerce")
# TÍTULO
st.title("FortiGate Sizing Tool v1.0")
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
   "Firewall Latency (µs)",
   "Concurrent Sessions"
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
# RESULTADOS
st.subheader("Modelos FortiGate compatibles", divider="blue")
# Filtrar por el parámetro principal
filtered_df = df_models.loc[:, df_models.loc[selected_feature] >= selected_value]
# Aplicar filtros adicionales
for feature, min_val in additional_filters.items():
   filtered_df = filtered_df.loc[:, filtered_df.loc[feature] >= min_val]
if not filtered_df.empty:
   # Formato y limpieza final
   filtered_df = filtered_df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (float, int)) else x)
   df_final = filtered_df.reset_index().rename(columns={"index": "Feature"}).set_index("Feature")
   st.dataframe(df_final, use_container_width=True, height=600)
else:
   st.warning("No hay modelos que cumplan con los criterios seleccionados.")
