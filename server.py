from flask import Flask, request, jsonify, send_from_directory
from PIL import Image

app = Flask(__name__)
port = 1337

@app.route('/pi/sensors', methods=['POST'])
def saveSensorData():
    sensorData = request.json
    print(f"Sensor data received: {str(sensorData)}")
    with open("Sensor Logs.csv", "a") as csvFile:
        values = ",".join(str(value) for value in sensorData.values())
        csvFile.write(values + "\n")
    return jsonify(sensorData)

@app.route('/pi/image', methods=['POST'])
def image():
    with open("feed.jpg", "wb") as outputFile:
        outputFile.write(request.data)
        return("Image received")

@app.route('/disconnect')
def disconnect():
    return {"Name": "John Doe", "Description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."}

@app.route('/disconnect/sensors', methods=["GET"])
def sendSensorData():
    with open("Sensor Logs.csv", "r") as csvFile:
        # content = csvFile.read()
        parameters = dict(request.args)
        if "quantity" in parameters:
            quantity = int(request.args.get("quantity"))
            content = csvFile.read().split("\n")
            desiredData = content[-(quantity+1):]
            return "\n".join(desiredData)
        else:
            return csvFile.read()
        return content

@app.route('/disconnect/feed')
def feed():
    return send_from_directory("", "feed.jpg")

@app.route('/disconnect/sucrose')
def sucrose():
    img = Image.open('feed.jpg')
    # img.show()
    pix = img.load()
    print(img.size)
    counter = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if all(i>150 for i in pix[x,y]):
                counter += 1
    ratio = counter/(img.size[1] * img.size[0]) * 100
    return f"{ratio:.1f}"

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = port)