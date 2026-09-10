# Bangladeshi Taka Note Detection API

## Project Overview

This project deploys a trained **YOLOv11 Bangladeshi Taka note detection model** as a REST API using **FastAPI** and **Docker**.

The API accepts an image of a Bangladeshi currency note, performs object detection using the trained YOLOv11 model, and returns the detected denomination, confidence score, and bounding-box coordinates in JSON format.

This project was developed as part of **Module 17: Deployment of Bangladeshi Taka Note Detection Model Using REST API & Docker**.

---

## Features

* YOLOv11 model integration
* Single-image currency note detection
* REST API using FastAPI
* Image upload through `/predict`
* JSON prediction response
* Confidence scores
* Bounding-box coordinates
* Invalid file validation
* Dockerized application
* Swagger/OpenAPI API documentation
* CPU-based inference

---

## Technologies Used

* **Python 3.11**
* **YOLOv11**
* **Ultralytics**
* **FastAPI**
* **Uvicorn**
* **OpenCV**
* **NumPy**
* **Docker**

---

## Project Structure

```text
Bangladeshi-Money-Detection-API/
│
├── app/
│   ├── model.py
│   └── test_model.py
│
├── models/
│   └── best.pt
│
├── test_images/
│   ├── test_image_1.jpeg
│   ├── test_image_2.jpeg
│   ├── test_image_3.jpeg
│   ├── test_image_4.jpeg
│   ├── test_image_5.jpeg
│   ├── test_image_6.jpeg
│   ├── test_image_7.jpeg
│   ├── test_image_8.jpg
│   ├── test_image_9.jpg
│   └── test_image_10.jpg
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

> `env/`, `__pycache__/`, and other unnecessary local files should not be included in the GitHub repository.

---

# 1. Model Integration & Inference

The trained YOLOv11 model from the previous phase is stored in:

```text
models/best.pt
```

The model is loaded in `main.py` using Ultralytics:

```python
from ultralytics import YOLO

model = YOLO("./models/best.pt")
```

The API performs inference on an uploaded image and extracts:

* Detected denomination
* Confidence score
* Bounding-box coordinates

The bounding box is returned using:

```text
x1
y1
x2
y2
```

---

# 2. REST API

The application uses **FastAPI** to expose the trained model through a REST API.

## Endpoint

```text
POST /predict
```

## Input

The endpoint accepts an image file.

Supported image types include common formats such as:

* JPEG
* JPG
* PNG

The uploaded image is sent as a multipart form-data file.

## Example Request

```text
POST http://localhost:8000/predict
```

with the image supplied as the `file` field.

---

## Example Response

For example, when `test_image_7.jpeg` is uploaded, the API returns:

```json
{
  "filename": "test_image_7.jpeg",
  "predictions": [
    {
      "class": "1000_Tk",
      "confidence": 0.96,
      "box": {
        "x1": 52,
        "y1": 215,
        "x2": 1589,
        "y2": 870
      }
    }
  ]
}
```

### Response Fields

| Field        | Description                            |
| ------------ | -------------------------------------- |
| `filename`   | Name of the uploaded image             |
| `class`      | Detected Bangladeshi Taka denomination |
| `confidence` | Model confidence score                 |
| `box.x1`     | Left coordinate of bounding box        |
| `box.y1`     | Top coordinate of bounding box         |
| `box.x2`     | Right coordinate of bounding box       |
| `box.y2`     | Bottom coordinate of bounding box      |

---

# 3. Input Validation

The API checks whether the uploaded file is an image.

For example, if a PDF or another non-image file is uploaded, the API returns an HTTP `400 Bad Request` response:

```json
{
  "detail": "File must be an image"
}
```

The API also handles cases where the uploaded image cannot be decoded.

---

# 4. Running the API Locally

## Step 1: Clone the Repository

Clone this repository to your computer:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Then navigate into the project directory:

```bash
cd Bangladeshi-Money-Detection-API
```

---

## Step 2: Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv env
```

Activate it on Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

---

## Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Step 4: Start the FastAPI Server

Run:

```bash
uvicorn main:app --reload
```

The API should then be available at:

```text
http://localhost:8000
```

---

# 5. API Documentation

FastAPI automatically provides interactive API documentation.

After starting the server, open:

