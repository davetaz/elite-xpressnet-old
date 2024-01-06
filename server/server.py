from flask import Flask, request, jsonify

import time

app = Flask(__name__)

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