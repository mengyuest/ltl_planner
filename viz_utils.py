import matplotlib.pyplot as plt

from matplotlib.patches import Patch, Rectangle

def viz_grid(i, j, n_grid, mode, new=False):
    if mode=="init":
        color="limegreen"
    elif mode=="house":
        color="crimson"
    elif mode=="pear":
        color="yellow"
    elif mode=="obs":
        color="saddlebrown"
    elif mode=="space":
        color="lightgray"
    if new:
        patch = Rectangle((j, n_grid-1-i), 1, 1, facecolor=color, alpha=0.8, edgecolor="gray", linewidth=1.0, label=mode)
    else:
        patch = Rectangle((j, n_grid-1-i), 1, 1, facecolor=color, alpha=0.8, edgecolor="gray", linewidth=1.0)
    ax = plt.gca()
    ax.add_patch(patch)


def viz_grid_text(i, j, n_grid, text, color):
    patch = Rectangle((j, n_grid-1-i), 1, 1, facecolor=color, alpha=0.8, edgecolor="gray", linewidth=1.0)
    ax = plt.gca()
    ax.add_patch(patch)
    plt.text(j+0.5, n_grid-1-i+0.5, text, fontsize=24,ha="center")
