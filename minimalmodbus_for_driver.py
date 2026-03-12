import minimalmodbus
# import serial (check back when needed for more advanced serial configuration)
from serial_config import BAUD_RATE, TIMEOUT, SLAVE_ID
from math import pi

"""
Important registers for motor control: 
- 0x8106: Control register (write to start/stop motor)
- 0x8204: Speed control register (write to set speed)
- 0x8206: Speed feedback register (read to get current speed)
- 0x820B: Voltage feedback register (read to get current voltage)
- 0x820F: Alarm status register (read to check for any active alarms)

"""


class MotorDriver:
    """Framework for controlling motor drivers via Modbus RTU serial communication."""
    
    def __init__(self, port, slave_id=SLAVE_ID, baudrate=BAUD_RATE, timeout=TIMEOUT):
        """        
        port: Serial port name (like "/dev/ttyUSB0")
        slave_id: Modbus slave ID
        baudrate: Serial baud rate
        timeout: Serial timeout in seconds
        """
        self.port = port
        self.slave_id = slave_id
        self.instrument = minimalmodbus.Instrument(port, slave_id)
        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.timeout = timeout
        self.instrument.debug = False


    def read_register(self, register_address):
        try:
            return self.instrument.read_register(register_address, number_of_decimals=0)
        except Exception as e:
            print(f"Error reading register {register_address}: {e}")
            return None
    
    def write_register(self, register_address, value):
        try:
            self.instrument.write_register(register_address, value)
            return True
        except Exception as e:
            print(f"Error writing to register {register_address}: {e}")
            return False
    
    """
    For control register 0x8106, the bits are defined as follows:
    Low byte:   Bit 0: start stop EN (1: start, 0: stop)
                Bit 1: Direction FR (1: reverse, 0: forward) 
                Bit 2: Brake BK (1: enable brake, 0: no brake)
    High byte:  Bit 0: Control mode (1: internal, 0: external)
                Bit 1: speed way (1: internal, 0: external) 
                Bit 2: sensor sensorless (1:sensor, 0: sensorless)
                Bit 3: open loop (1: open loop, 0: closed loop)
                Bit 4: Hall Angle (1:60 degrees, 0:120 degrees)
                Bit5: 0
                Bit6: 0
    """
    def move_forward(self):
        # Start motor, forward direction, no brake (00000111 00000001 in binary)
        self.write_register(0x8106, 0x0701)
    
    def move_reverse(self):
        # Start motor, reverse direction, no brake (00000111 00000011 in binary)
        self.write_register(0x8106, 0x0703)
    
    def stop_without_brake(self):
        # Stop motor, no brake (00000111 00000100 in binary)
        self.write_register(0x8106, 0x0700)

    def stop_with_brake(self):
        # Stop motor, with brake (00000111 00000100 in binary)
        self.write_register(0x8106, 0x0704)

    def set_speed(self, speed):
        self.write_register(0x8204, speed)

    # Read the speed register and return the speed in RPM 
    def read_speed(self):
        speed_in_rpm = self.read_register(0x8206) 
        return speed_in_rpm

    # Read the voltage register and return the voltage in volts (value is in 0.1V units)
    def read_voltage(self):
        print(self.read_register(0x820B)) # example: 240=24V

    # Read the alarm status register and print out any active alarms
    def read_alarm(self):
        alarm = self.read_register(0x820F) 
        if alarm is not None:
            alarm_message = {
                0x01: "Locked rotor alarm",
                0x02: "Mean current alarm",
                0x04: "Hall fault",
                0x08: "Power Low Voltage Alarm",
                0x10: "Power supply high voltage alarm",
                0x20: "Peak current alarm",
                0x40: "Hardware peak current alarm",
                0x80: "Temperature alarm"
            }
            print("Alarm status: ")
            for key, message in alarm_message.items(): # have to add .items() or else it would return keys only.
                if alarm & key:
                    print(f" - {message}")
            

    def close(self):
        """Close the serial connection."""
        self.instrument.close()