```text
http://localhost:8000/docs
```

The Swagger UI can be used to test the `/predict` endpoint by uploading an image.

---

# 6. Dockerization

The application is containerized using Docker so that the API, dependencies, and trained model can run in an isolated environment.

## Dockerfile

The Dockerfile:

1. Uses Python 3.11
2. Creates the application working directory
3. Installs required Linux libraries
4. Installs Python dependencies
5. Copies the FastAPI source code
6. Copies the trained YOLO model
7. Exposes port `8000`
8. Starts the FastAPI application using Uvicorn

---

## Build the Docker Image

From the project root directory, run:

```bash
docker build -t taka-detection-api .
```

This creates a Docker image named:

```text
taka-detection-api
```

---

## Run the Docker Container

Run:

```bash
docker run -p 8000:8000 taka-detection-api
```

The API will then be accessible from the host machine at:

```text
http://localhost:8000
```

---

## Test the Dockerized API

Open:

```text
http://localhost:8000/docs
```

Then:

1. Open `POST /predict`
2. Click **Try it out**
3. Select an image
4. Click **Execute**
5. View the JSON response

---

# 7. Dockerized API Example

The Dockerized application was successfully tested using:

```text
test_image_7.jpeg
```

The model detected:

```text
Class: 1000_Tk
Confidence: 0.96
```

with the following bounding box:

```text
x1 = 52
y1 = 215
x2 = 1589
y2 = 870
```

Example JSON response:

```json
{
  "filename": "test_image_7.jpeg",
  "predictions": [
    {
      "class": "1000_Tk",
      "confidence": 0.96,
      "box": {
        "x1": 52,
        "y1": 215,
        "x2": 1589,
        "y2": 870
      }
    }
  ]
}
```

---

# 8. Testing & Validation

The API is intended to be tested using multiple Bangladeshi Taka note images.

For the assignment evaluation, multiple test images are used to verify:

* Correct denomination detection
* Confidence score generation
* Bounding-box generation
* JSON response structure
* API input validation
* Dockerized inference

Additional testing results and screenshots are included in the accompanying project documentation.

---

# 9. API Response Format

The general response structure is:

```json
{
  "filename": "image_name.jpeg",
  "predictions": [
    {
      "class": "denomination",
      "confidence": 0.00,
      "box": {
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0
      }
    }
  ]
}
```

This format allows the client application to easily access the detected denomination, confidence score, and location of the detected note.

---

# 10. Error Handling

The API provides appropriate responses for invalid input.

### Non-image file

HTTP Status:

```text
400 Bad Request
```

Response:

```json
{
  "detail": "File must be an image"
}
```

### Invalid image data

HTTP Status:

```text
400 Bad Request
```

Response:

```json
{
  "detail": "Could not decode the uploaded image"
}
```

### Missing file

FastAPI automatically validates the required file parameter and returns an appropriate HTTP validation response.

---

# 11. Docker Commands Summary

### Build

```bash
docker build -t taka-detection-api .
```

### Run

```bash
docker run -p 8000:8000 taka-detection-api
```

### Check running containers

```bash
docker ps
```

### Stop a running container

```bash
docker stop <CONTAINER_ID>
```

### View Docker images

```bash
docker images
```

---

# 12. Assignment Requirements Completed

The project covers the main requirements of the assignment:

* [x] YOLOv11 model integration
* [x] Single-image inference
* [x] Detection classes
* [x] Confidence scores
* [x] Bounding-box coordinates
* [x] FastAPI REST API
* [x] `POST /predict` endpoint
* [x] Image file input
* [x] JSON output
* [x] Invalid input handling
* [x] Dockerfile
* [x] Python dependencies
* [x] Model weights included
* [x] Docker image successfully built
* [x] Docker container successfully executed
* [x] API accessible from host machine
* [x] API successfully tested inside Docker

---

# 13. Future Improvements

Possible future improvements include:

* Cloud deployment using AWS, Azure, GCP, Railway, or Render
* Authentication and authorization
* Batch image prediction
* Improved API response metadata
* Confidence threshold configuration
* Web-based frontend for uploading currency images
* Performance optimization for production deployment

---

# 14. Author

**Sadman Wasee**

Computer Science & Engineering

North South University

---

## License

This project was developed for educational and academic purposes.
