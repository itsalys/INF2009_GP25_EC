# Centralised Server

This guide outlines how to set up the centralised server for the Smart Gantry system. It includes the web interface, MQTT communication layer, and attendance data handling.

---

## System Services

### `webserver.service`
This service runs the **Flask-based web application** that serves as the dashboard for both employees and administrators.

- Displays real-time attendance data  
- Provides tools for managing employee records  
- Monitors overall system status  

This service ensures the web interface is always available and responsive.

### `attendance_handler.service`
This service handles **incoming attendance data** from edge devices over MQTT. It verifies and records attendance actions into the MariaDB database.

- Listens for `clock_in` and `clock_out` messages  
- Processes employee attendance logic  
- Updates the database in real time  

By running separately from the webserver, this service offloads backend processing and maintains smooth performance of the dashboard.

---

## Installation and Set up

### 1. Clone the Repository

```bash
git clone https://github.com/itsalys/INF2009_GP25_EC.git
cd smartgantry
```

---

### 2. Python Environment Setup

Ensure Python is installed:

```bash
python --version
```

Navigate to the webserver folder:

```bash
cd Webserver
```

Create a virtual environment and activate it (recommended):

```bash
python -m venv venv
venv\Scripts\activate       # On Windows
source venv/bin/activate    # On Linux/macOS
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `Webserver/` folder and add your credentials (e.g., DB username, password).  
**Note:** This file is ignored by Git—ensure it's not staged before committing.

---

### 3. Database Setup (MariaDB)

Install MariaDB:

- Windows: Use [XAMPP](https://www.apachefriends.org/)
- Linux: `sudo apt install mariadb-server`

Edit the configuration to allow larger packets (to prevent truncation):

```ini
# Go to: C:\xampp\mysql\bin\my.ini (Windows) or /etc/mysql/my.cnf (Linux)
[mysqld]
max_allowed_packet=16M
```

Start MariaDB:

- Windows (via XAMPP Control Panel): Start **MySQL**
- Linux:

```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

---

### 4. MQTT Broker Setup

Install Mosquitto MQTT Broker:

```bash
sudo apt install mosquitto
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

This broker facilitates real-time message exchange (e.g., `clock_in`, `clock_out`) between the central server and edge devices.

---

### 5. Run the Centralised Server

From the `Webserver/` folder, run both the web application and the attendance handler:

```bash
python app.py
python attendance_handler.py
```

These commands will launch both the centralised web dashboard and the background logic that processes clock-in/clock-out messages from edge devices. On first run, the web application should initialise the database schema automatically. To ensure continuous operation without manual supervision, we recommend setting up system services as described below.


---

### 6. System Services Setup

Two services are provided to run continuously in the background and restart on boot:

- **webserver.service**: Launches the Flask application.
- **attendance_handler.service**: Listens for MQTT messages and updates the MariaDB database.

To install and enable these:

```bash
# Copy service files to systemd directory (Linux example)
sudo cp services/webserver.service /etc/systemd/system/
sudo cp services/attendance_handler.service /etc/systemd/system/

# Reload systemd, enable, and start services
sudo systemctl daemon-reexec
sudo systemctl enable webserver.service
sudo systemctl enable attendance_handler.service
sudo systemctl start webserver.service
sudo systemctl start attendance_handler.service
```

These services ensure the system is resilient and runs without manual intervention after boot.

---


