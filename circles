import matplotlib.pyplot as plt

# Coordinates for the centers of the circles
x = [0, 0]
y = [0, 2]

# Create the plot
fig, ax = plt.subplots()

# Draw the circles
circle1 = plt.Circle((x[0], y[0]), 0.2, color='blue', fill=True)
circle2 = plt.Circle((x[1], y[1]), 0.2, color='green', fill=True)

# Add circles to the plot
ax.add_patch(circle1)
ax.add_patch(circle2)

# Draw the connecting line
ax.plot(x, y, color='black', linewidth=2)

# Set limits and aspect ratio
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 3)
ax.set_aspect('equal')
ax.axis('off')  # Hide axes

# Show the plot
plt.show()