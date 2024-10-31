import math
from qreader import QReader
import cv2
import numpy as np

#%%
qreader = QReader()
image = cv2.cvtColor(cv2.imread("QR_codes/corner test for transform.png"), cv2.COLOR_BGR2RGB)  # change this to absolute path

decoded, detected = qreader.detect_and_decode(image, return_detections=True)

print(decoded)
print(detected)

#%%
centres = [cord["cxcy"] for cord in detected]
centres = [(int(round(x)), int(round(y))) for x, y in centres]

centroid_x = sum(x for x, y in centres) / len(centres)
centroid_y = sum(y for x, y in centres) / len(centres)
def angle_from_centroid(point):
    x, y = point
    return math.atan2(y - centroid_y, x - centroid_x)

centres = sorted(centres, key=angle_from_centroid)
centres = np.array([centres], dtype=np.float32)

#%%
cv2.polylines(image, centres, isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#%%
width, height = 500, 500
dst_points = np.array([
    (0, 0),
    (width - 1, 0),
    (width - 1, height - 1),
    (0, height - 1)
], dtype=np.float32)
matrix = cv2.getPerspectiveTransform(centres, dst_points)

warped_image = cv2.warpPerspective(image, matrix, (width, height))

cv2.imshow("Image", warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
