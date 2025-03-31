import json
import time
import random
import statistics
import threading
import paho.mqtt.client as mqtt
from datetime import datetime

# === Configuration ===
BROKER = "192.168.88.9"
PORT = 1883
KEEPALIVE = 60
SIMULATED_DEVICES = 100
TOTAL_MESSAGES = 10  # 10 clock-ins and 10 clock-outs
DEVICE_PREFIX = "ed"
EMPLOYEE_IDS = [str(1040 + i) for i in range(SIMULATED_DEVICES)]
RESPONSE_TIMEOUT = 5  # seconds
response_times = []
lock = threading.Lock()

def simulate_device(device_num):
    employee_id = EMPLOYEE_IDS[device_num]
    device_id = f"{DEVICE_PREFIX}{device_num:03d}"
    topic_in = f"smartgantry/{device_id}/clock_in_response"
    topic_out = f"smartgantry/{device_id}/clock_out_response"
    request_in = f"smartgantry/{device_id}/clock_in_request"
    request_out = f"smartgantry/{device_id}/clock_out_request"
    responses = {}

    def on_message(client, userdata, msg):
        now = time.time()
        with lock:
            if msg.topic in responses:
                responses[msg.topic]["received"] = now

    client = mqtt.Client(client_id=f"sim_{device_id}")
    client.on_message = on_message
    client.connect(BROKER, PORT, KEEPALIVE)
    client.subscribe(topic_in)
    client.subscribe(topic_out)
    client.loop_start()

    for _ in range(TOTAL_MESSAGES):
        # Clock In
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        payload_in = {"employee_id": employee_id, "action": "clock_in", "timestamp": timestamp}
        responses[topic_in] = {"sent": time.time(), "received": None}
        client.publish(request_in, json.dumps(payload_in))

        timeout = time.time() + RESPONSE_TIMEOUT
        while time.time() < timeout:
            if responses[topic_in]["received"]:
                break
            time.sleep(0.05)

        with lock:
            if responses[topic_in]["received"]:
                diff = responses[topic_in]["received"] - responses[topic_in]["sent"]
                response_times.append(diff)

        time.sleep(0.1)

        # Clock Out
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        payload_out = {"employee_id": employee_id, "action": "clock_out", "timestamp": timestamp}
        responses[topic_out] = {"sent": time.time(), "received": None}
        client.publish(request_out, json.dumps(payload_out))

        timeout = time.time() + RESPONSE_TIMEOUT
        while time.time() < timeout:
            if responses[topic_out]["received"]:
                break
            time.sleep(0.05)

        with lock:
            if responses[topic_out]["received"]:
                diff = responses[topic_out]["received"] - responses[topic_out]["sent"]
                response_times.append(diff)

        time.sleep(0.2)

    client.loop_stop()
    client.disconnect()

# === Run Devices in Parallel ===
threads = []
start = time.time()

for i in range(SIMULATED_DEVICES):
    t = threading.Thread(target=simulate_device, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()

# === Report ===
if response_times:
    print(f"✅ Total Responses: {len(response_times)}")
    print(f"📊 Average Response Time: {sum(response_times) / len(response_times):.4f} sec")
    print(f"📊 Median Response Time: {statistics.median(response_times):.4f} sec")
else:
    print("⚠️ No responses received.")

print(f"🕒 Total Test Duration: {end - start:.2f} sec")
