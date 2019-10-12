import time
import requests
import subprocess

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

localIP = "192.168.137.1"
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

while True:

    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure() * 100
    humidity = bme280.get_humidity()
    sensorPayload =  {"Time": str(int(time.time())),
                "Temperature": f"{temperature:.1f}",
                "Pressure": f"{pressure:.1f}",
                "Humidity": f"{humidity:.1f}"}

    response = requests.post(f'http://{localIP}:1337/pi', json=sensorPayload)
    if response.ok:
        print(f"Successfully sent sensor data: {str(sensorPayload)}")
    else:
        print(f"Sensor data failed to send: {response.reason}")

    subprocess.call(["raspistill", "-n", "-t 1", "-q 50", "-o ~/PlanBee/image.jpg"])
    with open("\CityBee\image.jpg", "rb") as imageFile:
        response = requests.post(f'http://{localIP}:1337/pi/image', data=imageFile)
        if response.ok:
            print("Successfully sent image")
        else:
            print(f"Image failed to send: {response.reason}")

        time.sleep(10)


