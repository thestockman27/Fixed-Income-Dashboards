import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
import pandas as pd
import quandl as ql
import numpy as np

# Replace 'YOUR_API_KEY' with your Quandl API key
ql.ApiConfig.api_key = 'FMezMmR86K7axszB_rkz'

# Fetch U.S. Treasury yield data
yield_ = ql.get("USTREASURY/YIELD")

# Subsample the data to reduce image size
#yield_ = yield_.iloc[::5, :]  # Adjust the step value as needed
yield_ = yield_.iloc[(len(yield_)-300):, :] 
# Extract relevant data for 3D plotting
time_values = pd.to_datetime(yield_.index)[::-1]  # Reverse the order
tenors = range(len(yield_.columns))


# Create a 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Create a meshgrid for tenors and time
T, T_ = np.meshgrid(tenors, range(len(time_values)))

# Plot the 3D surface
surf = ax.plot_surface(T, T_, yield_.values[::-1, :], cmap='viridis', edgecolor='k', linewidth=0.5)


# Customize the plot
ax.set_xlabel('Tenors')
ax.set_ylabel('Time')
ax.set_zlabel('Yields')
ax.set_title('U.S. Treasury Yield Surface Over Time')

# Add a colorbar
cbar = fig.colorbar(surf, ax=ax, orientation='vertical', shrink=0.8, aspect=10)

# Add sliders for rotation angles
axcolor = 'lightgoldenrodyellow'
ax_rot_x = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_rot_y = plt.axes([0.1, 0.06, 0.65, 0.03], facecolor=axcolor)
slider_rot_x = Slider(ax_rot_x, 'X Rotation', 0, 360, valinit=30)
slider_rot_y = Slider(ax_rot_y, 'Y Rotation', 0, 360, valinit=30)

def update(val):
    ax.view_init(elev=slider_rot_x.val, azim=slider_rot_y.val)
    fig.canvas.draw_idle()

slider_rot_x.on_changed(update)
slider_rot_y.on_changed(update)

plt.show()
