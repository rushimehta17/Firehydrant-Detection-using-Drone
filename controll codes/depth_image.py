import airsim
import cv2
import numpy as np 

# connect to the AirSim simulator
client = airsim.VehicleClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

while True:
    # Get depth image from the front-facing camera
    depth_image = client.simGetImage("0", airsim.ImageType.DepthPerspective)
    
    png = cv2.imdecode(airsim.string_to_uint8_array(depth_image), cv2.IMREAD_UNCHANGED)

    cv2.imshow("AirSim", png)

client.armDisarm(False)
client.enableApiControl(False)