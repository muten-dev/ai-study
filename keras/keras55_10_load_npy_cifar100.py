import numpy as np

x_train = np.load('./_save/_npy/k55_10_x_train_data_cifar100.npy')
y_train = np.load('./_save/_npy/k55_10_y_train_data_cifar100.npy')
x_test = np.load('./_save/_npy/k55_10_x_test_data_cifar100.npy')
y_test = np.load('./_save/_npy/k55_10_y_test_data_cifar100.npy')

# print(type(x_data), type(y_data))   # <class 'numpy.ndarray'> <class 'numpy.ndarray'>
print(x_train, y_train)
print(x_train.shape, y_train.shape)

print(x_test, y_test)
print(x_test.shape, y_test.shape)