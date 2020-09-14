
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Passive Investment vs Active Investment strategies                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: marcosotm                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/marcosotm/myst_lab1_MOTM.git                                         -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import data as dt
import functions as fn
import pandas as pd



# data.py
# ---------------------------------------------------------------------------------------- Paso 1.1 -- #
# -- Obtener la lista de todos los archivos

archivos = dt.archivos()


# ---------------------------------------------------------------------------------------- Paso 1.2 -- #
# -- Leer todods los archivos y guardarlos en un diccionario

data_archivos = dt.data_archivos(archivos)


# fucntions.py
# ---------------------------------------------------------------------------------------- Paso 1.3 -- #
# Counstruir el vector de fechas a partir del vector de nombres de los archivos

i_fechas = fn.f_fechas(archivos)
print(i_fechas[0:4])


# functions.py
# ----------------------------------------------------------------------------------------- Paso 1.4 -- #
# -- Construir el vector de tickers utilizables en yahoo finance

global_tickers = fn.obtener_tickers(archivos, data_archivos)
print(global_tickers[0:4])

# funtions.py
# ----------------------------------------------------------------------------------------- Paso 1.5 -- #
# -- Descargar y acomodar todos los precios historicos

precios = fn.descarga_precios(global_tickers, i_fechas)
print(precios.head())

# main.py
# ----------------------------------------------------------------------------------------- Paso 2.1 -- #
# -- Definir capital inicial, el costo de comisiones y el diccionario base para el df final

# capital inicial
k = 1000000
# porcentaje de comision por transaccion
c = 0.0125
# fecha de inicio (previo a cualquier transaccion)
tiempo_cero = '2018-01-30'
# diccionario para resultado final
inv_pasiva = {'timestamp': [tiempo_cero], 'capital': [k]}


# main.py
# ----------------------------------------------------------------------------------------- Paso 2.2 -- #
# -- Definir df de la posicion inicial, remover tickers que no se utilizan y actualizar los que cambiaron

pos_datos = data_archivos['NAFTRAC_310118'].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]
# los % para KOFL, KOFUBL, BSMXB, USD seran asignados a cash
c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']
# extraer la lista de activos a eliminar
i_activos = list(pos_datos[list(pos_datos['Ticker'].isin(c_activos))].index)
# eliminar los activos del dataframe
pos_datos.drop(i_activos, inplace=True)
# agregar .MX para empatar precios
pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'
# actualizar tickers
pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')
print(pos_datos.head())


# main.py
# ----------------------------------------------------------------------------------------- Paso 2.3 -- #
# -- Agregar columna de precios desde los datos descargados

match = 0
print(precios.index.to_list()[match])
precio_inicial = [precios.iloc[match, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]
pos_datos['Precio'] = precio_inicial


# main.py
# ----------------------------------------------------------------------------------------- Paso 2.4 -- #
# -- Agregar columna de Titulos, Postura y Comision

# se calcula el capital destinado a cada accion, pero no se agrega como columna
capital = pos_datos['Peso (%)']*k - pos_datos['Peso (%)']*k*c

# cantidad de titulos por accion
pos_datos['Titulos'] = capital//pos_datos['Precio']

# valor de la postura por accion
pos_datos['Postura'] = pos_datos['Titulos']*pos_datos['Precio']

# costo de comision por accion y total
pos_datos['Comision'] = pos_datos['Postura']*c
pos_comision = pos_datos['Comision'].sum()

# efectivo libre en la postura
pos_cash = k - pos_datos['Postura'].sum() - pos_comision

# valor de la posicion
pos_value = pos_datos['Postura'].sum()

print(pos_datos.head())

# se agrega al diccionario la posicion inicial
inv_pasiva['timestamp'].append(i_fechas[0])
inv_pasiva['capital'].append(pos_value + pos_cash)


# main.py
# ----------------------------------------------------------------------------------------- Paso 3.1 -- #
# -- Calcular la evolucion del valor de la posicion durante las fechas seleccionadas

match = 1
for match in range(len(precios)):
    precios_i = [precios.iloc[match, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]
    capital_i = sum(pos_datos['Titulos'] * precios_i)

    inv_pasiva['timestamp'].append(precios.index.astype(str).to_list()[match])
    inv_pasiva['capital'].append(capital_i + pos_cash)

print(inv_pasiva)


# main.py
# ----------------------------------------------------------------------------------------- Paso 3.2 -- #
# -- Crear df_pasiva y calcular rendimiento y rendimiento acumulado

df_pasiva = pd.DataFrame(inv_pasiva)
df_pasiva['rend'] = df_pasiva['capital'].pct_change()
df_pasiva['rend_acum'] = df_pasiva['rend'].cumsum()
df_pasiva = df_pasiva.fillna(0)
df_pasiva = df_pasiva.set_index('timestamp')

print(df_pasiva)
