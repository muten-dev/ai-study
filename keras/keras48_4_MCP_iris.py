import time
from icecream import ic
from sklearn.datasets import load_iris
import numpy as np

datasets = load_iris()
x = datasets.data
y = datasets.target

# ic(datasets.feature_names)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    train_size=0.75,
                                                    shuffle=True,
                                                    random_state=12)
ic(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)  # (batch_size, timesteps, feature)
x_test = x_test.reshape(-1, x_test.shape[1], 1)
ic(x_train.shape, x_test.shape)

#2. 모델 구성
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Input, Conv1D, Flatten, Dropout, GlobalAveragePooling1D, MaxPooling1D

# model = Sequential()
# model.add(Conv1D(filters=32, kernel_size=2, padding='same', activation='relu', input_shape=(4, 1)))
# model.add(Dropout(0.2))
# model.add(Conv1D(32, 2, padding='same', activation='relu'))
# model.add(MaxPooling1D())
# model.add(Conv1D(64, 2, padding='same', activation='relu'))
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(1))

# 3. 컴파일, 훈련
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
es = EarlyStopping(monitor='val_loss', patience=20, mode='min', verbose=1)
cp = ModelCheckpoint(monitor='val_loss', save_best_only=True, mode='auto', 
                     filepath='./_save/ModelCheckPoint/keras48_4_MCP_iris.hdf5')

start_time = time.time()
# model.compile(loss='mse', optimizer='adam')
# model.fit(x_train, y_train, epochs=100, batch_size=8, verbose=2, validation_split=0.2, callbacks=[es, cp])
duration_time = time.time() - start_time

# model.save('./_save/ModelCheckPoint/keras48_4_MCP_iris.h5')
# model = load_model('./_save/ModelCheckPoint/keras48_4_MCP_iris.h5')   # save_model
model = load_model('./_save/ModelCheckPoint/keras48_4_MCP_iris.hdf5')  # CheckPoint

# 4. 평가, 예측
loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)  # x_test를 훈련시킨 값으로
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)  # y_test와 y_predict값을 통해 결정계수를 계산

ic(duration_time)
ic(loss)
ic(r2)


'''
LSTM
ic| duration_time: 2.649158477783203
ic| loss: 0.03157087042927742
ic| r2: 0.9530984163662419

Standard Conv1D
ic| duration_time: 1.7096083164215088
ic| loss: 0.025716209784150124
ic| r2: 0.9617960855952423

save_model_h5
ic| duration_time: 2.1433565616607666
ic| loss: 0.030738042667508125
ic| r2: 0.954335661156702

load_model_h5
ic| duration_time: 0.0
ic| loss: 0.030738042667508125
ic| r2: 0.954335661156702

ModelCheckPoint_hdf5
ic| duration_time: 0.0
ic| loss: 0.04404949024319649
ic| r2: 0.9345602261176371
'''