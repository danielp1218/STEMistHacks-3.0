from ultralytics import YOLO
import torch

model = YOLO("yolov9s.pt")
result = model.train(data="data.yaml", epochs=100, batch=8, imgsz=640, device=0)
model.export()
