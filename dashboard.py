# Example of using the MQTT client class to subscribe to a feed and print out
# any changes made to the feed.  Edit the variables below to configure the key,
# username, and feed to subscribe to for changes.

# Import standard python modules.
import sys
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time, threading
import glo
# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
import temphumidity
import getlight
import board

ADAFRUIT_IO_KEY      = '66df32bd4a584ef1a4c0c3f742edc88b'
ADAFRUIT_IO_USERNAME = 'Nature0505'  # See https://accounts.adafruit.com
                                                    # to find your username.
# Set to the ID of the feed to subscribe to for updates.
ACTEM = 'ac'
AUTO = 'auto'
ACON = 'aconoff'
DOOR = 'door'
HUMID = 'humidifier'
SYSTEMON = 'onoffbutton'
LIGHT = 'light'


def dash_board(GPIO):
#def dash_board():
# Set to your Adafruit IO key & username below

    #GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    #GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
    # Define callback functions which will be called when certain events happen.
    def connected(client):
        # Connected function will be called when the client is connected to Adafruit IO.
        # This is a good place to subscribe to feed changes.  The client parameter
        # passed to this function is the Adafruit IO MQTT client so you can make
        # calls against it easily.
        #print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
        # Subscribe to changes on a feed named DemoFeed.
        client.subscribe(ACTEM)
        client.subscribe(AUTO)
        client.subscribe(ACON)
        client.subscribe(DOOR)
        client.subscribe(HUMID)
        client.subscribe(SYSTEMON)
        client.subscribe(LIGHT)
        
    def disconnected(client):
        # Disconnected function will be called when the client disconnects.
        print('Disconnected from Adafruit IO!')
        sys.exit(1)

    def message(client, feed_id, payload):
        # Message function will be called when a subscribed feed has a new value.
        # The feed_id parameter identifies the feed, and the payload parameter has
        # the new value.
        print('Feed {0} received new value: {1}'.format(feed_id, payload))
        
        if feed_id == 'onoffbutton':
            print(payload)
            if payload == "ON":
                publish_init()
                glo.start_system = True
            else:
                publish_off()
                glo.start_system = False
        elif feed_id == 'auto':
            if payload=='Auto':
                glo.auto_start = True
            elif payload=='Manul':
                glo.auto_start = False

        if glo.start_system and not glo.auto_start:
            #if feed_id != "auto":
                #auto_start = Falses
            if feed_id == 'ac':
                print(payload)
                if payload >= 20:
                    print("level 2")
                elif payloat < 20:
                    print("level 1")
            elif feed_id == "aconoff":
                if payload=='ON':
                    print("ON")
                elif payload=='OFF':
                    print("OFF")
            
            elif feed_id == 'door':
                if payload=='Close':
                    print(feed_id)
                elif payload=='Open':
                    print(feed_id)       
            elif feed_id == 'light':
                if payload=='ON':
                    print(feed_id)
                    print("ON")
                    GPIO.output(26, GPIO.HIGH) #Turn ON
                elif payload=='OFF':
                    print(feed_id)
                    print("OFF")
                    GPIO.output(26, GPIO.LOW) 
            elif feed_id == "humidifier":
                print(payload)
                if payload == 0:
                    pass
                    #GPIO.output(17, GPIO.HIGH) # Turn on
                elif payload == 1:
                    pass
                elif payload == 2:
                    pass
                elif payload == 3:
                    pass
                elif payload == 4:
                    pass
                else:
                    pass

    def publish_init():
        time.sleep(0.5)
        client.publish(ACTEM, 26)
        client.publish(AUTO, "Auto")
        time.sleep(0.5)
        #client.publish(ACON, "OFF")
        client.publish(DOOR, "OFF")
        #client.publish("humidity", glo.humid)
        time.sleep(0.5)
        #client.publish("temperature", glo.temp)
        #client.publish("lux", glo.light)
        #client.publish(LIGHT, "OFF")
        time.sleep(0.5)
        client.publish(HUMID, 0)
    
    def publish_off():
        time.sleep(1)
        #client.publish(SYSTEMON, "ON")
        client.publish(AUTO, "Manul")
        time.sleep(0.5)
        client.publish(ACON, "OFF")
        time.sleep(0.5)
        client.publish(DOOR, "OFF")
        #client.publish("humidity", glo.humid)
        time.sleep(0.5)
        #client.publish("temperature", glo.temp)
        #client.publish("lux", glo.light)
        client.publish(LIGHT, "OFF")
        time.sleep(0.5)
        client.publish(HUMID, 0)

    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_connect    = connected
    client.on_disconnect = disconnected
    client.on_message    = message

    # Connect to the Adafruit IO server.
    client.connect()
    client.loop_background()
    
    time.sleep(1)
    client.publish(SYSTEMON, "ON")

    def auto_control():
        while glo.code_run:
            print(glo.start_system)
            print("auto: " + str(glo.auto_start))
            if glo.start_system and glo.auto_start:
                if glo.temp and glo.humid:
                    print("temp: " + str(glo.temp))
                    if glo.temp < 20:
                        print("Opend the AC")
                        client.publish(ACON, "ON")
                    else:
                        print("Close the AC")
                        client.publish(ACON, "OFF")    
                    #time.sleep(2)
                    print("humid: " + str(glo.humid))
                    if glo.humid < 10:
                        print("Level1")
                        client.publish(HUMID, 5)
                    elif glo.humid < 20:
                        print("Level2")
                        client.publish(HUMID, 3)
                    elif glo.humid < 30:
                        client.publish(HUMID, 1)
                    else:
                        client.publish(HUMID, 0)

                #time.sleep(2)
                print("Light: " + str(glo.light))
                if glo.light < 400:
                    client.publish(LIGHT, "ON")
                    GPIO.output(26, GPIO.HIGH)
                else:
                    client.publish(LIGHT, "OFF")
                    GPIO.output(26, GPIO.LOW)

            time.sleep(10)

    def update_status():
        while glo.code_run:
            client.publish("humidity", glo.humid)
            time.sleep(10)
            client.publish("temperature", glo.temp)
            time.sleep(10)
            client.publish("lux", glo.light)
            time.sleep(10)

    time.sleep(0.3)
    t_control = threading.Thread(target=auto_control, name='control_system')
    t_control.start()

    t_dash = threading.Thread(target=update_status, name='status')
    t_dash.start()

    while glo.code_run:
        pass
    GPIO.cleanup()
    #t_control.join()
    #t_dash.join()









