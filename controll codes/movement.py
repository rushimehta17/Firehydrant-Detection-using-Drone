import airsim
import time
import cv2

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

positions = [[0,0], [-1.5,32.0], [-1.5, 40.0], [7, 40.0], [0, 62.0], [0, 90.0]]

# set camera name and image type to request images and detections
camera_name = "0"
image_type = airsim.ImageType.Scene
# set detection radius in [cm]
client.simSetDetectionFilterRadius(camera_name, image_type, 40 * 40) 
# add desired object name to detect in wild card/regex format
client.simAddDetectionFilterMeshName(camera_name, image_type, "Hydrant*") 

def detect_hydrant(pos1, y):
    
    while y < pos1 :
        rawImage = client.simGetImage(camera_name, image_type)
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        hydrants = client.simGetDetections(camera_name, image_type)
        if hydrants:
            for hydrant in hydrants:
                cv2.rectangle(png,(int(hydrant.box2D.min.x_val),int(hydrant.box2D.min.y_val)),(int(hydrant.box2D.max.x_val),int(hydrant.box2D.max.y_val)),(255,0,0),2)
                cv2.putText(png, hydrant.name, (int(hydrant.box2D.min.x_val),int(hydrant.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))
                
        cv2.imshow("AirSim", png)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("q")
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            client.simClearDetectionMeshNames(camera_name, image_type)
        elif cv2.waitKey(1) & 0xFF == ord('a'):
            client.simAddDetectionFilterMeshName(camera_name, image_type, "Hydrant*")

        drone_state = client.getMultirotorState()
        # Get current position
        position = drone_state.kinematics_estimated.position
        y = position.y_val



# Get drone state
drone_state = client.getMultirotorState()
# Get current position
position = drone_state.kinematics_estimated.position
x, y, z = position.x_val, position.y_val, position.z_val
# Print current position
print(f"Starting Position of the Drone: x: {x}, y: {y}, z: {z}")

client.takeoffAsync().join()

for pos in positions:
    client.moveToPositionAsync(pos[0], pos[1], -1.4, 3)
    
    detect_hydrant(pos[1], y)
    time.sleep(3.0)
    # Get drone state
    drone_state = client.getMultirotorState()
    # Get current position
    position = drone_state.kinematics_estimated.position
    x, y, z = position.x_val, position.y_val, position.z_val
    # Print current position
    print(f"Current Position of the Drone: x: {x}, y: {y}, z: {z}")
    

cv2.destroyAllWindows() 
client.reset()
client.armDisarm(False)
client.enableApiControl(False)