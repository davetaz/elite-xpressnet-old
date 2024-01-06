from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
from bson import json_util

import time

app = Flask(__name__)

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['dcc_db']

# Configuration: Set this flag to True to use the mock controller for development.
USE_MOCK_CONTROLLER = True

# Dictionary to store the state of trains
train_state = {}

class RealHornbyController:
    def __init__(self, device_path, baud_rate):
        import hornby  # Import hornby module only when using the real controller
        # Open a serial connection with the Hornby Elite DCC controller
        hornby.connection_open(device_path, baud_rate)

    def throttle(self, train_number, speed, direction):
        import hornby  # Import hornby module only when using the real controller
        # Control the train throttle
        t = hornby.Train(train_number)
        t.throttle(speed, direction)

    def function(self, train_number, function_id, switch):
        import hornby  # Import hornby module only when using the real controller
        # Control the train function
        t = hornby.Train(train_number)
        t.function(function_id, switch)

class MockHornbyController:
    def __init__(self):
        pass

    def throttle(self, train_number, speed, direction):
        # Simulate throttle control (update mock state)
        pass

    def function(self, train_number, function_id, switch):
        # Simulate function control (update mock state)
        pass

# Create the appropriate controller based on configuration
if USE_MOCK_CONTROLLER:
    controller = MockHornbyController()
else:
    controller = RealHornbyController('/dev/ttyACM0', 9600)

# Helper function to wait for a given number of seconds
def wait(secs):
    time.sleep(secs)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# API endpoint to create a new locomotive with metadata
@app.route('/train', methods=['POST'])
def create_train():
    data = request.json
    if 'identifier' not in data:
        return jsonify({'message': 'Missing identifier in the request'}), 400

    trains_collection = db['trains']
    train = trains_collection.find_one({'identifier': data['identifier']})
    if not train:
        train_data = {
            'identifier': data['identifier'],
            'config': {
                'name': data.get('name', '')
            },
            'throttle': {
            'speed': 0,
            'direction': 0
            },
            'functions': {}
        }

        trains_collection.insert_one(train_data)

        return jsonify({'message': f'Train {data["identifier"]} created successfully'}), 201

    else:
        return jsonify({'message': f'Train {data["identifier"]} already exists'}), 400

# API endpoint to get train data including metadata, functions, and state
@app.route('/train/<int:train_id>', methods=['GET','POST'])
def control_train(train_id):
    if request.method == 'GET':
        trains_collection = db['trains']
        train = trains_collection.find_one({'identifier': train_id})

        if not train:
            return jsonify({'message': f'Train {train_id} not found'}), 404

        return parse_json(train), 200
    elif request.method == 'POST':
        data = request.json

        trains_collection = db['trains']
        train = trains_collection.find_one({'identifier': train_id})
        if not train:
            return jsonify({'message': f'Train {train_id} not found'}), 404

        train_metadata = train.get('config', {})
        train_metadata.update(data)
        trains_collection.update_one({'_id': train['_id']}, {'$set': {'config': train_metadata}})
        return jsonify({'message': f'Train {train_id} updated successfully'}), 200

# API endpoint to control the throttle of a train
@app.route('/train/<int:train_number>/throttle', methods=['PUT', 'GET'])
def control_train_throttle(train_number):
    if request.method == 'PUT':
        speed = request.json.get('speed', 0)
        direction = request.json.get('direction', 0)  # Replace with your desired default direction

        # Create or update train state
        train_state[train_number] = {'speed': speed, 'direction': direction}

        # Control the train throttle
        controller.throttle(train_number, speed, direction)

        return jsonify({'message': f'Train {train_number} throttle set to speed {speed} and direction {direction}'}), 200

    elif request.method == 'GET':
        if train_number in train_state:
            return jsonify(train_state[train_number]), 200
        else:
            return jsonify({'message': f'Train {train_number} state not found'}), 404

# API endpoint to control the function of a train
@app.route('/train/<int:train_number>/function/<int:function_id>', methods=['PUT'])
def control_train_function(train_number, function_id):
    switch = request.json.get('switch', 0)  # Replace with your desired default switch value

    # Control the train function
    controller.function(train_number, function_id, switch)

    return jsonify({'message': f'Train {train_number} function {function_id} set to {switch}'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)