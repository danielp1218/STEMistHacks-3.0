import asyncio
import math

from torch import Tensor
from ultralytics import YOLO
import cv2
from fastapi import FastAPI, WebSocket
from dataclasses import dataclass
import time
import base64

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

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            self.frame = self.vid.read()[1]
            results = self.model.track(self.frame, persist=True)
            annotated_frame = results[0].plot()
            if results[0].boxes:
                self.stats.in_camera = True
                box = Tensor.cpu(results[0].boxes.xywh).numpy()
                box = box[0]
                midPoint = (int(box[0]), int(box[1]))
                if self.prev_point is not None:
                    instantaneousEnergy = math.sqrt(
                        pow(midPoint[0] - self.prev_point[0], 2) + pow(midPoint[1] - self.prev_point[1], 2))
                    instantaneousEnergy = pow(math.atan(instantaneousEnergy) / math.pi * 4.6403712297, 3) # magic number
                    tDelta = time_elapsed()
                    self.stats.energy = (self.stats.energy + instantaneousEnergy * tDelta) / (
                                tDelta + 1)
                self.prev_point = midPoint
                cv2.putText(annotated_frame, "Energy: " + str(self.stats.energy), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
            else:
                self.prev_point = None
                self.stats.in_camera = False


runner = BackgroundRunner()
app = FastAPI()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(runner.run_main())


@app.websocket("/camera")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        #change to png
        frame = cv2.imencode('.png', runner.frame)[1]
        await websocket.send_bytes(frame.tobytes())
        await asyncio.sleep(1)


@app.websocket("/stats")
async def get_stats(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({"energy": runner.stats.energy, "hunger": runner.stats.hunger, "mood": runner.stats.mood, "in_camera": runner.stats.in_camera})
        await asyncio.sleep(1)
