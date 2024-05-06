import requests
import json
import airsim
import cv2
import numpy as np

# connect to the AirSim simulator
client = airsim.VehicleClient()
client.confirmConnection()

# set camera name and image type to request images and detections
camera_name = "0"
image_type = airsim.ImageType.Scene

# set detection radius in [cm]
client.simSetDetectionFilterRadius(camera_name, image_type, 200 * 100) 
# add desired object name to detect in wild card/regex format
client.simAddDetectionFilterMeshName(camera_name, image_type, "Hydrant*") 


while True:
    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        continue
    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
    _, encoded_png = cv2.imencode('.png', png)
    image_data = encoded_png.tobytes()

    # Define the URL of your RoboFlow model API
    model_url = "https://detect.roboflow.com/csci513_project/1?api_key=a3nAGFRDhZDc8ASTgG8l"

    # Make a request to the RoboFlow API
    print("making request to roboflow")
    response = requests.post(
        model_url,
        files={"file": image_data},
        headers={"Content-Type": "multipart/form-data"}
    )
    print("response:", response)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print("request was success")

        detection_data = json.loads(response.content)

        # Example: Drawing bounding boxes on the image
        for item in detection_data['predictions']:
            x, y, width, height = item['x'], item['y'], item['width'], item['height']
            cv2.rectangle(png, (x, y), (x + width, y + height), (255, 0, 0), 2)

    # Display the image
    # cv2.imshow("AirSim with RoboFlow", png)

    # cylinders = client.simGetDetections(camera_name, image_type)
    # if cylinders:
    #     for cylinder in cylinders:
    #         s = pprint.pformat(cylinder)
    #         print("Cylinder: %s" % s)

    #         cv2.rectangle(png,(int(cylinder.box2D.min.x_val),int(cylinder.box2D.min.y_val)),(int(cylinder.box2D.max.x_val),int(cylinder.box2D.max.y_val)),(255,0,0),2)
    #         cv2.putText(png, cylinder.name, (int(cylinder.box2D.min.x_val),int(cylinder.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))

    
    cv2.imshow("AirSim", png)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        client.simClearDetectionMeshNames(camera_name, image_type)
    elif cv2.waitKey(1) & 0xFF == ord('a'):
        client.simAddDetectionFilterMeshName(camera_name, image_type, "Cylinder*")
cv2.destroyAllWindows()