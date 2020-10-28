from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt


def field_by_size(B):
    lb = label(B)
    regions = list(filter(lambda x: True, regionprops(lb)))
    field = max(regions, key=lambda x: x.image.shape[0])
    return field.bbox


def binarize(screen, threshold):
    gray = 0.2125 * screen[:, :, 0] + 0.7154 * screen[:, :, 1] + 0.0721 * screen[:, :, 2]
    threshold = threshold(gray)
    binarized = (gray > threshold).astype(int)
    return binarized


def crop_field(screen, bbox, threshold=lambda x: 0.99):
    b = binarize(screen, threshold=threshold)
    if np.sum(b == 0) // np.sum(b == 1) > 2:
        screen = 1 - screen
    return screen[bbox[0]:bbox[1], bbox[2]:bbox[3]]


def find_field(screen, threshold=lambda x: 0.99, find_field_method=field_by_size):
    # Fixing fields that are black on background
    b = binarize(screen, threshold=threshold)
    if (np.sum(b == 0) // np.sum(b == 1) > 2):
        screen = 1 - screen
    
    b = binarize(screen, threshold=threshold)
    field_bbox = find_field_method(b)
    bin_field = np.logical_not(b[field_bbox[0]:field_bbox[2], field_bbox[1]:field_bbox[3]]).astype(int)
    tmp = binary_erosion(np.copy(bin_field))
    tmp = binary_erosion(tmp)
    tmp = binary_erosion(tmp).astype(int)
    y, x = np.where(tmp.astype(int) == 1)
    return field_bbox[0] + min(y) - 5, field_bbox[0] + max(y) + 5, field_bbox[1] + min(x) - 5, field_bbox[1] + max(x) + 5

def vertical_lines(image):
    lines = np.sum(image.sum(axis=0) / image.shape[0] == 1)
    return lines

def horizontal_lines(image):
    lines = np.sum(image.sum(axis=1) / image.shape[1] == 1)
    return lines

def is_game_over(field, threshold=lambda x: 0.75):
    b = binarize(field, threshold)
    regions = regionprops(label(~b))
    for region in regions:
        image = resize(region.image, (10, 10))
        vertical = vertical_lines(image)
        horizontal = horizontal_lines(image)
        if vertical == 3 and horizontal == 4:
            return True
    return False
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--game-over', action='store_true', dest='game_over')
    parser.add_argument('--file', dest='file', required=True)
    args = parser.parse_args()

    filename = args.file
    if args.game_over:
        screen = plt.imread(filename)
        field = find_field(screen)
        game_over = is_game_over(field)
        print("Game is over" if game_over else "Game isn't over")
        plt.imsave('result.png', field, cmap='gray')