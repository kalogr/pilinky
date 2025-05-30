import serial
import time
import logging
from collections import deque
from utils import is_valid_numeric_value, is_monotonic_increase, is_outlier
from mqtt_client import MQTTClient

class TeleinfoReader:
    """
    Reader for the uTeleinfo V2 USB module connected to /dev/ttyUSB0.
    Communicates with the serial port at 9600 baud.
    Publishes cleaned and validated teleinfo data to an MQTT broker running on localhost.
    """

    def __init__(self, port='/dev/ttyUSB0'):
        self.port = port
        self.last_display_times = {}
        self.energy_history = deque(maxlen=10)
        self.power_history = deque(maxlen=10)

        self.mqtt = MQTTClient(broker="localhost")
        self.mqtt.connect()

    def publish_measurement(self, label, value, publish_id,  interval):
        ''' Publish the measurement if the interval has passed since the last publish.'''

        now = time.time()
        if now - self.last_display_times.get(label, 0) >= interval:
            logging.info(f"{label}: {int(value)}")
            self.mqtt.publish(publish_id, int(value))
            self.last_display_times[label] = now

    def run(self):
        ''' Main loop to read teleinfo frames from the serial port.'''

        logging.info("Connecting to serial port...")
        with serial.Serial(self.port, 9600, bytesize=7, parity='E', stopbits=1, timeout=1) as ser:
            logging.info("Reading teleinfo frames...")

            while True:
                line = ser.readline().decode('ascii', errors='ignore').strip()
                parts = line.split()
                if len(parts) < 2:
                    continue

                label = parts[0]
                value = parts[1].lstrip('0') or '0'

                if label == 'SINSTS': # Instantaneous power in VA
                    if not is_valid_numeric_value(value):
                        continue
                    if not is_outlier(value, self.power_history):
                        self.power_history.append(int(value))
                        self.publish_measurement("Instantaneous power (VA)", value, "power", 10)

                elif label == 'EAST': # Active power in Wh
                    if not is_monotonic_increase(value, self.energy_history):
                        continue
                    if not is_outlier(value, self.energy_history):
                        self.energy_history.append(int(value))
                        self.publish_measurement("Total active energy (Wh)", value, "totalenergy", 10)

                elif label == 'EASF02': # Total injection in Wh
                    if not is_monotonic_increase(value, self.energy_history):
                        continue
                    if not is_outlier(value, self.energy_history):
                        self.energy_history.append(int(value))
                        self.publish_measurement("Total injection (Wh)", value, "injection", 10)
