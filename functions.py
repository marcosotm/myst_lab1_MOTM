
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: marcosotm                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import numpy as np
import time
import yfinance as yf


def f_fechas(files):
    return [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in files])]


def obtener_tickers(files, data_files):
    tickers = []
    for i in files:
        l_tickers = list(data_files[i]['Ticker'])
        [tickers.append(i + '.MX') for i in l_tickers]

    # se remueven tickers repetidos
    global_tickers = np.unique(tickers).tolist()
    # se remplazan tickers que se actualizaron
    global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
    global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
    global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]
    # se remueven los que no son tickers y los que contienen informacion incompleta
    [global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'KOFUBL.MX', 'BSMXB.MX']]

    return global_tickers


def descarga_precios(tickers, fechas):
    inicio = time.time()
    # descarga de yahoofinance
    data = yf.download(tickers, start="2017-08-21", end="2020-08-24", actions=False,
                       group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)

    print('se tardo', round(time.time() - inicio, 2), 'segundos')

    # convertir columna de fechas y utilizar unicamente precio de cierre
    data_close = pd.DataFrame({i: data[i]['Close'] for i in tickers})
    # utilizar solo las fechas de interes
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(fechas)))
    # localizar todos los precios (encontrar todos los precios de cada mes)
    precios = data_close.loc[data_close.index.astype(str).isin(ic_fechas)]
    # acomodar en orden alfanumerico las columnas (tickers)
    precios = precios.reindex(sorted(precios.columns), axis=1)

    return precios

