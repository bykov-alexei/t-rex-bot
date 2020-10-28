from skimage.measure import label, regionprops

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


def find_field(screen, threshold=lambda x: 0.95, find_field=field_by_size):
    b = binarize(screen, threshold=threshold)
    field_bbox = find_field(b)
    field = screen[field_bbox[0]:field_bbox[2], field_bbox[1]:field_bbox[3]]
    return field
    

if __name__ == '__main__':
    screen = plt.imread('screen.png')
    gr = find_field(screen)
    plt.imsave('gr.png', gr, cmap='gray')