# -*- coding: utf-8 -*-
import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

import re



#path = "C:\Users\ACORONADN\Desktop\stockML\intraQuarter"
path = "/Users/Coronado/Desktop/Git/Alejandro-Coronado/intraQuarter"

def Key_Stats(gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                        'Enterprise Value',
                        'Forward P/E',
                        'PEG Ratio',
                        'Enterprise Value/Revenue',
                        'Enterprise Value/EBITDA',
                        'Revenue',
                        'Gross Profit',
                        'EBITDA',
                        'Net Income Avl to Common ',
                        'Diluted EPS',
                        'Earnings Growth',
                        'Revenue Growth',
                        'Total Cash',
                        'Total Cash Per Share',
                        'Total Debt',
                        'Current Ratio',
                        'Book Value Per Share',
                        'Cash Flow',
                        'Beta',
                        'Held by Insiders',
                        'Held by Institutions',
                        'Shares Short (as of',
                        'Short Ratio',
                        'Short % of Float',
                        'Shares Short (prior ']):
    

    
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]



    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 ##############
                                 'DE Ratio',
                                 'Trailing P/E',
                                 'Price/Sales',
                                 'Price/Book',
                                 'Profit Margin',
                                 'Operating Margin',
                                 'Return on Assets',
                                 'Return on Equity',
                                 'Revenue Per Share',
                                 'Market Cap',
                                 'Enterprise Value',
                                 'Forward P/E',
                                 'PEG Ratio',
                                 'Enterprise Value/Revenue',
                                 'Enterprise Value/EBITDA',
                                 'Revenue',
                                 'Gross Profit',
                                 'EBITDA',
                                 'Net Income Avl to Common ',
                                 'Diluted EPS',
                                 'Earnings Growth',
                                 'Revenue Growth',
                                 'Total Cash',
                                 'Total Cash Per Share',
                                 'Total Debt',
                                 'Current Ratio',
                                 'Book Value Per Share',
                                 'Cash Flow',
                                 'Beta',
                                 'Held by Insiders',
                                 'Held by Institutions',
                                 'Shares Short (as of',
                                 'Short Ratio',
                                 'Short % of Float',
                                 'Shares Short (prior ',                                
                                 ##############
                                 'Status'])

    """
    Continene todas las variables que utilizaremos en el data set. Todas se encuentran en yahoo finance 
    dentro de la infromacion para cada accion en la pestaña de Keystats
    """    
    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    
    """
    No todos los precios se encuentran ajustados. La empresas puedem reducir el precio
    de sus acciones y aumentar la cantidad para tener un mayor numero de acciones
    disponibles. Esto no quiere decir que el valor de la empresa disminuya.

    Para solucionar este problema agregaremos el precio de cierre de cada firma
    obtenidos de Quandl utilizando el codigo quandlAPI.py
    """    

    stock_df = pd.DataFrame.from_csv("stock_prices.csv")

    ticker_list = []

    for dir_carpeta_accion in stock_list[1:]:
        print('DIR CARPETA ACCIOM: {}'.format(dir_carpeta_accion))
        carpeta_accion = os.listdir(dir_carpeta_accion)
        ticker = dir_carpeta_accion.split("/")[-1]
        ticker_list.append(ticker)

##        starting_stock_value = False
##        starting_sp500_value = False

        
        if len(carpeta_accion) > 0:
            for file in carpeta_accion:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = dir_carpeta_accion+'/'+file
                html_source = open(full_file_path,'r').read()
                try:
                    value_list = []

                    for variable in gather:
                        try:
                            #print('XX1')
                            regex = re.escape(variable) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?'
                            value = re.search(regex, html_source)
                            value = (value.group(1))


                            """
                            Lo que hace regex es buscar en el HTML un patron
                            VARIABLE + [empiece con cualquier cosa][Digito][.][otroDigito][puedeHaberoNO-MB] o [NA][puedeHaberoNO-%][</td>]

                            """

                            if "B" in value:
                                value = float(value.replace("B",''))*1000000000

                            elif "M" in value:
                                value = float(value.replace("M",''))*1000000

                            value_list.append(value)
                            #print('XX2')
                            
                        except Exception as e:
                            print('Exception NA {}    FILE:   {}'.format(e, file))
                            value = "N/A"
                            value_list.append(value)
                    
                    """
                    Buscaremos la fecha en el archivo sp500_df. 
                    A diferencia de los archivos HTML, la base de datos del indexSP500 no contempla los fines de semana.
                    Cuando tengamos un archivo html en fines de semana lo que haremos será tomar el dia del viernes

                    """
                            
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except Exception as e:
                        #print('Exception 1 FIN DE SEMANA : {}'.format(e))
                        try:
                            sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row["Adjusted Close"])
                        except Exception as e:
                            print('Exception 2')
                            print("fapsdolkfhasf;lsak",str(e))


                    one_year_later = int(unix_time + 31536000)

                    try:
                        sp500_1y = datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_1y)]
                        sp500_1y_value = float(row["Adjusted Close"])
                    except:
                        #print('Exception 3')
                        try:
                            sp500_1y = datetime.fromtimestamp(one_year_later-259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_1y)]
                            sp500_1y_value = float(row["Adjusted Close"])
                        except Exception as e:
                            print('Exception 3.1')
                            print("sp500 1 year later issue",str(e))



                    try:
                        stock_price_1y = datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df.index == stock_price_1y)][ticker.upper()]
                        

                        stock_1y_value = round(float(row),2)
