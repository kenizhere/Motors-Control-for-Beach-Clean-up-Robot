import minimalmodbus
import serial
from serial_config import BAUD_RATE, TIMEOUT, SLAVE_ID

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

    def read_holding_register(self, register_address):
        """Read a holding register from the motor driver."""
        try:
            value = self.instrument.read_register(register_address, number_of_decimals=0)
            return value
        except Exception as e:
            print(f"Error reading register {register_address}: {e}")
            return None
    
    def write_holding_register(self, register_address, value):
        """Write to a holding register on the motor driver."""
        try:
            self.instrument.write_register(register_address, value)
            return True
        except Exception as e:
            print(f"Error writing to register {register_address}: {e}")
            return False
    
    def close(self):
        """Close the serial connection."""
        self.instrument.close()