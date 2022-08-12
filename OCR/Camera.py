import cv2


def Camera():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(1)
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
