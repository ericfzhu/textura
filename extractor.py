from PIL import Image
import numpy as np
from collections import Counter


def extract_palette(image_file_path: str) -> list:
    '''Opens an image file and retrieves its palette.'''
    try:
        with Image.open(image_file_path) as image:
            # Extract the palette
            palette = image.getpalette()
    except FileNotFoundError:
        print(f"Cannot open {image_file_path}")
        return None
    except OSError:
        print(f"Cannot extract palette from {image_file_path}")
        return None
    return palette


def filter_palette(palette: list, num_colors: int) -> list:
    '''Returns the most prominent colors from the image palette.'''
    # Convert the color palette to a list
    palette_list = np.array(palette).reshape(-1, 3).tolist()
    # Count the number of occurrences of each color
    color_counts = Counter(tuple(rgb) for rgb in palette_list)
    # Get the most common colors
    most_common_colors = color_counts.most_common(num_colors)
    # Convert RGB tuples back to ints
    filtered_palette = [tuple(int(value) for value in item[0]) for item in most_common_colors]
    return filtered_palette


def main() -> None:
    image_file_path = '6bc36493-8ade-4dae-8507-527f903642fb.jpg'
    palette = extract_palette(image_file_path)
    if palette is None:
        print(f'Error: Unable to extract palette from {image_file_path}')
        return

    filtered_palette = filter_palette(palette, 5)

    # Display filtered palette
    print(filtered_palette)


if __name__ == '__main__':
    main()
