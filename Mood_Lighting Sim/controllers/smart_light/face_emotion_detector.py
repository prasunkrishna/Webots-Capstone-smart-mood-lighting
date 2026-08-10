import cv2
import json
import time
import joblib
import numpy as np

# LOAD MODEL
model = joblib.load("face_model.pkl")
scaler = joblib.load("face_scaler.pkl")

print("Model loaded successfully")
print("Model expects", model.n_features_in_, "features")

emotion_file = "face_emotion_output.json"

LIGHT_UPDATE_INTERVAL = 5
last_light_update = time.time()

# FACE DETECTOR
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# WEBCAM
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access webcam")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        # Resize to training size
        face = cv2.resize(face, (48, 48))

        # Normalize
        face = face.astype("float32") / 255.0

        # Flatten
        features = face.flatten()

        # Reshape
        features = features.reshape(1, -1)

        # Scale
        features = scaler.transform(features)

        # Predict emotion
        emotion = model.predict(features)[0]

        probabilities = model.predict_proba(features)
        confidence = np.max(probabilities) * 100

        print(
            f"Emotion: {emotion} | "
            f"Confidence: {confidence:.2f}%"
        )
        
        # Draw box
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"{emotion} ({confidence:.1f}%)",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Update Webots every 2 mins
        if time.time() - last_light_update >= LIGHT_UPDATE_INTERVAL:

            with open(emotion_file, "w") as f:
                json.dump(
                    {
                        "emotion": emotion,
                        "confidence": float(confidence)
                    },
                    f
                )

            print("Emotion sent to Webots")

            last_light_update = time.time()

    cv2.imshow("Face Emotion Detection", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()