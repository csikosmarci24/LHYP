from numpy import loadtxt
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt

dataset = loadtxt('data.csv', delimiter=',')

X_train = dataset[:600,0:6]
y_train = dataset[:600,6]
X_test = dataset[600:,0:6]
y_test = dataset[600:,6]

model = Sequential()
model.add(Dense(9, input_dim=6, activation='relu', kernel_regularizer=keras.regularizers.l1()))
model.add(Dense(6, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)))
model.add(Dense(1, activation='sigmoid', kernel_regularizer=keras.regularizers.l1_l2(0.01)))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=150, batch_size=10)

# y_pred = model.predict(X_test)
# pred = list()
# for i in range(len(y_pred)):
#     pred.append(np.argmax(y_pred[i]))
# test = list()
# for i in range(len(y_test)):
#     test.append(np.argmax(y_test[i]))

# a = accuracy_score(pred,test)
# print('Accuracy is:', a*100)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()