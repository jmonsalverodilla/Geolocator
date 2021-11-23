##########################################Libraries###########################
from flask import Flask, request, render_template
import pandas as pd
from src.locator_api import locator,assign_cusec
from src.folium_map import mapa
import yaml
import os

###########################################CODE##############################################
app = Flask(__name__)

#Primer html: insertar los datos
@app.route('/')
def home():
    return render_template('index_pro.html')

#Segundo html: predict
def load_conf_file(config_file):
  with open(config_file, "r") as f:
      config = yaml.safe_load(f)
  return config

config = load_conf_file("./config/settings.yml")
area = config["CUSEC"]["LISTA_CA"][0]

@app.route('/predict', methods=['POST'])
def predict():
    final_features = [list(request.form.values())]

    column_names = ['tipo_via', 'nombre_via', 'numero_portal', 'codigo_postal', 'municipio', 'provincia']

    df = pd.DataFrame(final_features, columns=column_names)
    df['direccion'] = df['tipo_via'] + ' ' + df['nombre_via'] + ', ' + df['numero_portal'] + ', ' + df[
        'codigo_postal'] + ', ' + df['municipio'] + ', ' + df['provincia'] + ', ' + 'Spain'

    #Llamo a una función que a su vez llama a una API
    df_located = locator(df)
    global df_output #df_output is a geopandas dataframe
    df_output = assign_cusec(df_located)
    if df_output.shape[0] == 0:
        return render_template('index_pro.html',
                               result='La dirección introducida no pertenece a {},introduzca otra dirección'.format(area))
    if df_output['longitud'][0] == "NaN":
        return render_template('index_pro.html',
                               result='La dirección introducida no ha sido encontrada, revise los campos'.format(area))
    else:
        global df_final
        df_final = df.merge(df_output, how="inner", on=['direccion'])

        figure = mapa(df_final, df_output)
        return figure._repr_html_()

if __name__ == '__main__':
    port = os.environ.get("PORT", 8080)
    app.run(debug=False, host="0.0.0.0", port=port)
