import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import numpy as np 
import cv2 
from extra_functions import perspect_transform, color_thresh, rover_coords

# Read in the sample image
image = mpimg.imread('IMG/robocam_2017_07_08_20_28_09_991.jpg')

# Rover yaw values will come as floats from 0 to 360 
# Fenerate a random value in this range
rover_yaw = np.random.random(1) * 360
# Will need to convert to radians before adding to pixel_angles

# Generate a random rover position in world rover_coords# Position values will range from 20 to 18- to
# to avoid the edges in a 200 x 200 pixel world
rover_xpos = np.random.random(1) * 160 + 20
rover_ypos = np.random.random(1) * 160 + 20

# Since we've chosen random numbers for yaw and position
# multiple run of the code will result in different outputs each time.

# Define a function to apply a rotation to pixel positions
def rotate_pix(xpix, ypix, yaw):
	# TODO
	# Convert Yaw to radians
	yaw_rad = rover_yaw * np.pi/180
	# Apply a rotation
	xpix_rotated = xpix * np.cos(yaw_rad) - ypix * np.sin(yaw_rad)
	ypix_rotated = xpix * np.sin(yaw_rad) + ypix * np.cos(yaw_rad)
	# Return the result
	return xpix_rotated, ypix_rotated

# Define a function to perform a translation
def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale):
	# TO DO:
	# Apply a scaling and a translation
	xpix_translated = np.int_(xpos + (xpix_rot / scale))
	ypix_translated = np.int_(ypos + (ypix_rot / scale))
	return xpix_translated, ypix_translated

# Degine a function to apply rotation and translation ( and clipping)
# Once I define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
	# Apply rotation
	xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
	# Apply translation
	xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
	# Clip the world_size
	x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
	y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
	# Return the result
	return x_pix_world, y_pix_world

# Perform warpin and color thresholding
######
# Degine calibration box in source (actual) and destination (desired) coordinates
# These source and destination points are defined to warp the image
# to a grid where each 10x10 square represents 1 square meter
dst_size = 5
# Set a bottom offset to account for the fact that the bottom of the image
# is not the position of the rover but a bit in front of it
bottom_offset = 6
source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])
warped = perspect_transform(image, source, destination)
colorsel = color_thresh(warped, rgb_thresh=(160, 160, 160))
# Extract nabigable terrain pixels
xpix, ypix = rover_coords(colorsel)
# Generate 200x200 pixel worldmap
worldmap = np.zeros((200,200))
scale = 10
# Get navigable pixel positions in world coords
x_world, y_world = pix_to_world(xpix, ypix, rover_xpos, rover_ypos, rover_yaw, worldmap.shape[0], scale)
# Add pixel positions to worldmap
worldmap[y_world, x_world] += 1
print('Xpos = ', rover_xpos, 'Ypos = ', rover_ypos, 'Yaw = ', rover_yaw)
# Plot the map in rover-centric coords

f, (ax1, ax2) = plt.subplots(1,2, figsize=(14,7))
f.tight_layout()
ax1.plot(xpix, ypix, '.')
ax1.set_title('Rover Space', fontsize = 40)
ax1.set_ylim(-160, 160)
ax1.set_xlim(0, 160)
ax1.tick_params(labelsize=20)

ax2.imshow(worldmap, cmap='gray')
ax2.set_title('World Space', fontsize=40)
ax2.set_ylim(0, 200)
ax2.tick_params(labelsize=20)
ax2.set_xlim(0, 200)

plt.subplots_adjust(left=0.1, right=1, top=0.9, bottom=0.1)
plt.show()






