from QR_codes.QR_Read import *
from rps_logic import *

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

if __name__ == "__main__":
    main()