##                        print(stock_1y_value)
##                        time.sleep(1555)
                    
                    except Exception as e:
                        #print('Exception 4')
                        try:
                            stock_price_1y = datetime.fromtimestamp(one_year_later-259200).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df.index == stock_price_1y)][ticker.upper()]
                            stock_1y_value = round(float(row),2)
                        except Exception as e:
                            print('Exception 5')
                            print("stock price:",str(e))



                    """
                    En esta parte se ejecuta la sustitucion de precios de Yahoo finance por los de 
                    stock_price.csv ajustados por Quandl.

                    """
                    try:
                        stock_price = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df.index == stock_price)][ticker.upper()]
                        stock_price = round(float(row),2)
                    
                    except Exception as e:
                        #print('Exception 6: FIN DE SEMANA {}'.format(e))
                        try:
                            stock_price = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df.index == stock_price)][ticker.upper()]
                            stock_price = round(float(row),2)
                        except Exception as e:
                            print('Exception 7')
                            print("stock price:",str(e))


                    """
                    Queremos saber si nuestras variables superaron el mercado.
                    Para esto tomamos en cambio porcentual en el index y lo comparamos con el cambio porcentual de 
                    nuestra accion. Si la acción aumento mas que proporcionalmente que el mercado entonces le 
                    asignaremos la etiqueta outperform, en caso contrario sera asinado como underperform.
                    """

                    stock_p_change = round((((stock_1y_value - stock_price) / stock_price) * 100),2)
                    sp500_p_change = round((((sp500_1y_value - sp500_value) / sp500_value) * 100),2)

                    
                    difference = stock_p_change-sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"


                    if value_list.count("N/A") > 15:
                        pass
                    else:
                        

                        df = df.append({'Date':date_stamp,
                                            'Unix':unix_time,
                                            'Ticker':ticker,
                                            
                                            'Price':stock_price, #Proviene de otro source
                                            'stock_p_change':stock_p_change, #Proviene de otro source
                                            'SP500':sp500_value, #Proviene de otro source
                                            'sp500_p_change':sp500_p_change,  #Proviene de otro source
                                            'Difference':difference, #Proviene de otro source
                                            'DE Ratio':value_list[0], #DATOS en HTML
                                            #'Market Cap':value_list[1],
                                            'Trailing P/E':value_list[1],
                                            'Price/Sales':value_list[2],
                                            'Price/Book':value_list[3],
                                            'Profit Margin':value_list[4],
                                            'Operating Margin':value_list[5],
                                            'Return on Assets':value_list[6],
                                            'Return on Equity':value_list[7],
                                            'Revenue Per Share':value_list[8],
                                            'Market Cap':value_list[9],
                                             'Enterprise Value':value_list[10],
                                             'Forward P/E':value_list[11],
                                             'PEG Ratio':value_list[12],
                                             'Enterprise Value/Revenue':value_list[13],
                                             'Enterprise Value/EBITDA':value_list[14],
                                             'Revenue':value_list[15],
                                             'Gross Profit':value_list[16],
                                             'EBITDA':value_list[17],
                                             'Net Income Avl to Common ':value_list[18],
                                             'Diluted EPS':value_list[19],
                                             'Earnings Growth':value_list[20],
                                             'Revenue Growth':value_list[21],
                                             'Total Cash':value_list[22],
                                             'Total Cash Per Share':value_list[23],
                                             'Total Debt':value_list[24],
                                             'Current Ratio':value_list[25],
                                             'Book Value Per Share':value_list[26],
                                             'Cash Flow':value_list[27],
                                             'Beta':value_list[28],
                                             'Held by Insiders':value_list[29],
                                             'Held by Institutions':value_list[30],
                                             'Shares Short (as of':value_list[31],
                                             'Short Ratio':value_list[32],
                                             'Short % of Float':value_list[33],
                                             'Shares Short (prior ':value_list[34],
                                            'Status':status},
                                           ignore_index=True)
                except Exception as e:
                    print('Exception 0')
                    pass


    df.to_csv("key_stats_acc_perf_WITH_NA.csv")
    

Key_Stats()
    

