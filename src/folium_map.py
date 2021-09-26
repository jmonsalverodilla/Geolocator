#Imports
import folium

def mapa(df_final,df_output):
    # Creamos figure
    figure = folium.Figure(width=1000, height=500)
    latitud = df_final['latitud'][0];
    longitud = df_final['longitud'][0];
    direccion = df_final['direccion'][0]
    mapa = folium.Map(location=[latitud, longitud], zoom_start=14, tiles='cartodbpositron').add_to(figure)

    # Añadimos markers individuales
    folium.Marker([latitud, longitud],
                  icon=folium.Icon(color='blue'), tooltip=direccion).add_to(mapa)
    print(df_final[['CUSEC', 'precio_m2', 'geometry']])

    folium.features.GeoJson(
        df_output.to_json(),
        tooltip=folium.features.GeoJsonTooltip(
            fields=['CUSEC', 'precio_m2'],
            aliases=['CUSEC: ', 'precio_m2: ']),
        name="CUSEC layer",
    ).add_to(mapa)

    # Añadimos tiles
    folium.TileLayer('OpenStreetMap', attr="OpenStreetMap", name="OpenStreetMap", overlay=False).add_to(mapa)
    folium.LayerControl().add_to(mapa)
    return figure


###################################UNUSED CODE#############################################
    # Set up Choropleth map
    # folium.Choropleth(geo_data=df_output[['CUSEC', 'precio_m2', 'geometry']].to_json(),
    #                   data=df_output[['CUSEC', 'precio_m2', 'geometry']],
    #                   columns=['CUSEC', 'precio_m2'],
    #                   key_on="feature.properties.CUSEC",
    #                   fill_color='RdBu', fill_opacity=0.6, line_opacity=0.6, legend_name="Legend", smooth_factor=0, Highlight=True,
    #                   line_color="white", name="CUSEC layer",
    #                   show=True, overlay=True, nan_fill_color="White"
    #                   ).add_to(mapa)

    #folium.GeoJson(data=df_output["geometry"][0]).add_to(mapa)