from ultralytics import YOLO

# Load trained model
model = YOLO("models/best.pt")

# Run inference
results = model("test_images/test_image_5.jpeg")

# Get first result
result = results[0]

# Print detections
for cls, conf, box in zip(
    result.boxes.cls,
    result.boxes.conf,
    result.boxes.xyxy
):
    class_id = int(cls)
    confidence = float(conf)
    x1, y1, x2, y2 = box.tolist()

    class_name = model.names[class_id]

    print(f"Class: {class_name}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Bounding Box: [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")
    print("-" * 40)

# Save annotated image
result.save(filename="outputs/20_taka_prediction.jpg")

print("Prediction image saved successfully.")