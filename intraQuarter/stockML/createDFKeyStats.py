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
path = "/Users/Coronado/Dropbox/stockML"


   
def Key_Stats(variables_keyStats=["Total Debt/Equity",
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

    """
    Continene todas las variables que utilizaremos en el data set. Todas se encuentran en yahoo finance 
    dentro de la infromación para cada acción en la pestaña de Key_stats

    """
    
    statspath = path+'/_KeyStats'  #Carpeta con la información de key stats de yahoo finance
    stock_list = [x[0] for x in os.walk(statspath)] 
   
    """
    Lista de todas las carpetas que contienen la información para cada una de las empresas. 
    Cada carpeta contiene varios archivos html para diferentes dias.
    Estos archivos html nos daran todos los datos que necesitamos para aplicar aprendizaje de maquina
    """
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
    sp500_df es un DataFrame que se descarga de Quadle y contienen el index S&P500. 
    Utilizaremos esta infromación por dia para compararla con el precio de cada accion para cada
    fecha. De esta manera podemos identificar si el precio de la acción supero el mercado para una
    fecha determinada.

    """
    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    ticker_list = []

    for dir_carpeta_accion in stock_list[1:]: #para cada directorio(html dir) de cada accion
        carpeta_accion = os.listdir(dir_carpeta_accion)
        ticker = dir_carpeta_accion.split("\\")[1]
        ticker_list.append(ticker)
        print('ticker')
        starting_stock_value = False
        starting_sp500_value = False

        
        if len(carpeta_accion) > 0:
            for nombre_archivo in carpeta_accion:
                date_stamp = datetime.strptime(nombre_archivo, '%Y%m%d%H%M%S.html') #convertimo la fecha que se encuentra en el nombre del documento
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = dir_carpeta_accion+'/'+nombre_archivo
                html_source = open(full_file_path,'r').read()  #Leemos el archivo html
                try:
                    value_list = []

                    for variableKS in variables_keyStats:  #La variable que vamos a buscar en el HTML
                        try:
                            regex = re.escape(variableKS) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            value = re.search(regex, html_source)
                            value = (value.group(1))

                            """
                            Lo que hace regex es buscar en el HTML un patron
                            VARIABLE + [empiece con cualquier cosa][Digito][.][otroDigito][puedeHaberoNO-MB] o [NA][puedeHaberoNO-%][</td>]

                            """

                            if "B" in value: #Convertimos a numero las señales de billones y millones
                                value = float(value.replace("B",''))*1000000000

                            elif "M" in value:
                                value = float(value.replace("M",''))*1000000

                            value_list.append(value)
                            
                            
                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)
                            #Pueden existir otros patrones en el HTML pero los omitiremos porque estos no serán muchos

                    
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    """
                    Buscaremos la fecha en el archivo sp500_df. 
                    A diferencia de los archivos HTML, la base de datos del indexSP500 no contempla los fines de semana.
                    Cuando tengamos un archivo html en fines de semana lo que haremos será tomar el dia del viernes

                    """

                    try:
                        #Estock price tiene un formato diferente por lo que sera bucado aparte
                        stock_price = float(html_source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        #    <span id="yfs_l10_afl">43.27</span>
                        try:
                            #Se proponen varias maneras en las que podría presentarse el stock_price en el HTML
                            stock_price = (html_source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price = float(stock_price.group(1))

                            #print(stock_price)
                        except Exception as e:
                            try:
                                stock_price = (html_source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                                stock_price = float(stock_price.group(1))
                            except Exception as e:
                                print(str(e),'a;lsdkfh',file,ticker)

                            #print('Latest:',stock_price)

                            #print('stock price',str(e),ticker,file)
                            #time.sleep(15)
                        
                    #print("stock_price:",stock_price,"ticker:", ticker)
                    """
                    Queremos saber si nuestras variables superaron el mercado.
                    Para esto tomamos en cambio porcentual en el index y lo comparamos con el cambio porcentual de 
                    nuestra accion. Si la acción aumento mas que proporcionalmente que el mercado entonces le 
                    asignaremos la etiqueta outperform, en caso contrario sera asinado como underperform.
                    """
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    
                    difference = stock_p_change-sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"


                    if value_list.count("N/A") > 0:
                        pass #omitimos agregar datos con un NA
                    else:
                        
                        #Agregaremos todas nuestras busquedas y variables al DF principal.
                        df = df.append({'Date':date_stamp,
                                            'Unix':unix_time,
                                            'Ticker':ticker,
                                            
                                            'Price':stock_price,
                                            'stock_p_change':stock_p_change,
                                            'SP500':sp500_value,
                                            'sp500_p_change':sp500_p_change,
                                            'Difference':difference,
                                            'DE Ratio':value_list[0],
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
                    pass



    df.to_csv("key_stats.csv") #GUARDAMOS