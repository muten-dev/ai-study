import numpy as np 
from icecream import ic
from tensorflow.keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    vertical_flip=False,
    width_shift_range=.1,
    height_shift_range=.1,
    rotation_range=10,
    zoom_range=.5,
    shear_range=.5,
    fill_mode='nearest'
)

# train_datagen = ImageDataGenerator(
#     rescale=1./255,
# )

# 1 ImageDataGenerator를 정의
# 2 파일에서 가져오려면 -> flow_from_directory()    // x, y가 tuple 형태로 뭉쳐있음
# 3 데이터에서 땡겨오려면 -> flow()                 // x, y가 나뉘어있음

augment_size = 100000 - x_train.shape[0]

randidx = np.random.randint(x_train.shape[0], size=augment_size)
ic(x_train.shape[0])     # ic| x_train.shape[0]: 50000000
ic(randidx)              # ic| randidx: array([20648, 10982,  9502, ..., 29041, 11683, 16800])
ic(randidx.shape)        # ic| randidx.shape: (50000,)0000,)

x_augmented = x_train[randidx].copy()
y_augmented = y_train[randidx].copy()

ic(x_augmented.shape)    # (40000, 28, 28)

x_augmented = x_augmented.reshape(x_augmented.shape[0], x_train.shape[1], x_train.shape[2], x_train.shape[3] if x_train.shape[3] else 1)
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], x_train.shape[3] if x_train.shape[3] else 1)
x_test = x_test.reshape(x_test.shape[0], x_train.shape[1], x_train.shape[2], x_train.shape[3] if x_train.shape[3] else 1)

x_augmented = train_datagen.flow(
    x_augmented, 
    np.zeros(augment_size),
    batch_size=augment_size, 
    shuffle=False,
    # save_to_dir='d:/temp/'
).next()[0]

# ic(x_augmented.shape)   # (40000, 28, 28, 1)
print(x_augmented[0][0].shape)   # (40000, 28, 28, 1)
print(x_augmented[0][1].shape)   # (40000, 28, 28, 1)
print(x_augmented[0][1][:10])   # (40000, 28, 28, 1)
print(x_augmented[0][1][10:15])   # (40000, 28, 28, 1)
# iterator 구조로 인해 next가 있을 때는 해당 객체가 실행 될 때마다 save_to_dir이 실행 되는 것으로 보임

print(x_train.shape)
print(x_augmented.shape)
x_train = np.concatenate((x_train, x_augmented))
y_train = np.concatenate((y_train, y_augmented))

ic(x_train.shape, y_train.shape)    # (100000, 28, 28, 1), (100000, 1)

# Data preprocessing
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1] * x_train.shape[2] * x_train.shape[3])
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1] * x_test.shape[2] * x_test.shape[3])
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

ic('********* 1st reshape **********')
ic(x_train.shape, x_test.shape)
ic(y_train.shape, y_test.shape)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

ic('********* Scaling **********')
ic(x_train.shape, x_test.shape)
x_train = x_train.reshape(-1, 32 * 32, 3)
x_test = x_test.reshape(-1, 32 * 32, 3)

ic('********* 2nd reshape **********')
ic(x_train.shape, x_test.shape)


# from sklearn.preprocessing import OneHotEncoder
# oneEnc = OneHotEncoder()
# y_train = oneEnc.fit_transform(y_train).toarray()
# y_test = oneEnc.transform(y_test).toarray()

# ic('********** OneHotEnc **********')
# ic(y_train.shape, y_test.shape)

#2. Model
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, Conv1D, Flatten, Dropout, GlobalAveragePooling1D, MaxPooling1D

model = Sequential()
model.add(Conv1D(filters=32, kernel_size=2, padding='same', activation='relu', input_shape=(32 * 32, 3)))
model.add(Dropout(0.2))
model.add(Conv1D(32, 2, padding='same', activation='relu'))
model.add(MaxPooling1D())
model.add(Conv1D(64, 2, padding='same', activation='relu'))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(10, activation='softmax'))

#3 Compile, Train
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])

from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', patience=10, mode='min', verbose=1)

import time
start_time = time.time()
model.fit(x_train, y_train, epochs=10, batch_size=512, verbose=2, 
          validation_split=0.15, callbacks=[es])
duration_time = time.time() - start_time

#4 Evaluate
loss = model.evaluate(x_test, y_test)   # evaluate -> return loss, metrics

ic(duration_time)
ic(loss[0])
ic(loss[1])

'''
ic| duration_time: 703.9444949626923
ic| loss[0]: 1.3177965879440308
ic| loss[1]: 0.5913000106811523
'''