from fastapi import FastAPI, UploadFile, File, HTTPException
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()


model = YOLO("./models/best.pt")

@app.get("/")
def home():
    return {"message": "FastAPI is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    contents = await file.read()

    image = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
        status_code=400,
        detail="Could not decode the uploaded image"
        )

    results = model(image)

    result = results[0]

    predictions = []

    for cls, conf, box in zip(
        result.boxes.cls,
        result.boxes.conf,
        result.boxes.xyxy
    ):

        class_name = model.names[int(cls)]
        confidence = round(float(conf), 2)
        box_coordinates = {
            "x1": round(float(box[0])),
            "y1": round(float(box[1])),
            "x2": round(float(box[2])),
            "y2": round(float(box[3]))
        }

        predictions.append({
            "class": class_name,
            "confidence": confidence,
            "box": box_coordinates
        })

    return {
        "filename": file.filename,
        "predictions": predictions
    }