import minimalmodbus_for_driver
from serial_config import LEFT_PORT, RIGHT_PORT
from time import sleep
from cmath import pi

# Initialize motor drivers for left and right motors
left_motor = minimalmodbus_for_driver.MotorDriver(LEFT_PORT)
right_motor = minimalmodbus_for_driver.MotorDriver(RIGHT_PORT)

def turn_on_motors():
    """Turn on both motors"""
    left_motor.move_forward()  # Start left motor
    right_motor.move_forward()  # Start right motor

def stop_motors():
    left_motor.stop_with_brake()  
    right_motor.stop_with_brake()  

def stop_without_brake():
    left_motor.stop_without_brake()  
    right_motor.stop_without_brake()

def go_straight():
    left_motor.set_speed(100)  
    right_motor.set_speed(100)

def turn_left():
    left_motor.set_speed(50)  
    right_motor.set_speed(150)  

def turn_right():
    left_motor.set_speed(150)  
    right_motor.set_speed(50)  

def reverse():
    stop_motors()  
    sleep(0.5)  # Short delay to ensure motors have stopped
    left_motor.move_reverse()  
    right_motor.move_reverse()  

def read_speeds():
    left_speed = left_motor.read_speed()
    right_speed = right_motor.read_speed()
   # speed_in_meter_per_second_left = (left_speed + right_speed) * pi * RADIUS / 60  # add RADIUS after knowing the wheel sprocket radius
    print(f"Left Motor Speed: {left_speed} RPM, Right Motor Speed: {right_speed} RPM")
   # print(f"Speed in m/s: {speed_in_meter_per_second_left}")

def main():
    
    try: 
        turn_on_motors()
        sleep(2)  # Run motors for 2 seconds
        go_straight()
        sleep(2)
        turn_left()
        sleep(2)
        turn_right()
        sleep(2)
        reverse()
        sleep(2)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        left_motor.close()
        right_motor.close()