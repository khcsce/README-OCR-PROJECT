# https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array
# https://stackoverflow.com/questions/18310152/sending-binary-data-over-sockets-with-python
# stock photo from Shutterstock

from PIL import Image
import io
import math
import matplotlib.pyplot as plt

# image max size is 6 MB uncompressed
def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  # image.save(imgByteArr, 'JPEG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

img = Image.open('stock_photo.jpg', mode='r')
byteArr = image_to_byte_array( img )
print( len(byteArr) )
print( byteArr[-1] )
numPackets = math.ceil(len(byteArr) / 4096)

import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('computer', 8080))
try:
  client.send('I am CLIENT'.encode())
  client.send(('NUM_PACKETS: %i' % numPackets).encode())
  for i in range(numPackets - 1):
    # client.send( imgByteArr[i*4096 :  
    from_server = client.recv(4096).decode()
  client.send('stop'.encode())
finally:
  client.close()
  print(from_server)
