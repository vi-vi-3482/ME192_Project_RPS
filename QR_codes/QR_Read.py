import math
from qreader import QReader
import cv2
import numpy as np


grid_corners = ["(0, 0)", "(1, 0)", "(0, 1)", "(1, 1)"]
rps_blocks = ("rock_block", "paper_block", "scissor_block")
rps_cards = ("rock_card", "paper_card", "scissor_card")

qr_strings = [grid_corners, rps_blocks, rps_cards]

def read_qr_code(image):
    qreader = QReader()
    decoded, detected = qreader.detect_and_decode(image, return_detections=True)

    return decoded, detected


def sort_codes(decoded, detected, qr_strings):
    qr_codes = {}
    for name, categories in zip(['grid_corners', 'rps_blocks', 'rps_cards'], qr_strings):
        matched = []
        for item in categories:
            if item in decoded:
                index = decoded.index(item)
                matched.append((item, detected[index]))
        qr_codes[name] = matched

    return qr_codes

def main():
    image = cv2.cvtColor(cv2.imread("QR_codes/corner test for transform.png"), cv2.COLOR_BGR2RGB)  # change this to absolute path
    decoded, detected = read_qr_code(image)

    sorted_qr_codes = sort_codes(decoded, detected, qr_strings)

    print(sorted_qr_codes)

if __name__ == "__main__":
    main()

exit()
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
