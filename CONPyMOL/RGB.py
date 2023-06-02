'''
 Functions and variables to manage RGB data
 Forms part of the CONPyMOL pluggin
'''

rgb_dictionary = {
    "black": (0, 0, 0),
    "blue": (0, 0, 1),
    "brown": (0.64, 0.26, 0.26),
    "green": (0, 1, 0),
    "orange": (1, 0.5, 0),
    "pink": (0.9, 0.67, 0.67),
    "red": (1, 0, 0),
    "yellow": (1, 1, 0),
    "white": (1, 1, 1),
    "purple": (0.5, 0, 0.5),
    "grey": (0.5, 0.5, 0.5)
}


# Create a function to return the RGB value of a given value between 0.0 and 1.0
def rgb(value=None, color=None):
    if value is not None:
        value = float(value)
        r = 1 - value
        g = 1 - r
        b = 0
        return (r, g, b)
    elif color is not None:
        return rgb_dictionary[color]
    else:
        print("INTERNAL ERROR: rgb() got no arguments!")
        return (1, 1, 1)
