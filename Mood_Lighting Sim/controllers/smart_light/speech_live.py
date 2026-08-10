import sounddevice as sd
import numpy as np
import librosa
import joblib
import json
import time
import warnings
import speech_recognition as sr

warnings.filterwarnings("ignore")

# Load trained model and scaler


# Load trained model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

print("Model expects", model.n_features_in_, "features")

emotion_file = "audio_emotion_output.json"

SAMPLE_RATE = 22050
RECORD_TIME = 5

LIGHT_UPDATE_INTERVAL = 5  # 1 minutes
last_light_update = time.time()

recognizer = sr.Recognizer()


def extract_features(audio):
    mfcc = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)

    chroma = librosa.feature.chroma_stft(y=audio, sr=SAMPLE_RATE)
    chroma = np.mean(chroma.T, axis=0)

    mel = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE)
    mel = np.mean(mel.T, axis=0)

    contrast = librosa.feature.spectral_contrast(y=audio, sr=SAMPLE_RATE)
    contrast = np.mean(contrast.T, axis=0)

    tonnetz = librosa.feature.tonnetz(
        y=librosa.effects.harmonic(audio), sr=SAMPLE_RATE
    )
    tonnetz = np.mean(tonnetz.T, axis=0)

    features = np.hstack([mfcc, chroma, mel, contrast, tonnetz])

    return features


while True:
    print("\n Speak now...")

    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_text = recognizer.listen(source, phrase_time_limit=RECORD_TIME)

    

    # Record audio for emotion model
    audio = sd.rec(
        int(RECORD_TIME * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )

    sd.wait()
    audio = audio.flatten()

    # Feature calculations
    energy = np.mean(np.abs(audio))

    pitches, magnitudes = librosa.piptrack(y=audio, sr=SAMPLE_RATE)
    pitch = np.mean(pitches[pitches > 0])

    print("Voice Energy:", round(energy, 5))
    print("Pitch Estimate:", round(pitch, 2), "Hz")

    # Ignore weak audio
    if energy < 0.002:
        print("No strong voice detected")
        continue

    # Extract features
    features = extract_features(audio)

    # Match model feature size
    features = features[:model.n_features_in_]
    features = np.expand_dims(features, axis=0)

    # Scale features
    features = scaler.transform(features)

    # Predict emotion
    emotion = model.predict(features)[0]

    # Confidence score
    probabilities = model.predict_proba(features)
    confidence = np.max(probabilities) * 100

    print("Detected Emotion:", emotion)
    print("Confidence Score:", round(confidence, 2), "%")

    # Update Webots light every 2 minutes
    if time.time() - last_light_update >= LIGHT_UPDATE_INTERVAL:

        with open(emotion_file, "w") as f:
            json.dump({
                "emotion": emotion,
                "confidence": float(confidence)
            }, f)

        print("Emotion sent to Webots (light updated)")
        last_light_update = time.time()

    else:
        print("Emotion detected but waiting to update light...")