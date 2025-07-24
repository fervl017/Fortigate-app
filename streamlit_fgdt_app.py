import streamlit as st
import pandas as pd

excel_file = "Data/Models Comparison FortiNet (Tables).xlsx"
df_raw = pd.read_excel(excel_file, sheet_name="FG_Features_Matrix", engine="openpyxl", header=None, storage_options=None, engine_kwargs=None)

model_names = df_raw.iloc[1, 2:12].tolist()
features = df_raw.iloc[2:23, 1].tolist()
feature_values = df_raw.iloc[2:23, 2:12]
feature_values.columns = model_names
feature_values.index = features
df_models = feature_values.T
df_models = df_models.apply(pd.to_numeric, errors="coerce")

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
