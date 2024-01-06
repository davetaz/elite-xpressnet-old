class MockHornbyController:
    def __init__(self):
        self.connected = False

    def connection_open(self, device, baud):
        self.connected = True

    def connection_close(self):
        self.connected = False

    def throttle(self, speed, direction):
        # Simulate throttle control (update mock state)
        pass

    def function(self, num, switch):
        # Simulate function control (update mock state)
        pass