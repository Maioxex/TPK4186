import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
# from containerlist import containerlist as cl
# from Ships import ships as sh
# from Containers import container as co


# Generate some random data for the voxel plot

data = np.ones((23, 22, 18))
#data = np.random.rand(23, 22, 18)
data[:,:,10] = 0
# Generate some random weights for the boxes
weights = np.random.rand(23, 22, 18)

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
ax.voxels(data, facecolors=colors, edgecolor='k')

# Set the axis labels and title
ax.set_xlabel('L')
ax.set_ylabel('W')
ax.set_zlabel('H')
ax.set_title('3D Voxel Plot with Elongated and Color-Coded Boxes')

# Show the plot
plt.show()
