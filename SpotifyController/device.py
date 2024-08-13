class Device:
    def __init__(self, device_id, device_is_active, device_name,
                 device_supports_volume, device_type,
                 device_volume_percent):
        self.device_id = device_id
        self.device_is_active = device_is_active
        self.device_name = device_name
        self.device_supports_volume = device_supports_volume
        self.device_type = device_type
        self.device_volume_percent = device_volume_percent

    def __str__(self):
        string_repr = "Device Info:\n"
        string_repr += f"id: {self.device_id}\n"
        string_repr += f"playing: {self.device_is_active}\n"
        string_repr += f"name: {self.device_name}\n"
        string_repr += f"type: {self.device_type}\n"
        string_repr += f"volume support: {self.device_supports_volume}\n"
        string_repr += f"volume: {self.device_volume_percent}%"

        return string_repr
