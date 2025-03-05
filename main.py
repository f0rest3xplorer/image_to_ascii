from PIL import Image
import numpy as np
import shutil
import argparse
import os

# Create argument parser
parser = argparse.ArgumentParser(description="Process an image file for ASCII conversion.")

# Add file argument (must be a valid path)
parser.add_argument("file", type=str, help="Path to the image file")

# Parse arguments
args = parser.parse_args()

# Check if the file exists
if not os.path.isfile(args.file):
    print(f"Error: File '{args.file}' not found.")
    exit(1)

# print(f"Using file: {args.file}")

chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
max_pixel_value = 255

def ask_filter():
    filter = input(f'Which filter would you like to use? Average(a), Lightness(l), Luminosity(lum): ')
    if filter == 'a':
        filter = 'average'
    elif filter == 'l':
        filter = 'lightness'
    elif filter == 'lum':
        filter = 'luminosity'
    return filter

def resize_image(img, new_width=100):
    width, height = img.size
    aspect_ratio = height / width  # Calculate original aspect ratio
    new_height = int(new_width * aspect_ratio * 0.45)  # Adjust for character proportions
    resized_img = img.resize((new_width, new_height))
    return resized_img

# Get terminal width and set image width accordingly
terminal_width = shutil.get_terminal_size().columns
image_width = terminal_width  # Adjust as needed

# Open and resize image
img = Image.open(args.file)
img = resize_image(img, new_width=image_width)

# Save 2-D Pixel Array
pixel_array = np.array(img)

# Convert pixel matrix to brightness matrix

def brightness_matrix(pixel_array, filter='average'):
    brightness_matrix = []
    for row in pixel_array:
        intensity_row = []
        for p in row:
            if filter == 'average':
                intensity = ((p[0] + p[1] + p[2]) / 3.0)
            if filter == 'lightness':
                intensity = (max(p) + min(p)) / 2.0
            if filter == 'luminosity':
                intensity = (0.21 * p[0]) + (0.72 * p[1]) + (0.07 * p[2])
            intensity_row.append(intensity)
        brightness_matrix.append(intensity_row)
    return brightness_matrix



#convert to ascii

def convert_to_ascii(brightness, chars):
    ascii_matrix = []
    for row in brightness:
        ascii_row = []
        for p in row:
            ascii_row.append(chars[int(p/max_pixel_value * len(chars)) - 1])
        ascii_matrix.append(ascii_row)

    return(ascii_matrix)

def print_ascii_matrix(ascii_matrix):
    for row in ascii_matrix:
        line = "".join(row)  
        print(line)  

filter = ask_filter()
brightness = brightness_matrix(pixel_array, filter)
ascii = convert_to_ascii(brightness, chars)
print_ascii_matrix(ascii)






