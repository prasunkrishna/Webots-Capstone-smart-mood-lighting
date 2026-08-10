import numpy as np
import pickle
import json
import time

model = pickle.load(open("va_model.pkl", "rb"))
scaler = pickle.load(open("va_scaler.pkl", "rb"))

emotion_file = "physio_emotion_output.json"


def va_to_emotion(valence, arousal):
    if valence > 0.4 and arousal > 0.5:
        return "happy"

    elif valence < -0.3 and arousal > 0.6:
        return "angry"

    elif valence < -0.3 and arousal < 0.5:
        return "sad"

    else:
        return "neutral"


while True:
    # Simulated physiological signals
    heart_rate = np.random.normal(80, 10)
    gsr = np.random.normal(0.6, 0.1)
    temperature = np.random.normal(36.7, 0.2)

    print("\nPhysiological Signals")
    print("Heart Rate:", round(heart_rate, 2))
    print("GSR:", round(gsr, 3))
    print("Temperature:", round(temperature, 2))

    X = [[heart_rate, gsr, temperature]]
    X = scaler.transform(X)

    # Predict Valence & Arousal
    valence, arousal = model.predict(X)[0]

    print("Valence:", round(valence, 2))
    print("Arousal:", round(arousal, 2))

    # Convert VA to emotion
    emotion = va_to_emotion(valence, arousal)

    # Confidence score calculation
    confidence = (abs(valence) + arousal) / 2
    confidence = max(0, min(confidence, 1)) * 100

    print("Detected Emotion:", emotion)
    print("Confidence Score:", round(confidence, 2), "%")

    # Send emotion to Webots
    with open(emotion_file, "w") as f:
        json.dump({
            "emotion": emotion,
            "confidence": float(confidence)
        }, f)

    print("Emotion sent to Webots")

    time.sleep(10)