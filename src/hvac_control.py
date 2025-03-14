try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True  # Running on a Raspberry Pi
except ImportError:
    print("⚠️ Warning: RPi.GPIO not found! Running in simulation mode.")
    RASPBERRY_PI = False  # Running in Codespace or another environment
import time
import paho.mqtt.client as mqtt
from src.ai_model import predict_temperature
from src.sensors import get_real_sensor_data


# GPIO CONFIGURATION (For Raspberry Pi)

FAN_PIN = 17      # Fan Relay
HEATER_PIN = 27   # Heater Relay
AC_PIN = 22       # AC Relay

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.setup(AC_PIN, GPIO.OUT)

# Turn OFF all components initially
GPIO.output(FAN_PIN, GPIO.LOW)
GPIO.output(HEATER_PIN, GPIO.LOW)
GPIO.output(AC_PIN, GPIO.LOW)


# MQTT CONFIGURATION (For IoT Smart Devices)

BROKER_ADDRESS = "mqtt.example.com"  # Change this to your MQTT broker address
TOPIC_FAN = "home/hvac/fan"
TOPIC_HEATER = "home/hvac/heater"
TOPIC_AC = "home/hvac/ac"

client = mqtt.Client()
client.connect(BROKER_ADDRESS, 1883, 60)


# CONTROL HVAC SYSTEM (Raspberry Pi GPIO)

def control_hvac_gpio(desired_temperature):
    """ Controls HVAC system using Raspberry Pi GPIO based on AI predictions. """
    current_data = get_real_sensor_data()
    predicted_temp = predict_temperature(current_data)

    print("\n[Real-Time HVAC Sensor Data]")
    for key, value in current_data.items():
        unit = "°C" if key == "temperature" else "%" if key == "humidity" else "ppm" if key == "co2_level" else ""
        print(f"{key.replace('_', ' ').capitalize()}: {value} {unit}")

    print("\n[Adjusting HVAC System...]")
    if predicted_temp > desired_temperature:
        print(f"Cooling down to {desired_temperature}°C... ❄️")
        GPIO.output(FAN_PIN, GPIO.HIGH)
        GPIO.output(AC_PIN, GPIO.HIGH)
        GPIO.output(HEATER_PIN, GPIO.LOW)
    elif predicted_temp < desired_temperature:
        print(f"Heating up to {desired_temperature}°C... 🔥")
        GPIO.output(FAN_PIN, GPIO.LOW)
        GPIO.output(AC_PIN, GPIO.LOW)
        GPIO.output(HEATER_PIN, GPIO.HIGH)
    else:
        print("Temperature is optimal. No adjustment needed. ✅")
        GPIO.output(FAN_PIN, GPIO.LOW)
        GPIO.output(AC_PIN, GPIO.LOW)
        GPIO.output(HEATER_PIN, GPIO.LOW)

    print("\n[HVAC Adjustment Complete]\n")


# CONTROL HVAC SYSTEM (MQTT Smart Devices)

def control_hvac_mqtt(desired_temperature):
    """ Controls HVAC system using IoT-based MQTT smart devices. """
    current_data = get_real_sensor_data()
    predicted_temp = predict_temperature(current_data)

    print("\n[Real-Time HVAC Sensor Data]")
    for key, value in current_data.items():
        unit = "°C" if key == "temperature" else "%" if key == "humidity" else "ppm" if key == "co2_level" else ""
        print(f"{key.replace('_', ' ').capitalize()}: {value} {unit}")

    print("\n[Adjusting HVAC System...]")
    if predicted_temp > desired_temperature:
        print(f"Cooling down to {desired_temperature}°C... ❄️")
        client.publish(TOPIC_FAN, "ON")
        client.publish(TOPIC_AC, "ON")
        client.publish(TOPIC_HEATER, "OFF")
    elif predicted_temp < desired_temperature:
        print(f"Heating up to {desired_temperature}°C... 🔥")
        client.publish(TOPIC_FAN, "OFF")
        client.publish(TOPIC_AC, "OFF")
        client.publish(TOPIC_HEATER, "ON")
    else:
        print("Temperature is optimal. No adjustment needed. ✅")
        client.publish(TOPIC_FAN, "OFF")
        client.publish(TOPIC_AC, "OFF")
        client.publish(TOPIC_HEATER, "OFF")

    print("\n[HVAC Adjustment Complete]\n")

