
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Passive Investment vs Active Investment strategies                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: marcosotm                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/marcosotm/myst_lab1_MOTM.git                                         -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import os
import pandas as pd


def archivos():
    path = 'files/NAFTRAC_holdings'
    abspath = os.path.abspath(path)
    archivos_lista = [f[:-4] for f in os.listdir(abspath) if os.path.isfile(os.path.join(abspath, f))]
    return archivos_lista


def data_archivos(files):
    data_archivos_dict = {}

    for i in files:
        # leer archivos despues de los primeros 2 renglones
        data = pd.read_csv('files/NAFTRAC_holdings/' + i + '.csv', skiprows=2,
                           header=None)
        # renombrar columnas
        data.columns = list(data.iloc[0, :])
        data = data.loc[:, pd.notnull(data.columns)]
        data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
        # remover comas
        data['Precio'] = [i.replace(',', '') for i in data['Precio']]
        # remover asteriscos
        data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
        convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
        data = data.astype(convert_dict)
        # convertir a decimal la columna de peso
        data['Peso (%)'] = data['Peso (%)'] / 100
        # guardar en diccionario
        data_archivos_dict[i] = data


    return data_archivos_dict