try:
    import Adafruit_DHT
    RASPBERRY_PI = True
except ImportError:
    print("⚠️ Warning: Adafruit_DHT not found! Using simulated sensor data.")
    RASPBERRY_PI = False

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Serial module not found! Using simulated CO₂ data.")
    SERIAL_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: OpenCV (cv2) not found! Using simulated occupancy detection.")
    OPENCV_AVAILABLE = False

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Ultralytics YOLO not found! Using simulated detection.")
    YOLO_AVAILABLE = False


# TEMPERATURE & HUMIDITY SENSOR (DHT22)

if RASPBERRY_PI:
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4  # GPIO pin where the sensor is connected
else:
    DHT_SENSOR = None
    DHT_PIN = None


def get_dht22_data():
    """ Reads Temperature & Humidity from DHT22 Sensor (or simulates if running in Codespace) """
    if not RASPBERRY_PI:
        return 24.5, 55.0  # Simulated temperature & humidity

    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    if humidity is not None and temperature is not None:
        return round(temperature, 2), round(humidity, 2)
    else:
        print("⚠️ Failed to retrieve data from DHT22 sensor")
        return None, None


# CO₂ SENSOR (MH-Z19)

SERIAL_PORT = "/dev/ttyAMA0"  # Change this if using a different port

def get_co2_level():
    """ Reads CO₂ Level from MH-Z19 Sensor (or simulates in Codespace) """
    if not SERIAL_AVAILABLE:
        return 400  # Simulated CO₂ level

    try:
        ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
        ser.write(b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79')
        response = ser.read(9)
        if response and response[0] == 0xFF and response[1] == 0x86:
            co2 = response[2] * 256 + response[3]
            return co2
        return None
    except serial.SerialException as e:
        print(f"⚠️ Serial Error: {e}")
        return None



# OCCUPANCY DETECTION (AI CAMERA - YOLO)

if YOLO_AVAILABLE:
    model = YOLO("yolov8n.pt")  # Pretrained YOLOv8 model
else:
    model = None

def detect_people(frame):
    """ Detects people in the given video frame using YOLO (or simulates in Codespace) """
    if not YOLO_AVAILABLE:
        return True  # Simulate a person being detected

    model = YOLO("yolov8n.pt")  # Pretrained YOLOv8 model
    results = model(frame)

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])  # Class ID
            if cls_id == 0:  # Class 0 is 'Person' in COCO dataset
                return True  # At least one person detected
    return False


def check_occupancy_camera():
    """ Uses AI-powered camera to detect room occupancy (or simulates in Codespace) """
    if not OPENCV_AVAILABLE:
        return 1  # Simulate an occupied room

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        return 0  # Assume room is empty

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Error: Could not read frame!")
        return 0  # Assume room is empty

    occupied = detect_people(frame)
    return 1 if occupied else 0



# FETCH ALL SENSOR DATA

def get_real_sensor_data():
    """ Retrieves real-time data from all sensors """
    temperature, humidity = get_dht22_data()
    co2_level = get_co2_level()
    occupancy = check_occupancy_camera()
    
    sensor_data = {
        "temperature": temperature if temperature is not None else 22,
        "humidity": humidity if humidity is not None else 50,
        "co2_level": co2_level if co2_level is not None else 400,
        "occupancy": occupancy
    }
    
    return sensor_data
