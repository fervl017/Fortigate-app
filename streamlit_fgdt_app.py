import streamlit as st
import pandas as pd

# Cargar Excel
excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None, storage_options=None, engine_kwargs=None)

df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None)
# Extraer nombres de modelos y características
model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:23, 1].tolist()
feature_values = df_raw.iloc[2:23, 2:12]
feature_values.columns = model_names
feature_values.index = features
df_models = feature_values.T
df_models = df_models.apply(pd.to_numeric, errors="coerce")

# Título
st.title("FortiGate Model Selector")
st.markdown("Use the sliders below to set your minimum requirements. The app will show FortiGate models that meet or exceed your criteria.")

user_input = {}
for feature in df_models.columns:
    min_val = df_models[feature].min()
    max_val = df_models[feature].max()
    if pd.notna(min_val) and pd.notna(max_val) and min_val != max_val:
        user_input[feature] = st.sidebar.slider(
            label=feature,
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(min_val)
        )

filtered_df = df_models.copy()
for feature, value in user_input.items():
    filtered_df = filtered_df[filtered_df[feature] >= value]

st.subheader("Matching FortiGate Models")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No models match the selected criteria.")
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
       st.dataframe(filtered_df)
   else:
       st.warning("No hay modelos que cumplan con el criterio.")
