import segno

grid_corners = [(0, 0), (1, 0), (0, 1), (1, 1)]
rps_blocks = ("rock_block", "paper_block", "scissor_block")
rps_cards = ("rock_card", "paper_card", "scissor_card")


for i, v in enumerate(grid_corners):
    qrcode = segno.make_qr(str(v))
    qrcode.save(f"grid_corners_{v}.png", scale=10, dark="darkblue")


for i, v in enumerate(rps_blocks):
    qrcode = segno.make_qr(str(v))
    qrcode.save(f"rps_{v}.png", scale=10, dark="darkred")

for i, v in enumerate(rps_cards):
    qrcode = segno.make_qr(str(v))
    qrcode.save(f"rps_card_{v}.png", scale=10, dark="darkgreen")
