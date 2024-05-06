import airsim
import numpy as np
import cv2

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()

# Take PNG image from the front camera
response = client.simGetImage("0", airsim.ImageType.Scene)

if response:
    # Convert to numpy array and decode
    img1d = np.frombuffer(response, dtype=np.uint8)  # Using frombuffer to handle bytes object
    img_rgb = cv2.imdecode(img1d, cv2.IMREAD_COLOR)  # Decoding the PNG image

    # Save the image
    filename = "screenshot.png"
    cv2.imwrite(filename, img_rgb)
    print(f"Saved screenshot as {filename}")
else:
    print("Could not capture image.")
