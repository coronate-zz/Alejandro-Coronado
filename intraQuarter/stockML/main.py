# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
import pandas as pd
from sklearn import metrics
from sklearn import tree
from matplotlib import style
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
style.use("ggplot")


FEATURES =  ['DE Ratio',
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
             'Shares Short (prior ']

print('CARGANDO DATOS')
data_df = pd.DataFrame.from_csv("key_stats_acc_perf_NO_NA.csv")

#data_df = data_df[:100]
data_df = data_df.reindex(np.random.permutation(data_df.index))
data_df = data_df.replace("NaN",0).replace("N/A",0)
    

X = np.array(data_df[FEATURES].values)#.tolist())

y = (data_df["Status"]
         .replace("underperform",0)
         .replace("outperform",1)
         .values.tolist())

X = preprocessing.scale(X)
X_train, X_test, Y_train, Y_test = train_test_split(X, y , train_size=0.75)

print('GENERANDO MODELOS')

model = svm.SVC(kernel="linear", C= 1.0)
model.fit(X_train,Y_train)
y_model = model.predict(X_test)
print(' Capacidad de Prediccion de Modelo Lineal: ')
print(accuracy_score(Y_test, y_model))
print ('\n \tMétricas clasicas de Clasificadores: ' )
print(metrics.classification_report(y_model, Y_test))


model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, Y_train)
y_model = model.predict(X_test)

print(' Capacidad de prediccion RandomForestClassifier : ')
print(accuracy_score(Y_test, y_model))
print ('\n \tMétricas clasicas de Clasificadores: ' )
print(metrics.classification_report(y_model, Y_test))



model = tree.DecisionTreeClassifier()
model = model.fit(X_train, Y_train)
y_model = model.predict(X_test)

print(' Capacidad de prediccion Tree : ')
print(accuracy_score(Y_test, y_model))
print ('\n \tMétricas clasicas de Clasificadores: ' )
print(metrics.classification_report(y_model, Y_test))


stocks_list= np.unique( data_df['Ticker'])

"""
for each_ticker in  stocks_list:
        try:

            plot_df = data_df[(data_df['Ticker'] == each_ticker)]
            #print('P1 {}'.format( plot_df))
            plot_df = plot_df.set_index(['Date'])

            if plot_df['Status'][-1] == 'underperform':
                color = 'r'
            else:
                color = 'g'

            
            plot_df['Difference'].plot(label=each_ticker, color=color)
            plt.legend()
        except Exception as e:
            print(str(e))
plt.show()

"""

#tree.export_graphviz(model, out_file='tree.dot') 



