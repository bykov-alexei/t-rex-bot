import mss
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

from models.RandomModel import RandomModel
from recognizer import find_field, crop_field
from uuid import uuid4 as uuid

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--monitor', dest='monitor', type=int, default=0)
parser.add_argument('--restart', action='store_true', default=True)
args = parser.parse_args()

monitor = {"left": 0, "top": 0, "width": 1920, "height": 1080}

model = RandomModel()

with mss.mss() as sct:
                 
    monitor = sct.monitors[args.monitor]

    screen = np.array(sct.grab(monitor))[:, :, :3] / 255
    bbox = find_field(screen)

    while True:
        screen = np.array(sct.grab(monitor))[:, :, :3] / 255
        field = crop_field(screen, bbox)
        model.run(field)
        if model.game_over:
            print(model.score, [model.weights[i] / sum(model.weights) for i in range(len(model.weights))])
            if not args.restart:
                exit(0)
            else:
                model = type(model)(model.name)
                time.sleep(3)
                model.start_game()
        # cv2.imshow('field', field)
        # if cv2.waitKey(25) & 0xFF == ord("q"):
        #     cv2.destroyAllWindows()
        #     break