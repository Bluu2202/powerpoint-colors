lookup = {}

for i in range(256):
    lookup[i] = {}
    for j in range(256):
        lookup[i][j] = {}
        for alpha in [0.15, 0.3, 0.5, 0.65, 0.8, 0.95]:
            new = i * alpha + j * (1 - alpha)
            if abs(new % 1 - 0.5) < 1e-6: lookup[i][j][alpha] = "Kill"
            else: lookup[i][j][alpha] = round(new)
