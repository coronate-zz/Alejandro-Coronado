import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import copy
from sklearn.cross_validation import train_test_split

X= pd.read_csv("dataX.csv")
y= pd.read_csv("datay.csv")


X_train, X_test, Y_train, Y_test = train_test_split(X, y , train_size=0.75)



learning_rate = 0.01
training_epochs = 15
batch_size = 100
display_step = 1

n_hidden_1 = 10 # 1st layer number of features
n_hidden_2 = 50 # 2nd layer number of features
n_input = len(X_train.columns) # MNIST data input (img shape: 28*28)
n_classes = 1 # MNIST total classes (0-9 digits)

#x = tf.placeholder( ), [None, n_input])
#y_ = tf.placeholder("float", [None, n_classes])

x = tf.placeholder(tf.float32, [None, n_input])
y_ = tf.placeholder(tf.float32, [None, n_classes])


weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}


 # Hidden layer with RELU activation
layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
layer_1 = tf.nn.sigmoid(layer_1)
 # Hidden layer with RELU activation
layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
y = tf.nn.sigmoid(tf.matmul(layer_1, weights['out']) + biases['out'])



# Define loss and optimizer
cost = tf.reduce_mean(tf.reduce_sum((y_-y)**2)) 
optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(cost)
#train_step = tf.train.GradientDescentOptimizer(0.01).minimize(lossfn)
# Initializing the variables
init = tf.initialize_all_variables()

lossfn = tf.reduce_mean(tf.reduce_sum((y_- y)**2)) 
optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(lossfn)




sess = tf.Session() # tipo de sesion, puede ser interactiva

sess.run(init)
for i in range(5000):
  sess.run(optimizer, feed_dict={x: X_train, y_: Y_train})


results=sess.run(y, feed_dict={x: X_test, y_: Y_test})
correct_prediction = tf.equal(tf.round(y),y_) # aca estams definiendo otras operacioes

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
acc=sess.run(accuracy, feed_dict={x: X_test, y_: Y_test}) # las corremos

def rocCurve(results, Y_test):
    #fig3 = plt.figure()
    #ax3 = fig3.add_subplot(111)
    VPRlist=list()
    FPRlist=list()
    criterio=[i*.01 for i in range(101)]
    for i in criterio:
        vPositivos=list()
        fPositivos=list()
        vNegativos=list()
        fNegativos=list()
        
        print 'CRITERIO: {}'.format(i)
        aux=copy.copy(results)
        aux[results>=i]=1
        aux[results<i]=0
        print[np.sum(aux)]
        z=Y_test.values
        for j in range(len(z)):
            #print('Valor Real: {}  Valor Predecido: {}'.format(z[i], aux[i]))
            #print z[i]==aux[i]==1
            if z[j]==1: #Positivos Reales
                if aux[j]==1:#Verdadero Positivo
                    vPositivos.append(1)
                    #print('XXX')
                else: #Falsos Positivos Rechazar cuando es verdader ERROR I
                    fNegativos.append(1)
            else:
                if aux[j]==1: #Falsos Positivos aceptamos y cuando realmente es falas
                    fPositivos.append(1)
                else: #verdaderos Negativos
                    vNegativos.append(1)
        vpsum=np.sum(vPositivos)
        vnsum=np.sum(vNegativos)
        fpsum=np.sum(fPositivos)
        fnsum=np.sum(fNegativos)
        print' VP : {}   VN : {}  FP : {}  FN : {}  '.format(vpsum, vnsum, fpsum, fnsum)
        VPR=1 -np.double(vpsum)/(np.double(vpsum)+np.double(fnsum))
        #print('suma {}'.format(np.double(vpsum)+ np.double(fnsum) ))
        VPRlist.append(VPR)
        FPR=1-np.double(fpsum)/(  np.double(fpsum)+ np.double(vnsum))
        ax3.scatter(x=VPR, y=FPR)
        FPRlist.append(FPR)
        #plt.scatter(x=FPRlist, y=VPRlist)
        print 'VPR {}    FPR {}   Criterio {}'.format( VPR, FPR, i)
    #ax3.plot([x*.01 for x in range(100)], [y*.01 for y in range(100)], color='green')
    #axes.set_ylim([0,1])
    #axes.set_xlim([0,1])
    #plt.show()
    return(VPRlist, FPRlist, criterio)
       
VPRlist, FPRlist, criterio= rocCurve(results, Y_test)        


        
fig3 = plt.figure()
ax3 = fig3.add_subplot(111) 
ax3.plot([x*.01 for x in range(100)], [y*.01 for y in range(100)], color='green')
ax3.scatter(x=(VPRlist), y=(FPRlist ))
axes = plt.gca()
axes.set_ylim([0,1])
axes.set_xlim([0,1])
print('\n\n')
print( 'ACCURACY: {}'.format(acc))
print 'Hiden Leyer 1: {}    Hiden Leyer 2: {} '.format( n_hidden_1, n_hidden_2 ) 
print( 'NUMERO DE ENTRENAMIENTOS:  5000')