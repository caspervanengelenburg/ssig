import numpy as np
from matplotlib.cm import get_cmap
import matplotlib.colors as mcolors

# some nice colors
delft_color = "#00A6D6" # TU Delft light blue color
google_colors = ["#4285F4", # blue
                 "#DB4437", # red
                 "#F4B400", # yellow
                 "#0F9D58"  # green
                 ]


# Custom coloring schemes
COLORS_ROOMTYPE = ['#1f77b4',  # living room
                   '#e6550d',  # master room
                   '#fd8d3c',  # kitchen
                   '#fdae6b',  # bathroom
                   '#fdd0a2',  # dining room
                   '#72246c',  # child room
                   '#5254a3',  # study room
                   '#6b6ecf',  # second room
                   '#2ca02c',  # guest room
                   '#37c837',  # balcony
                   '#1f77b4',  # entrance
                   '#98df8a',  # storage
                   '#d62728',  # walk-in
                   '#e6e6e6',  # external area
                   '#000000',  # exterior wall
                   '#000000',  # front door
                   '#000000',  # interior wall
                   '#ffffff']  # interior door

ROOM_ARRAY_TOGETHER = [[0],
                       [1, 5, 7, 8], # bedroom
                       [2],
                       [3],
                       [4],
                       [6],
                       [9],
                       [10],
                       [11],
                       [12],
                       [13],
                       [14],
                       [15],
                       [16],
                       [17]]

COLORS_ROOMTYPE_REDUC = ['#1f77b4',  # living room
                         '#e6550d',  # bedroom
                         '#fd8d3c',  # kitchen
                         '#fdae6b',  # bathroom
                         '#fdd0a2',  # dining room
                         '#5254a3',  # study room
                         '#37c837',  # balcony
                         '#1f77b4',  # entrance
                         '#98df8a',  # storage
                         '#d62728',  # walk-in
                         '#e6e6e6',  # external area
                         '#000000',  # exterior wall
                         '#000000',  # front door
                         '#000000',  # interior wall
                         '#ffffff']  # interior door

# Color maps
COLOR_MAP_ROOMTYPE = mcolors.ListedColormap(COLORS_ROOMTYPE)
CMAP_ROOMTYPE = get_cmap(COLOR_MAP_ROOMTYPE)

COLOR_MAP_ROOMTYPE_REDUC = mcolors.ListedColormap(COLORS_ROOMTYPE_REDUC)
CMAP_ROOMTYPE_REDUC = get_cmap(COLOR_MAP_ROOMTYPE_REDUC)


# Entity categories and associated classes
CATEGORIES = ["living room",
              "master room",
              "kitchen",
              "bathroom",
              "dining room",
              "child room",
              "study room",
              "second room",
              "guest room",
              "balcony",
              "entrance",
              "storage",
              "walk-in",
              "external area",
              "exterior wall",
              "front door",
              "interior wall",
              "interior door"]

CLASSES = np.arange(0, len(CATEGORIES))


# Roots
DATA_PATH = r'C:\Users\caspervanengel\OneDrive\Documents\PHD\1_data\rplan\0-full'