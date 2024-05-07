from PIL import Image
import tkinter as tk


def change_icon_color(img_obj, target_color, tk_controller):

    # Convert color to rgb
    target_color =  convert_tk_col_to_rgb(target_color, tk_controller)

    img_obj = img_obj.convert('RGBA')  # Open the source image and convert it to RGBA mode
    data = img_obj.getdata()  # Load the image data into a list

    # Create a new data list
    new_data = []

    # Replace black color with the desired target color
    for item in data:
        # Change all black (also shades of blacks) pixels to the target color
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((target_color[0], target_color[1], target_color[2], item[3]))
        else:
            new_data.append(item)  # Original color and alpha

    # Update image data
    img_obj.putdata(new_data)

    return img_obj


def convert_tk_col_to_rgb(tk_color, tk_controller):
    return tuple(c // 256 for c in tk_controller.winfo_rgb(color=tk_color))  # Needs the controller unfortunately
