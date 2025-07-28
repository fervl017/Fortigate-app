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
df_models = feature_values
df_models = df_models.apply(pd.to_numeric, errors="coerce")
# Título
st.title("FortiGate Model Selector")
st.markdown("Primero selecciona el parámetro que deseas usar como filtro. Luego ajusta el valor mínimo deseado para ver los modelos que cumplen con ese requisito.")
# Paso 1: Elegir el parámetro
selected_feature = st.selectbox("Selecciona el parámetro a filtrar:", df_models.columns)
# Paso 2: Mostrar slider para ese parámetro
if pd.notna(df_models[selected_feature].min()) and pd.notna(df_models[selected_feature].max()):
   min_val = float(df_models[selected_feature].min())
   max_val = float(df_models[selected_feature].max())
   selected_value = st.slider(
       f"Selecciona el valor mínimo para '{selected_feature}'",
       min_value=min_val,
       max_value=max_val,
       value=min_val
   )
   # Paso 3: Filtrar modelos
   filtered_df = df_models[df_models[selected_feature] >= selected_value]
   # Mostrar resultados
   st.subheader("Matching FortiGate Models")
   if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
   else:
       st.warning("No hay modelos que cumplan con el criterio.")
