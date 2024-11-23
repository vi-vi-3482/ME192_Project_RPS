import math
from qreader import QReader
import cv2
import numpy as np
import multiprocessing as mp

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
                matched.append([item, detected[index]])
        qr_codes[name] = matched

    return qr_codes

def get_image(capture):
    result, image = capture.read()
    return image

class WebcamStream:
    def __init__(self, src=0, display=False):
        self.capture = cv2.VideoCapture(src)
        if not self.capture.isOpened():
            raise ValueError("Error: Could not open webcam.")
        self.result, self.frame = self.capture.read()
        self.stopped = False
        self.display = display
        self.frame_queue = mp.Queue(maxsize=1)

    def start(self):
        # Start the frame capture in a separate process
        self.capture_process = mp.Process(target=self.update)
        self.capture_process.start()

    def update(self):
        while not self.stopped:
            if self.capture.isOpened():
                self.result, self.frame = self.capture.read()
                if not self.frame_queue.full():
                    self.frame_queue.put(self.frame)

    def stop(self):
        self.stopped = True
        self.capture_process.terminate()
        self.capture.release()

    def show_camera(self):
        while not self.stopped:
            frame = self.frame_queue.get()
            cv2.imshow("webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.stop()

    def run(self):
        self.start()
        if self.display:
            # Start the show_camera process
            self.display_process = mp.Process(target=self.show_camera)
            self.display_process.start()

def centres_of_qr(detected):
    centres = []
    for i, v in enumerate(detected):
        centres.append(v['cxcy'])

    centres = [(int(round(x)), int(round(y))) for x, y in centres]

    centroid_x = sum(x for x, y in centres) / len(centres)
    centroid_y = sum(y for x, y in centres) / len(centres)

    def angle_from_centroid(point):
        x, y = point
        return math.atan2(y - centroid_y, x - centroid_x)

    centres = sorted(centres, key=angle_from_centroid)
    centres = np.array([centres], dtype=np.float32)

    return centres

def perspective_transform(centres, image):
    width, height = 1000, 1000  # these need to be set to match the franka workspace
    dst_points = np.array([
        (0, 0),
        (width - 1, 0),
        (width - 1, height - 1),
        (0, height - 1)
    ], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(centres, dst_points)

    warped_image = cv2.warpPerspective(image, matrix, (width, height))

    return matrix, warped_image

class Blocks:
    def __init__(self, decoded, detected, matrix):
        self.block_name = decoded
        self.block_data = detected
        self.centre = centres_of_qr([self.block_data])
        self.mapped_centre = map_centres(self.centre, matrix)

class Cards:
    def __init__(self, decoded, detected, matrix):
        self.card_name = decoded
        self.card_data = detected
        self.centre = centres_of_qr([self.card_data])
        self.mapped_centre = map_centres(self.centre, matrix)

def map_centres(centres, matrix):
    centres = np.array(centres, dtype=np.float32)

    transformed_point = cv2.perspectiveTransform(centres, matrix)

    return transformed_point

def run_camera(display=False):
    cam = WebcamStream(display=display)
    cam.run()

def detect(cam):
    image = cam.frame_queue.get()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    decoded, detected = read_qr_code(image)

    print(decoded)

    sorted_qr_codes = sort_codes(decoded, detected, qr_strings)

    plane_edges = centres_of_qr([item[1] for item in sorted_qr_codes['grid_corners']])
    transform_matrix, transform_image = perspective_transform(plane_edges, image)

    blocks = [Blocks(item[0], item[1], transform_matrix) for item in sorted_qr_codes['rps_blocks']]

    return blocks

def main():

    cam = WebcamStream(display=True, src=4)
    cam.run()

    while True:
        while True:
            image = cam.frame_queue.get()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            decoded, detected = read_qr_code(image)

            # print(decoded)

            sorted_qr_codes = sort_codes(decoded, detected, qr_strings)
            if len(sorted_qr_codes['grid_corners']) == 4 :
                break

        try:
            plane_edges = centres_of_qr([item[1] for item in sorted_qr_codes['grid_corners']])
        except:
            continue
        transform_matrix, transform_image = perspective_transform(plane_edges, image)
        if len(sorted_qr_codes['rps_blocks']) >= 0 :
            blocks = [Blocks(item[0], item[1], transform_matrix) for item in sorted_qr_codes['rps_blocks']]
        for block in blocks:
            print(block.block_name)
            print(block.mapped_centre)

        if len(sorted_qr_codes['rps_cards']) >= 0 :
            cards = [Cards(item[0], item[1], transform_matrix) for item in sorted_qr_codes['rps_cards']]
            for card in cards:
                print(card.card_name)
                print(card.mapped_centre)

if __name__ == "__main__":
    main()