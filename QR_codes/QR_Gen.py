import segno

grid_corners = [(0, 0), (1, 0), (0, 1), (1, 1)]

for i, v in enumerate(grid_corners):
    qrcode = segno.make_qr(str(v))
    qrcode.save("grid_corners_%d.png" % i)

rps = ("rock", "paper", "scissor")

for i, v in enumerate(rps):
    qrcode = segno.make_qr(str(v))
    qrcode.save("rps_%d.png" % i)