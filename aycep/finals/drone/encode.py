import base64

with open('daksh1.jpg', 'rb') as f:
    image = base64.b64encode(f.read())
    
with open('outputoutput', 'wb') as f:
    f.write(image)
