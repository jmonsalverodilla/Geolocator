#Imports
import joblib
import yaml

###############CONFIG FILE#############################
#Reading from config file
def load_conf_file(config_file):
   with open(config_file, "r") as f:
       config = yaml.safe_load(f)
   return config

config = load_conf_file("../config/settings.yml")
lista_ca = config["CUSEC"]["LISTA_CA"]
variables = config["CUSEC"]["VARIABLES"]

#Importing file
df_cusec = joblib.load('../obj/df_cusec_geometry.pkl')

#Subset
df_cusec_reduced = df_cusec[df_cusec['NCA'].isin(lista_ca)][variables]
joblib.dump(df_cusec_reduced, "../obj/df_cusec_reduced_geometry.pkl")
