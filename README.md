# INF2009: Automated Clock-In and Attendance System

This repository contains the complete implementation of the **Automated Clock-In and Attendance System**, a decentralised IoT solution for employee access tracking. The system is composed of two major components:

- **Centralised Server** (`Webserver/`): Hosts the Flask-based web dashboard, handles MQTT communication, and logs attendance in a database.
- **Smart Gantry Device** (`SmartGantry/`): Operates at entry/exit points to detect personnel, authenticate them using face and speech recognition, and communicate attendance actions to the central server.

---

## 🔧 System Overview

| Component         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| Webserver         | Flask app + MQTT listener for centralised control, monitoring, and logging |
| SmartGantry       | Edge device with sensors and authentication modules                         |
| MariaDB           | Main relational database for employee and attendance data                  |
| Mosquitto         | MQTT broker for message exchange between devices and server                |

---

## 📂 Repository Structure

```bash
INF2009_GP25_EC/
├── SmartGantry/           # Code for the smart gantry edge devices
├── Webserver/             # Flask app, MQTT logic, and attendance handler
├── .gitignore
└── README.md              # This file
```

---

## 🚀 Set Up

See detailed READMEs in the respective folders:

- [`Webserver/README.md`](./Webserver/README.md)
- [`SmartGantry/README.md`](./SmartGantry/README.md)

---

## 🖥️ Centralised Server (Webserver/)

- Hosts the main web dashboard
- Runs two core services:
  - `webserver.service`: Flask app for real-time attendance and admin dashboard
  - `attendance_handler.service`: Background MQTT listener to process clock-in/out messages

Refer to the [Webserver README](./Webserver/README.md) for full installation steps.

---

## 📡 Smart Gantry Device (SmartGantry/)

- Installed at physical gantries
- Detects personnel using sensors and authenticates them
- Sends attendance data to the server over MQTT
- Runs two core services:
  - `smartgantry.service`: Real-time facial and speech authentication
  - `app_handler.service`: Handles admin commands from server (e.g., mode update, device scan)

Refer to the [SmartGantry README](./SmartGantry/README.md) for setup and configuration instructions.

---

## 🧩 Configuration Files

- `.env`: Stored in `Webserver/`, contains environment variables like DB credentials
- `config.json`: Stored in `SmartGantry/`, defines MQTT broker and device mode settings

---
