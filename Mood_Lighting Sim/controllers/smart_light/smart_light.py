from controller import Supervisor
import json

# 1. Initialize the Supervisor
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# 2. Find your bulb in the world
bulb = robot.getFromDef("Bulb")

# 3. Get access to light & visual fields
color_field = bulb.getField("color")
intensity_field = bulb.getField("intensity")

visual = robot.getFromDef("BulbVisual")
appearance = visual.getField("appearance").getSFNode()
color_visual = appearance.getField("baseColor")   # Correct for PBRAppearance
emissive_field = appearance.getField("emissiveColor")

# 4. Emotion Configuration Dictionary (Easy to add/modify emotions here!)
EMOTION_LIGHT_MAP = {
    "happy":     {"color": [1.0, 1.0, 0.0], "intensity": 8.0},  # Yellow
    "sad":       {"color": [0.0, 0.0, 1.0], "intensity": 3.0},  # Blue
    "angry":     {"color": [1.0, 0.0, 0.0], "intensity": 7.0},  # Red
    "disgust":   {"color": [0.0, 1.0, 0.0], "intensity": 4.0},  # Green
    "fearful":   {"color": [0.5, 0.0, 0.8], "intensity": 3.0},  # Purple
    "surprised": {"color": [1.0, 0.4, 0.0], "intensity": 9.0},  # Orange
    "calm":      {"color": [0.0, 0.8, 1.0], "intensity": 5.0},  # Cyan
    "neutral":   {"color": [1.0, 1.0, 1.0], "intensity": 4.0}   # White
}

# 5. The Main Loop
while robot.step(timestep) != -1:
    try:
        with open("physio_emotion_output.json", "r") as f:
            data = json.load(f)
            mood = data.get("emotion", "neutral")
    except:
        mood = "neutral"

    # Safely get the light config for the mood (defaults to neutral if unknown)
    light_config = EMOTION_LIGHT_MAP.get(mood, EMOTION_LIGHT_MAP["neutral"])
    color = light_config["color"]
    intensity = light_config["intensity"]

    # APPLY
    color_field.setSFColor(color)        # Light
    color_visual.setSFColor(color)       # Base color
    emissive_field.setSFColor(color)     # Emissive color
    intensity_field.setSFFloat(intensity)