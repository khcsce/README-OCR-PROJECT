import socket               # Import socket module
import cv2


def Camera():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(filename='saved_img.jpg', img=frame)
                webcam.release()
                img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
                img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
                gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                img_ = cv2.resize(gray, (28, 28))
                img_resized = cv2.imwrite(
                    filename='saved_img-final.jpg', img=img_)
                break
            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                exit()
        except(KeyboardInterrupt):
            webcam.release()
            cv2.destroyAllWindows()
            break


# Camera()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()  # Get local machine name
host_ip = socket.gethostbyname(host)
port = 12345                 # Reserve a port for your service.

s.connect((host_ip, port))

#s.send("Hello server!")
f = open('saved_img.jpg', 'rb')
print('Sending...')
l = f.read(4096)
while (l):
    print('Sending...')
    s.send(l)
    l = f.read(4096)
f.close()
print("Done Sending")
# print(s.recv(4096))
s.close                     # Close the socket when done
