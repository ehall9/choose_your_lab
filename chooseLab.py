from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from time import sleep
from sense_hat import SenseHat
#import threading
from multiprocessing import Process, Value

s = SenseHat()
green = (0,255,0)
red = (255,0,0)
kit = MotorKit()

#speed = 1
#direction = 1
speed = Value('i', 1)
direction = Value('i', 1)


digits0_9 = [
    [2, 9, 11, 17, 19, 25, 27, 33, 35, 42],  # 0
    [2, 9, 10, 18, 26, 34, 41, 42, 43],      # 1
    [2, 9, 11, 19, 26, 33, 41, 42, 43],      # 2
    [1, 2, 11, 18, 27, 35, 41, 42],          # 3
    [3, 10, 11, 17, 19, 25, 26, 27, 35, 43], # 4
    [1, 2, 3, 9, 17, 18, 27, 35, 41, 42],    # 5
    [2, 3, 9, 17, 18, 25, 27, 33, 35, 42],   # 6
    [1, 2, 3, 9, 11, 19, 26, 34, 42],        # 7
    [2, 9, 11, 18, 25, 27, 33, 35, 42],      # 8
    [2, 9, 11, 17, 19, 26, 27, 35, 43]       # 9
]

def display_two_digits (a_number, color):

    global digits0_9
    black = (0, 0, 0)

    if a_number < 0:
        negative = True
        a_number = abs(a_number)
    else:
        negative = False

    first_digit = int(int(a_number / 10) % 10)
    second_digit = int(a_number % 10)

    # set pixels for the two digits
    pixels = [black for i in range(64)]
    digit_glyph = digits0_9[first_digit]
    for i in range(0, len(digit_glyph)):
        pixels[digit_glyph[i]] = color
    digit_glyph = digits0_9[second_digit]
    for i in range(0, len(digit_glyph)):
        pixels[digit_glyph[i]+4] = color

    # display the result
    s.set_pixels(pixels)

def motor_control(speed, direction):
    #global speed, direction
    while(True):
        kit.stepper1.onestep(direction=direction.value)
        print(0.001 / speed.value)
        sleep(0.001 / speed.value)

def sense_hat_monitor(speed, direction):
    #global speed, direction
    while(True):
        events = s.stick.get_events()
        if events:
            for e in events:
                if e.action != 'pressed':
                   continue
                if e.direction == "up":
                    direction.value = 1
                if e.direction == "down":
                    direction.value = 0
                if e.direction == "right":
                    if speed.value < 10:
                        speed.value += 1
                if e.direction == "left":
                    if speed.value > 1:
                        speed.value -= 1
        if direction.value == 1:
            display_two_digits(speed.value, green)
        else:
            display_two_digits(speed.value, red)


motor_process = Process(target=motor_control, args=(speed, direction))
monitor_process = Process(target=sense_hat_monitor, args=(speed, direction))

motor_process.start()
monitor_process.start()
