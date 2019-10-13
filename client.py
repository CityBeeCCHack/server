import time
import requests
import subprocess

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

serverIP = "192.168.88.161"
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

flag = 0
while True:

    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure() * 100
    humidity = bme280.get_humidity()
    sensorPayload =  {"Time": int(time.time()),
                "Temperature": int(temperature),
                "Pressure": int(pressure),
                "Humidity": int(humidity)}
    while True:
        try:
            response = requests.post(f'http://{serverIP}:1337/pi/sensors', json=sensorPayload)
            print(f"Successfully sent sensor data: {str(sensorPayload)}")
            break
        except:
            print("Could not connect to server")
            time.sleep(30)
    

    if flag == 0:
        subprocess.call(["raspistill", "-n", "-t", "1", "-q", "50", "-o", r"/home/pi/CityBee/image1.jpg"])
        time.sleep(0.5)
        with open(r"/home/pi/CityBee/image1.jpg", "rb") as imageFile:
            response = requests.post(f'http://{serverIP}:1337/pi/image', data=imageFile)
            if response.ok:
                print("Successfully sent image")
            else:
                print(f"Image failed to send: {response.reason}")
        flag += 0

    time.sleep(60)


