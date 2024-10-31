from qreader import QReader
import cv2


#%%
qreader = QReader()
image = cv2.cvtColor(cv2.imread("corner test rectangle.png"), cv2.COLOR_BGR2RGB)

results = qreader.detect_and_decode(image, return_detections=True)

print(results)