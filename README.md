🏡 HVAC AI System - Smart Climate Control
An AI-powered HVAC system that adapts to occupancy, temperature, and air quality.

🚀 Features
📡 Real-Time Sensor Data: Reads temperature, humidity, CO₂ levels, and occupancy.
🤖 AI-Based Climate Control: Predicts and adjusts the temperature using machine learning.
📷 Smart Occupancy Detection: Uses YOLOv8 AI to detect people in the room.
🌍 IoT & Raspberry Pi Integration: Works with GPIO-based relays and MQTT smart plugs.
📊 Live Dashboard: Displays real-time data via a Flask web app.

🛠 Technologies Used
Python, Flask, Pandas, Scikit-Learn
YOLOv8 (Ultralytics) for AI-based occupancy detection
Adafruit_DHT, pyserial for sensor readings
MQTT for IoT-based HVAC control
Raspberry Pi GPIO (optional for hardware control)

📥 Installation
1️⃣ Clone the Repository
cd HVAC-AI

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the AI Model Training
python -m src.ai_model

4️⃣ Start the Web App
python -m src.web_app
Then open http://localhost:5000/ in your browser.

🖥️ How It Works
1️⃣ Reads sensor data (temperature, humidity, CO₂, occupancy)
2️⃣ AI predicts the best temperature based on past patterns
3️⃣ Controls HVAC devices (fan, AC, heater)
4️⃣ Displays live data on the web dashboard

📸 Screenshots
🔹 Live Dashboard

🔹 Sensor Data API
