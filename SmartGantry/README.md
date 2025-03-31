# Smart Gantry (Edge Device)

This project powers the **Smart Gantry edge device**, designed for secure and automated attendance logging at access points. The system combines facial recognition, speech verification, and object detection to provide seamless entry and exit experiences for employees. It communicates with a centralised server via MQTT and is designed to run reliably using systemd services.

---

## System Services

### ✅ `smartgantry.service`
This service runs the **core application** that manages the edge device’s real-time interactions with users. Its responsibilities include:

- Detecting approaching objects using an ultrasonic sensor
- Running facial recognition to identify employees
- Performing speech recognition for voice password confirmation
- Sending `clock_in` or `clock_out` messages to the central server via MQTT

This service ensures that access attempts are processed efficiently and accurately.

### ✅ `app_handler.service`
This service handles **supplementary commands** received from the central server. These include:

- Scanning for connected devices and reporting device information (e.g., hostname, IP address, mode)
- Updating the device mode between `entry` and `exit`
- Registering new employees by receiving and storing face data

Running this as a separate service keeps administrative tasks isolated from the real-time core application, enhancing reliability and maintainability.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/itsalys/INF2009_GP25_EC.git
cd smartgantry
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv smartgantry
```

- **Linux/macOS:**  
  ```bash
  source smartgantry/bin/activate
  ```

- **Windows:**  
  ```cmd
  smartgantry\Scripts\activate
  ```

### 3. Install Dependencies

```bash
sudo apt update
sudo apt install -y portaudio19-dev cmake
pip install -r requirements.txt
```

> Note: `portaudio19-dev` is required for microphone support. `cmake` is needed for some compiled packages like dlib. 

### 4. Start the Main Application

```bash
python3 main.py
python3 app_handler.py
```

These commands will launch both the smart gantry logic and the handler for remote server commands. To run them continuously, it's recommended to set up system services as shown below.
---

## Setting Up System Services

Systemd unit files for both `smartgantry.service` and `app_handler.service` are available in the `services/` directory. To enable them:

```bash
sudo cp services/smartgantry.service /etc/systemd/system/
sudo cp services/app_handler.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable smartgantry.service
sudo systemctl enable app_handler.service
sudo systemctl start smartgantry.service
sudo systemctl start app_handler.service
```

---

## Configuration

All MQTT and device-specific settings are stored in `config.json`. Ensure this file is present and correctly configured before running the application or enabling services.
