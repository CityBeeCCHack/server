from flask import Flask, request, jsonify

app = Flask(__name__)
localIP = "192.168.137.1"

@app.route('/pi', methods=['POST'])
def pi():
    sensorData = request.json
    print(f'Value on server {sensorData}')  # --> Value on server {'temp': 100, 'temp_1': 150}
    with open("output.jpg", "wb") as outputFile:
        outputFile.write(request.data)
    return jsonify(sensorData)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True, port = 1337)