from controller import Robot

robot = Robot()

TIME_STEP = 64
MAX_SPEED = 3.0


leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

ps = []

psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    sensor = robot.getDevice(psNames[i])
    sensor.enable(TIME_STEP)
    ps.append(sensor)


camera = robot.getDevice('camera')
camera.enable(TIME_STEP)

width = camera.getWidth()
height = camera.getHeight()

print("Camera Enabled")


FRONT_THRESHOLD = 90
SIDE_THRESHOLD = 70
COLOR_THRESHOLD = 100


def move(left_speed, right_speed):
    leftMotor.setVelocity(left_speed)
    rightMotor.setVelocity(right_speed)


while robot.step(TIME_STEP) != -1:

    sensor_values = [sensor.getValue() for sensor in ps]

    front_right = sensor_values[0]
    front_right_center = sensor_values[1]

    front_left_center = sensor_values[6]
    front_left = sensor_values[7]

    left_side = sensor_values[5]
    right_side = sensor_values[2]

    front = max(
        front_right,
        front_right_center,
        front_left_center,
        front_left
    )

   
    image = camera.getImage()

    total_red = 0
    total_green = 0
    total_blue = 0

    count = 0

   
    for x in range(width // 3, 2 * width // 3):
        for y in range(height // 3, 2 * height // 3):

            r = camera.imageGetRed(image, width, x, y)
            g = camera.imageGetGreen(image, width, x, y)
            b = camera.imageGetBlue(image, width, x, y)

            total_red += r
            total_green += g
            total_blue += b

            count += 1

    avg_red = total_red / count
    avg_green = total_green / count
    avg_blue = total_blue / count

    detected_color = None

    
    if avg_red > COLOR_THRESHOLD and avg_red > avg_green + 30 and avg_red > avg_blue + 30:
        detected_color = "RED"

    elif avg_green > COLOR_THRESHOLD and avg_green > avg_red + 30 and avg_green > avg_blue + 30:
        detected_color = "GREEN"

    elif avg_blue > COLOR_THRESHOLD and avg_blue > avg_red + 30 and avg_blue > avg_green + 30:
        detected_color = "BLUE"

   
    if detected_color is not None:

        print("OBJECT FOUND")
        print("COLOR:", detected_color)

       
        if left_side < right_side:

            print("MOVE LEFT")
            move(-1.0, 2.5)

        else:

            print("MOVE RIGHT")
            move(2.5, -1.0)

  
    elif front > FRONT_THRESHOLD:

        print("TURNING")

        if left_side < right_side:
            move(-1.0, 2.5)
        else:
            move(2.5, -1.0)

   
    elif left_side > SIDE_THRESHOLD:

        move(2.0, 3.0)

    elif left_side < 50:

        move(3.0, 2.0)

   
    else:

        print("FORWARD")
        move(MAX_SPEED, MAX_SPEED)