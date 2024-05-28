from sklearn.model_selection import train_test_split # type: ignore
from tensorflow.keras.models import Sequential, load_model, save_model # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from keras.config import enable_unsafe_deserialization # type: ignore 

import numpy as np
import json


class BinaryToAverageModel:
    def __init__(self):
        self.model = None

    def create_model(self, input_shape):
        model = Sequential([
            Dense(64, input_shape=input_shape, activation='relu'),
            Dense(64, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model

    def train_model(self, X_train, y_train, epochs=100, batch_size=32, validation_data=None):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=validation_data)

    def evaluate_model(self, X_test, y_test):
        loss = self.model.evaluate(X_test, y_test)
        print("Test Loss:", loss)

    def save_model(self, filepath=r"neural_model\binary_to_average_model.keras"):
        save_model(self.model, filepath)

    def load_model(self, filepath=r"neural_model\binary_to_average_model.keras"):
        self.model = load_model(filepath)

    def predict(self, binary_representations):
        padded_binary_representations = pad_sequences([[int(bit) for bit in binary] for binary in binary_representations],
                                                     maxlen=self.model.input_shape[1], padding='post')
        predictions = self.model.predict(padded_binary_representations)
        return predictions.flatten()

def load_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data