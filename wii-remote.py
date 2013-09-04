import cwiid
import time
import serial

# Taken from the example provided at http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/resources/wiimote.py
# This attempts to take the input from a Wiimote and feed it to a serial interface connected to a micro-controller which powers the motors.
# Why? Because we can!

# Setup serial interface to ATmega via PI's I2C interface (not your normal USB as for most devices)
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.open()
ser.isOpen()

inByte = ser.read()
if (inByte == 'A'):
       ser.flushOutput()
ser.write('A')
       print "Handshake with micro-controller complete"

# Connect our Wii Remote
print 'Press 1+2 on your Wiimote now...'
wm = None
i=2
while not wm:
    try:
            wm=cwiid.Wiimote()
    except RuntimeError:
    if (i>5):
        print("cannot create connection")
        servos.setPWM(15,0)
        quit()
    print "Error opening wiimote connection"
    print "attempt " + str(i)
    i +=1

#set wiimote to report button presses and accelerometer state
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

#turn on led to show connected
wm.led = 1

while True:
    buttons = wm.state['buttons']
    if (buttons & cwiid.BTN_B):
        #boost mode
        speedModifier=200
    else:
        speedModifier=150

    if (buttons & cwiid.BTN_2):
        #print((wm.state['acc'][1]-125))
        #Write direction and speed to serial
        ser.write("k\n")
        while (buttons & cwiid.BTN_2):
            print (wm.state['acc'][1]-125)
            ser.write(str(speedModifier - wm.state['acc'][1]))
            ser.write("\n")
    elif (buttons & cwiid.BTN_1):
        #print ~(wm.state['acc'][1]-125)
        #Write direction and speed to serial
        ser.write("j\n")
        while (buttons & cwiid.BTN_1):
            print (wm.state['acc'][1]-125)
            ser.write(str(speedModifier - wm.state['acc'][1]))
            ser.write("\n")
    else:
        #print("stop")
        #Write "s" to serial
        ser.write("s\n")
    time.sleep(0.2)
