from controller import Supervisor
import json

# 1. Initialize the Supervisor (The Brain)
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# 2. Find your bulb in the world using the DEF name you gave it
bulb = robot.getFromDef("Bulb")


# 3. Get access to the 'color' field of the bulb
color_field = bulb.getField("color")
intensity_field = bulb.getField("intensity")

visual = robot.getFromDef("BulbVisual")

appearance = visual.getField("appearance").getSFNode()
color_visual = appearance.getField("baseColor")   # correct for PBRAppearance
emissive_field = appearance.getField("emissiveColor")

# 4. The Main Loop (Runs forever)
"""
while robot.step(timestep) != -1:
    # Set color to RED [R, G, B] where 1.0 is max and 0.0 is off
    color_field.setSFColor([1.0, 1.0, 0.0])
    
    # 1. Get the intensity field (put this at the top with your other setups)
    intensity_field = bulb.getField("intensity")
    
    # 2. Inside your loop, change it dynamically
    # Example: Set brightness to 8.0 (Very Bright)
    intensity_field.setSFFloat(8.0) 
    
    # Example: Dim it to 2.0
    intensity_field.setSFFloat(2.0)

"""
while robot.step(timestep) != -1:
    try:
        with open("audio_emotion_output.json", "r") as f:
            data = json.load(f)
            mood = data["emotion"]
    except:
        mood = "neutral"

    if mood == "happy":
        color = [1.0, 1.0, 0.0]  # Yellow
        intensity = 8.0

    elif mood == "sad":
        color = [0.0, 0.0, 1.0]  # Blue
        intensity = 3.0
    
    elif mood == "angry":
        color = [0.0, 1.0, 0.0]  # Red
        intensity = 6.0
    
    else:
        color = [1.0, 1.0, 1.0]
        intensity = 4.0

# APPLY
    color_field.setSFColor(color)        # Light
    color_visual.setSFColor(color)       # Base color
    emissive_field.setSFColor(color)     # 🔥 THIS FIXES IT
    intensity_field.setSFFloat(intensity)