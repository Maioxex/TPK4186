import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import Ships as sh
import containerlist as cl

ship = sh.ships(1, 18, 22, 23)
# print("step")
listo = cl.createRandomContainerList(3000)
# print(listo.getContainerListLength())
# print("step")
ship.loadShipWithContainerList(listo)
# print("step")
weights = np.zeros((18, 22, 23))
grid = ship.getGrid()
print(ship.getSize())
for i in range(ship.getSize()[0]):
    for j in range(ship.getSize()[1]):
        for k in range(ship.getSize()[2]):
            if grid[i][j][k] != 0:
                weights[i][j][k] = grid[i][j][k].getTotalWeight()
weights = np.transpose(weights)
ship.printShipLoadToFile()
print(ship.calculateShipTotalWeight())
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
# from containerlist import containerlist as cl
# from Ships import ships as sh
# from Containers import container as co


# Generate some random data for the voxel plot

#data = np.ones((23, 22, 18))
#data = np.random.rand(23, 22, 18)
# data[:,:,10] = 0
# Generate some random weights for the boxes
#weights = np.random.rand(23, 22, 18)

# Define the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the scaling of the axes to elongate the boxes in the x direction
ax.set_box_aspect((2, 1, 1))

# Define the color map for the weights, with red corresponding to high weights and green corresponding to low weights
cmap = plt.cm.get_cmap('RdYlGn_r')

# Normalize the weights to the range of the colormap
norm = plt.Normalize(weights.min(), weights.max())

# Convert the weights to colors using the colormap and normalization
colors = cmap(norm(weights))

# Plot the voxel data with elongated and color-coded boxes
ax.voxels(weights, facecolors=colors, edgecolor='k')

# Set the axis labels and title
ax.set_xlabel('L')
ax.set_ylabel('W')
ax.set_zlabel('H')
ax.set_title('3D Voxel Plot with Elongated and Color-Coded Boxes')

# Show the plot
plt.show()
