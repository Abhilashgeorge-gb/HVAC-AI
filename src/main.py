import time
import threading
from src.sensors import get_real_sensor_data
from src.ai_model import predict_temperature
from src.hvac_control import control_hvac_gpio, control_hvac_mqtt
from src.web_app import start_web_app

# Set the default desired temperature
DESIRED_TEMPERATURE = 22  # Modify based on user preference

def hvac_control_loop():
    """ Main loop for HVAC AI System. Reads sensors, predicts temperature, and controls HVAC. """
    print("\n🚀 HVAC AI System Starting...\n")
    
    while True:
        # Get real-time sensor data
        sensor_data = get_real_sensor_data()
        
        # Predict the optimal temperature
        predicted_temp = predict_temperature(sensor_data)
        
        # Adjust HVAC system based on AI prediction
        print(f"🔄 Adjusting HVAC to maintain {DESIRED_TEMPERATURE}°C...")
        
        # Use GPIO (Raspberry Pi) or MQTT (Smart Home Devices)
        try:
            control_hvac_gpio(DESIRED_TEMPERATURE)  # Uncomment if using Raspberry Pi relays
            # control_hvac_mqtt(DESIRED_TEMPERATURE)  # Uncomment if using MQTT smart devices
        except Exception as e:
            print(f"⚠️ Error controlling HVAC: {e}")

        # Wait before the next cycle
        time.sleep(10)  # Adjust interval as needed

if __name__ == "__main__":
    # Start web dashboard in a separate thread
    web_thread = threading.Thread(target=start_web_app, daemon=True)
    web_thread.start()

    # Run the main HVAC control loop
    hvac_control_loop()
