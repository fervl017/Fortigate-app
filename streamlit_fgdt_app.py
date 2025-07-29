import streamlit as st
import pandas as pd
# --------------------------------------
# CARGAR DATOS DESDE EL EXCEL
# --------------------------------------
excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None)
model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:23, 1].tolist()
feature_values = df_raw.iloc[2:23, 2:12]
feature_values.columns = model_names
feature_values.index = features
# No transponemos: modelos en columnas, características en filas
df_models = feature_values
df_models = df_models.apply(pd.to_numeric, errors="coerce")
# --------------------------------------
# INTERFAZ EN DOS COLUMNAS
# --------------------------------------
st.set_page_config(layout="wide")  # para usar todo el ancho
st.title("FortiGate Model Selector")
st.markdown("Ajusta los filtros en la columna izquierda y revisa los modelos disponibles a la derecha.")
col1, col2 = st.columns([1, 3])  # Filtros | Resultados
# --------------------------------------
# 🎯 FILTROS (COLUMNA IZQUIERDA)
# --------------------------------------
with col1:
   st.markdown("### Filtro principal")
   selected_feature = st.selectbox("Selecciona el parámetro principal:", df_models.index)
   if pd.notna(df_models.loc[selected_feature].min()) and pd.notna(df_models.loc[selected_feature].max()):
       min_val = float(df_models.loc[selected_feature].min())
       max_val = float(df_models.loc[selected_feature].max())
       selected_value = st.number_input(
           f"Valor mínimo para '{selected_feature}'",
           min_value=min_val,
           max_value=max_val,
           value=min_val,
           step=1.0 if max_val - min_val < 100 else 100.0
       )
   st.markdown("### Filtros adicionales (opcionales)")
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
           val = st.number_input(
               f"Valor mínimo para '{feature}'",
               min_value=min_val,
               max_value=max_val,
               value=min_val,
               step=1.0 if max_val - min_val < 100 else 100.0
           )
           additional_filters[feature] = val
# --------------------------------------
# 📊 RESULTADOS (COLUMNA DERECHA)
# --------------------------------------
with col2:
   st.subheader("Matching FortiGate Models")
   # Filtrar por parámetro principal
   filtered_df = df_models.loc[:, df_models.loc[selected_feature] >= selected_value]
   # Aplicar filtros adicionales
   for feature, min_val in additional_filters.items():
       filtered_df = filtered_df.loc[:, filtered_df.loc[feature] >= min_val]
   if not filtered_df.empty:
       # Formatear números
       filtered_df = filtered_df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (float, int)) else x)
       # Convertir índice en columna y volverlo a poner como índice, para evitar numeración automática
       df_final = filtered_df.reset_index().rename(columns={"index": "Feature"}).set_index("Feature")
       st.dataframe(df_final, use_container_width=True, height=600)
   else:
       st.warning("No hay modelos que cumplan con los criterios seleccionados.")
