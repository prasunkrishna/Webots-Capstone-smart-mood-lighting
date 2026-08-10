import numpy as np
import joblib
import json
import time

# Load trained context model
model = joblib.load("context_model.pkl")

emotion_file = "context_emotion_output.json"

# Mappings
time_map = {"morning": 0, "afternoon": 1, "evening": 2, "night": 3}
location_map = {"home": 0, "office": 1, "outdoor": 2}
activity_map = {
    "relaxing": 0,
    "studying": 1,
    "working": 2,
    "socializing": 3,
    "alone": 4
}
env_map = {"quiet": 0, "moderate": 1, "noisy": 2}

times = list(time_map.keys())
locations = list(location_map.keys())
activities = list(activity_map.keys())
environments = list(env_map.keys())

while True:

    # Random context simulation
    time_context = np.random.choice(times)
    location = np.random.choice(locations)
    activity = np.random.choice(activities)
    environment = np.random.choice(environments)

    print("\nContext Scenario")
    print("Time:", time_context)
    print("Location:", location)
    print("Activity:", activity)
    print("Environment:", environment)

    # Feature encoding
    X = [[
        time_map[time_context],
        location_map[location],
        activity_map[activity],
        env_map[environment]
    ]]

    # Predict emotion
    emotion = model.predict(X)[0]

    
    probs = model.predict_proba(X)[0]
    confidence = float(np.max(probs) * 100)

    print("Predicted Emotion:", emotion)
    print("Confidence:", confidence)

    # Write output in fusion-compatible format
    with open(emotion_file, "w") as f:
        json.dump({
            "emotion": emotion,
            "confidence": confidence
        }, f, indent=4)

    print("Saved to context_emotion_output.json")

    time.sleep(10)