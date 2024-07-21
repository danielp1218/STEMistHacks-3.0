import math

from ultralytics import YOLO
import cv2
import time
from dataclasses import dataclass
from torch import Tensor

# Load the YOLOv8 model
model = YOLO("best.pt")

vid = cv2.VideoCapture(0)


@dataclass
class Stats:
    energy: float
    hunger: float
    mood: str
    in_camera: bool


time_since_last = time.time_ns()


def time_elapsed():
    global time_since_last
    elapsed = time.time_ns() - time_since_last
    time_since_last = time.time_ns()
    return elapsed/1000000000


class BackgroundRunner:
    def __init__(self):
        self.model = YOLO("best.pt")
        self.vid = cv2.VideoCapture(0)
        t, self.frame = self.vid.read()
        self.prev_point = None
        self.stats = Stats(energy=0, hunger=0, mood="happy", in_camera=True)

    def run_main(self):
        while True:
            self.frame = self.vid.read()[1]
            results = self.model.track(self.frame, persist=True)
            annotated_frame = results[0].plot()
            if results[0].boxes:
                self.in_camera = True
                box = Tensor.cpu(results[0].boxes.xywh).numpy()
                box = box[0]
                midPoint = (int(box[0]), int(box[1]))
                tDelta = time_elapsed()
                if self.prev_point is not None:
                    instantaneousEnergy = math.sqrt(
                        pow(midPoint[0] - self.prev_point[0], 2) + pow(midPoint[1] - self.prev_point[1], 2))
                    instantaneousEnergy = pow(math.atan(instantaneousEnergy) / math.pi * 4.6403712297, 3) # magic number
                    self.stats.energy = (self.stats.energy + instantaneousEnergy * tDelta) / (
                                tDelta + 1)
                self.prev_point = midPoint

                if box[2]*box[3] > results[0].frame.shape[0]*results[0].frame.shape[1]/2:
                    self.stats.hunger -= tDelta
                else:
                    self.stats.hunger += tDelta/60
                cv2.putText(annotated_frame, "Energy: " + str(self.stats.energy), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
            else:
                self.prev_point = None
                self.stats.in_camera = False
            cv2.imshow("YOLO Tracking", annotated_frame)
            cv2.waitKey(1)


runner = BackgroundRunner()
runner.run_main()
