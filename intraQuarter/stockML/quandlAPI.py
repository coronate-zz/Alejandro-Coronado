import pandas as pd
import os
import quandl as qdl
import time



auth_tok = "WUzn6PCZywWuS8iXLZB-"

path = "/Users/Coronado/Desktop/Git/Alejandro-Coronado/intraQuarter"

def Stock_Prices():
    df = pd.DataFrame()

    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    #print(stock_list)

    for stock_folder in stock_list[1:]:
        print ( "STOCK FOLDER : {} ".format(stock_folder))#.-print('TICK {}'.format(stock_folder.split("/")[-1]))
        try:
            ticker = stock_folder.split("/")[-1]
            print("\n\nTICKER: {}".format(ticker) )
            name = "WIKI/"+ticker.upper()
            data = qdl.get(name,
                              trim_start = "2000-12-12",
                              trim_end = "2014-12-30",
                              authtoken=auth_tok)


            data[ticker.upper()] = data["Adj. Close"]
            #print('DATA: {}'.format(data) )
            df = pd.concat([df, data[ticker.upper()]], axis = 1)

        except Exception as e:
            print('PRIMER Exception: '.format(str(e)))
            time.sleep(10)
            try:
                ticker = stock_folder.split("\\")[1]
                print(ticker)
                name = "WIKI/"+ticker.upper()
                data = qdl.get(name,
                                  trim_start = "2000-12-12",
                                  trim_end = "2014-12-30",
                                  authtoken=auth_tok)
                data[ticker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[ticker.upper()]], axis = 1)

            except Exception as e:
                print(str(e))
                print('SEGUNDO Exception: '.format(str(e)))

    df.to_csv("stock_prices.csv")
                
Stock_Prices()