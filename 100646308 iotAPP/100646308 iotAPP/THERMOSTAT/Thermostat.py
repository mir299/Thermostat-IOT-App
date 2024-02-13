class SmartThermostat:
    def __init__(self):
        self.temperature = 72  # Default temperature in Fahrenheit
        self.mode = "OFF"  # Possible modes: "HEATING", "COOLING", "OFF"

    def set_temperature(self, temp):
        try:
            temp = int(temp)
            if 50 <= temp <= 90:  # Assuming a reasonable temperature range
                self.temperature = temp
                return f"Temperature set to {self.temperature}°F"
            else:
                return "Temperature must be between 50°F and 90°F"
        except ValueError:
            return "Invalid temperature value"

    def set_mode(self, mode):
        mode = mode.upper()
        if mode in ["HEATING", "COOLING", "OFF"]:
            self.mode = mode
            return f"Mode set to {self.mode}"
        else:
            return "Invalid mode. Available modes: HEATING, COOLING, OFF"

    def get_status(self):
        return f"Current setting - Mode: {self.mode}, Temperature: {self.temperature}°F"
