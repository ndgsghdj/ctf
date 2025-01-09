import requests
import base64

url = "http://34.87.84.198:8888/picture"

response = requests.get(url)

image = response.text.replace('post this image\n', '')
image = image[2:-1]

with open('image_encoded', 'wb') as f:
    f.write(image.encode())

with open('image', 'wb') as f:
    f.write(base64.b64decode(image.encode()))
