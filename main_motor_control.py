import minimalmodbus_for_driver
from serial_config import LEFT_PORT, RIGHT_PORT

def main():
    # Initialize motor drivers for left and right motors
    left_motor = minimalmodbus_for_driver.MotorDriver(LEFT_PORT)
    right_motor = minimalmodbus_for_driver.MotorDriver(RIGHT_PORT)
    
    try: 
        left_motor.write_holding_register(0x0001, 100)  # Example: Set left motor speed to 100
        right_motor.write_holding_register(0x0001, 100) # Example: Set right motor speed to 100
    
    
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        left_motor.close()
        right_motor.close()