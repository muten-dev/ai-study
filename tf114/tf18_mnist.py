from keras.datasets import mnist
import numpy as np
import tensorflow as tf
from sklearn import preprocessing
from sklearn.metrics import accuracy_score


tf.set_random_seed(66)

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(x_train.shape, y_train.shape)  # (60000, 28, 28) (60000,)
print(x_test.shape, y_test.shape)  # (10000, 28, 28) (10000,)

# print(y_train)

x_train = x_train.reshape(-1, 28*28)/255
x_test = x_test.reshape(-1, 28*28)/255
y_train = y_train.reshape(-1, 1)
y_test = y_test.reshape(-1, 1)

print(x_train.shape, y_train.shape)  # (60000, 784) (60000, 1)
print(x_test.shape, y_test.shape)  # (10000, 784) (10000, 1)

onehot_enc = preprocessing.OneHotEncoder()
y_train = onehot_enc.fit_transform(y_train).toarray()
y_test = onehot_enc.fit_transform(y_test).toarray()

print(y_train.shape)    # (60000, 10)

# 2. 모델 구성
x = tf.compat.v1.placeholder(tf.float32, shape=[None, 28*28])
y = tf.compat.v1.placeholder(tf.float32, shape=[None, 10])

# Output Layer
w = tf.Variable(tf.random.normal([28*28, 10]), name='weight')
b = tf.Variable(tf.random.normal([10]), name='bias')

# hyppthesis = x * w + b
hypothesis = tf.nn.softmax(tf.matmul(x, w) + b)

# loss = tf.reduce_mean(tf.square(hypothesis-y)) # mse
# loss = -tf.reduce_mean(y*tf.math.log(hypothesis)+(1-y)*tf.math.log(1-hypothesis))  # binary_crossentropy
# categorical_crossentropy
loss = tf.reduce_mean(-tf.reduce_sum(y * tf.math.log(hypothesis), axis=1))

# optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)
train = tf.train.AdamOptimizer(learning_rate=0.011).minimize(loss)

with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())

    for epochs in range(301):
        import time
        st = time.time()
        _, loss_val = sess.run([train, loss], feed_dict={
                               x: x_train, y: y_train})
        et = time.time() - st
        if epochs % 20 == 0:
            print(round(et, 4), 's, Epoch', epochs, 'loss', loss_val)
    predicted = sess.run(hypothesis, feed_dict={x: x_test})
    y_pred = np.argmax(predicted, axis=1)
    y_test = np.argmax(y_test, axis=1)
    print('accuracy_score: ', accuracy_score(y_test, y_pred))
