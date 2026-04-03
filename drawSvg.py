import matplotlib.pyplot as plt

# Read points from file
xs = []
ys = []
with open("naca_0018.dat") as f:
    for line in f:
        if line.strip():
            x, y = map(float, line.split())
            xs.append(x)
            ys.append(y)

# Create a clean figure
plt.figure(figsize=(6, 6))

# Plot the curve
plt.plot(xs, ys, linewidth=1)

# Remove everything visual except the line
plt.axis("off")              # hides axes, ticks, frame
plt.gca().set_aspect("equal", adjustable="box")  # equal scaling

# Tight layout so the SVG fits the curve closely
plt.margins(0)
plt.savefig("points.svg", format="svg", bbox_inches="tight", pad_inches=0)
plt.close()
