# np.save('./_save/_npy/k59_5_train_x.npy', arr=train_gen[0][0])
# np.save('./_save/_npy/k59_5_train_y.npy', arr=train_gen[0][1])
# np.save('./_save/_npy/k59_5_valid_x.npy', arr=valid_gen[0][0])
# np.save('./_save/_npy/k59_5_valid_y.npy', arr=valid_gen[0][1])
# np.save('./_save/_npy/k59_5_test_x.npy', arr=test_gen[0][0])
# np.save('./_save/_npy/k59_5_test_y.npy', arr=test_gen[0][1])

import numpy as np
from icecream import ic
x_train = np.load('./_save/_npy/k59_5_train_x.npy')
y_train = np.load('./_save/_npy/k59_5_train_y.npy')
x_valid = np.load('./_save/_npy/k59_5_valid_x.npy')
y_valid = np.load('./_save/_npy/k59_5_valid_y.npy')
x_test = np.load('./_save/_npy/k59_5_test_x.npy')
y_test = np.load('./_save/_npy/k59_5_test_y.npy')

ic(x_train.shape)    # (2648, 150, 150, 3)
ic(y_train.shape)    # (2648,)
ic(x_valid.shape)    # (661, 150, 150, 3)
ic(y_valid.shape)    # (661,)
ic(x_test.shape)     # (3, 150, 150, 3)
ic(y_test.shape)     # (3,)

# ic(x_train[1])
# ic(x_test[1])
# ic(y_train[1])
# ic(y_test[1])

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Conv2D, MaxPooling2D, Dropout, Flatten, Dense

model = Sequential()
model.add(InputLayer(input_shape=(150, 150, 3)))
model.add(Conv2D(16, (3, 3), (1, 1), 'same', activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.5))
model.add(Conv2D(32, (3, 3), (1, 1), 'same', activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# model.summary()

model.compile(
    loss='binary_crossentropy', 
    optimizer='adam',
    metrics=['acc'],
)

from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', patience=10, mode='min', verbose=1)

hist = model.fit(
    x_train, y_train,
    epochs=50,
    steps_per_epoch=32,
    validation_steps=4,
    validation_data=(x_valid, y_valid),
    callbacks=[es]
)

acc = hist.history['acc']
val_acc = hist.history['val_acc']
loss = hist.history['loss']
val_loss = hist.history['val_loss']

ic(acc[-1])
ic(val_acc[-1])
ic(loss[-1])
ic(val_loss[-1])

y_pred = model.predict(x_test)
ic(y_pred)

for i, j in enumerate(y_pred):
    if j >= 0.5:
        chance = round(j[0]*100, 1)
        print(f'{i+1}. Classified/ WOMEN with {chance}%')
    else:
        chance = round((1-j[0])*100, 1)
        print(f'{i+1}. Classified/ MEN with {chance}%')

# ic(y_pred)
'''
ic| acc[-1]: 0.8217522501945496
ic| val_acc[-1]: 0.6096823215484619
ic| loss[-1]: 0.37846890091896057
ic| val_loss[-1]: 0.8057641386985779
ic| y_pred: array([[0.5404332 ],
                   [0.47137678],
                   [0.04922736]], dtype=float32)
1. Classified/ WOMEN with 54.0%
2. Classified/ MEN with 52.9%
3. Classified/ MEN with 95.1%
'''
'''
pred_x = []
from tensorflow.keras.preprocessing import image
test_image = image.load_img('../data/men_women/pred/00.jpg', target_size=(150, 150))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)

ic(result)
ic(result.argmax())
ic(result.shape)
'''