from matplotlib import image
import matplotlib.pyplot as plt

img = image.imread('./image')

pts = np.array([[862.91217,1353.319336], [913.697632,1438.639648]])
plt.scatter(pts[:, 0], pts[:, 1], marker='x', color='red', s=200)
plt.show()


