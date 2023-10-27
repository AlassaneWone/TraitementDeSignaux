import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from skimage.draw import polygon_perimeter
from skimage.measure import label, regionprops
from scipy.signal import correlate2d, convolve2d
from skimage.feature import canny

nbr_de_formes = 0

image = plt.imread('./shapes.jpg')

img = rgb2gray(image)
canny_edges = canny(img, sigma=1)

label_img = label(canny_edges)
regions = regionprops(label_img)

fig, (ax0, ax1, ax2, ax3) = plt.subplots(1, 4, figsize=(20, 4))

for props in regions:
    nbr_de_formes += 1

    y0, x0 = props.centroid
    coords = polygon_perimeter(np.array(props.coords)[:, 0], np.array(props.coords)[:, 1])
    label_img[coords[0], coords[1]] = 1

    excentricite = props.eccentricity
    print(f"Forme {nbr_de_formes}: Excentricité = {excentricite}")

    plt.text(x0, y0, str(nbr_de_formes), color='r', fontsize=12, ha='center', va='center')

ax0.imshow(image)
ax1.imshow(img, cmap='gray')
ax2.imshow(canny_edges, cmap='gray')
ax3.imshow(label_img, cmap='gray')

for a in (ax0, ax1, ax2, ax3):
    a.axis('off')

plt.show()

print(nbr_de_formes)

