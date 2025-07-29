# Dividir la pantalla en 2 columnas
col1, col2 = st.columns([1, 3])  # Izquierda: filtros | Derecha: resultados
# ---------------------------------------------
# 🎯 FILTROS EN COLUMNA IZQUIERDA (col1)
# ---------------------------------------------
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
# ---------------------------------------------
# 📊 RESULTADOS EN COLUMNA DERECHA (col2)
# ---------------------------------------------
with col2:
   st.subheader("Matching FortiGate Models")
   # Filtrar por el principal
   filtered_df = df_models.loc[:, df_models.loc[selected_feature] >= selected_value]
   # Filtrar por los adicionales
   for feature, min_val in additional_filters.items():
       filtered_df = filtered_df.loc[:, filtered_df.loc[feature] >= min_val]
   if not filtered_df.empty:
       filtered_df = filtered_df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (float, int)) else x)
       df_final = filtered_df.reset_index().rename(columns={"index": "Feature"}).set_index("Feature")
       st.dataframe(df_final, use_container_width=True, height=600)
   else:
       st.warning("No hay modelos que cumplan con los criterios seleccionados.")
