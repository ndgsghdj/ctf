from pprint import pprint
import requests
import json
import pandas as pd

# URL where the dataset is hosted
url = "https://i-lost-my-weights-web-chall.ybn.sg/dataset"

# Fetch the dataset
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Dataset fetched successfully")
else:
    print("Failed to fetch dataset")

# Parse the JSON content from the response
data = json.loads(response.text)

# Now, let's inspect the structure of the data
print(data)  # To understand the format of the dataset

# Assuming the dataset contains a nested JSON object as shown in your response
train_x = data["train_x"]
train_y = data["train_y"]
test_x = data["test_x"]

# Convert these to numpy arrays or pandas DataFrame for easy manipulation
import numpy as np

train_x = np.array(train_x)
train_y = np.array(train_y)
test_x = np.array(test_x)

# Check the extracted data
print("train_x shape:", train_x.shape)
print("train_y shape:", train_y.shape)
print("test_x shape:", test_x.shape)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Initialize and train the model
model = LogisticRegression()
model.fit(train_x, train_y)

# Get the model's coefficients (weights)
weights = model.coef_

# Make predictions on the test data
predictions = model.predict(test_x)

# Print the coefficients and predictions
print("Model weights (coefficients):", weights)
pprint(predictions)

# Convert the binary predictions to a list of bits (0 and 1)
bit_string = ''.join(map(str, predictions))

# Check if the length of the bit_string is a multiple of 8 (for complete bytes)
if len(bit_string) % 8 != 0:
    # If not, we need to pad the bit string to make it divisible by 8
    bit_string = bit_string.ljust(len(bit_string) + (8 - len(bit_string) % 8), '0')

# Now, split the bit string into chunks of 8 (each chunk is a byte)
bytes_list = [bit_string[i:i+8] for i in range(0, len(bit_string), 8)]

# Convert each byte (8 bits) to an ASCII character
ascii_string = ''.join([chr(int(byte, 2)) for byte in bytes_list])

# Print the final ASCII string
print("Recovered ASCII String:", ascii_string)
