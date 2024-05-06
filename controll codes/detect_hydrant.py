import airsim
import cv2
import numpy as np 
import pprint

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# set camera name and image type to request images and detections
camera_name = "0"
image_type = airsim.ImageType.Scene


# set detection radius in [cm]
client.simSetDetectionFilterRadius(camera_name, image_type, 50 * 50) 
# add desired object name to detect in wild card/regex format
client.simAddDetectionFilterMeshName(camera_name, image_type, "Hydrant*") 

client.takeoffAsync().join()

while True:
    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        continue
    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
    hydrants = client.simGetDetections(camera_name, image_type)
    if hydrants:
        for hydrant in hydrants:
            # s = pprint.pformat(hydrant)
            # print("hydrant: %s" % s)

            cv2.rectangle(png,(int(hydrant.box2D.min.x_val),int(hydrant.box2D.min.y_val)),(int(hydrant.box2D.max.x_val),int(hydrant.box2D.max.y_val)),(255,0,0),2)
            cv2.putText(png, hydrant.name, (int(hydrant.box2D.min.x_val),int(hydrant.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))

    
    cv2.imshow("AirSim", png)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        client.simClearDetectionMeshNames(camera_name, image_type)
    elif cv2.waitKey(1) & 0xFF == ord('a'):
        client.simAddDetectionFilterMeshName(camera_name, image_type, "Hydrant*")

    client.moveToPositionAsync(0, 30, -1.5, 3).join()

cv2.destroyAllWindows() 
client.armDisarm(False)
client.enableApiControl(False)