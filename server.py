import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

Connected = False #global variable for the state of the connection
broker_address = "m15.cloudmqtt.com" 
port = 14510
user = "tfxbtqjx"
password = "VqANh1ktZMho"
sub_topic = "motor/light"    # receive messages on this topic

servo_pin = 18

#Servo moviment
deg_0_pulse   = 0.5 
deg_180_pulse = 2.5
f = 50.0

# Pulse Length
period = 1000/f
k      = 100/period
deg_0_duty = deg_0_pulse*k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k


def set_angle(angle):
        print("Set Angle " + angle)

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    
    
    if rc == 0:
        print("Connected to broker")
        client.subscribe(sub_topic)
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
        print("Connection failed")
        
    

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    
    message = str(msg.payload.decode("utf-8"))
    print(msg.topic+" "+message)
    
    if msg.topic == "motor/light":
        
        #Start GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin,GPIO.OUT)
        pwm = GPIO.PWM(servo_pin,f)
        pwm.start(0)

        angle = float(0)
        
        if message == "on":
            angle = float(40)
        if message == "off":
            angle = float(0)
        
        duty = deg_0_duty + (angle/180.0)* duty_range
        
        print(duty)
        pwm.ChangeDutyCycle(duty)
        
        print("Done")
        time.sleep(.6)
        
        print("cleaning up")
        GPIO.cleanup()


client = mqtt.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_start()
