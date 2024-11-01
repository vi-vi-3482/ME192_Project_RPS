import segno

grid_corners = [(0, 0), (1, 0), (0, 1), (1, 1)]

for i, v in enumerate(grid_corners):
    qrcode = segno.make_qr(str(v))
    qrcode.save("grid_corners_%d.png" % i, scale=30)

rps_blocks = ("rock", "paper", "scissor")
rps_cards = ("rock_card", "paper_card", "scissor_card")

for i, v in enumerate(rps_blocks):
    qrcode = segno.make_qr(str(v))
    qrcode.save("rps_%d.png" % i, scale=30)

for i, v in enumerate(rps_cards):
    qrcode = segno.make_qr(str(v))
    qrcode.save("rps_%d.png" % i, scale=30)