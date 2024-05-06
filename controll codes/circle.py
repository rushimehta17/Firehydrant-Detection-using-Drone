import airsim
import math

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Set the radius of the circle
radius = 6

# Set the altitude at which you want to fly
altitude = 1  # Adjust this as needed

# Calculate the center of the circle
center_x = 0
center_y = 0

# Set the drone's initial position to the starting point of the circle
initial_x = center_x + radius
initial_y = center_y

# Set the initial position and take off
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(initial_x, initial_y, -altitude), airsim.to_quaternion(0, 0, 0)), True)

# Fly the drone in a circle
num_points = 36  # You can adjust this to control the smoothness of the circle
for i in range(num_points):
    angle = i * (2 * math.pi / num_points)
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    client.moveToPositionAsync(x, y, -altitude, 2).join()  # Adjust the speed (last argument) as needed

# Land the drone
client.landAsync().join()

# Disconnect from the simulator
client.reset()
client.armDisarm(False)
client.enableApiControl(False)