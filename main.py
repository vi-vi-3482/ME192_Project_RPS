from QR_codes.QR_Read import *
from rps_logic import *
import logging
import franka_python

def main():
    cam = WebcamStream(display=True, src=4)
    cam.run()

    contoller = franka_python.RobotControl()

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

        if len(sorted_qr_codes['rps_cards']) >= 0:
            cards = [Cards(item[0], item[1], transform_matrix) for item in sorted_qr_codes['rps_cards']]
            for card in cards:
                print(card.card_name)
                print(card.mapped_centre)
        else:
            cards = None
            print("no card played")

        if len(cards) == 1:
            card = cards[0]

            to_play = match_card(card.card_name)

            block = None
            for b in blocks:
                if b.block_name == to_play:
                    block = b


            contoller.pick_place(*block.mapped_centre)

            print("complete")
            break

        else:
            print("no or wrong number of cards played")

if __name__ == "__main__":
    main()