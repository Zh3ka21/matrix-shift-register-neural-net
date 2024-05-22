import numpy as np
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.layers import Dense, Lambda # type: ignore
from keras.config import enable_unsafe_deserialization # type: ignore

class RandomNumberModel:
    def __init__(self):
        self.model = None

    def create_model(self):
        model = Sequential([
            Dense(64, input_shape=(1,), activation='relu'),
            Dense(64, activation='relu'),
            Dense(1, activation='linear'),  # Output layer for regression
            Lambda(lambda x: x % 10)  # Ensure the output is in the range [0, 10)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model

    def train_model(self):
        # Generate training data
        x_train = np.random.rand(10000, 1) * 10  # Inputs
        y_train = np.random.rand(10000, 1) * 10  # Outputs (targets)

        # Train the model
        self.model.fit(x_train, y_train, epochs=100, batch_size=32)

    def save_model(self, filepath=r"neural_model\rnm.keras"):
        self.model.save(filepath)

    def load_model(self, filepath=r"neural_model\rnm.keras"):
        enable_unsafe_deserialization()  # Enable unsafe deserialization
        self.model = load_model(filepath, compile=False)
    
    def generate_random_numbers(self, n):
        # Generate n random inputs
        x_input = np.random.rand(n, 1) * 10
        predictions = self.model.predict(x_input)

        # Ensure the output is within the range [0, 10)
        predictions = np.mod(predictions, 10)

        # Multiply to shift decimal point and convert to integers
        integer_predictions = (predictions * 10**6).astype(int)

        # Convert integers to strings without commas
        formatted_numbers = [str(num) for num in integer_predictions.flatten()]

        return formatted_numbers

