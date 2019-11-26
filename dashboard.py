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
    lock=threading.Lock()
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
                glo.start_system = False
                publish_off()  

        elif feed_id == 'auto':
            if payload == 'Auto':
                print("System has been changed to Auto model")
                glo.auto_start = True
            elif payload =='Manual':
                print("System has been changed to Manual model")
                glo.auto_start = False

        if glo.start_system and not glo.auto_start:
            if feed_id == "ac":
                print("feed_id == ac : {} ac_on: {}".format(feed_id == "ac", glo.ac_on))       
                if glo.ac_on:
                    glo.set_temp = int(payload)
                    print("AC has been changed to " + payload)
                    period = 21.5 + 0.2 *((33 - glo.set_temp)/16)
                    glo.ac.ChangeFrequency(1000/period)
                    glo.ac.ChangeDutyCycle(100 * (period - 20)/period)
            elif feed_id == "aconoff":
                if payload=='ON':
                    glo.ac_on = True
                    client.publish(ACTEM, glo.set_temp)
                    period = 21.5 + 0.2 *((33 - glo.set_temp)/16)
                    glo.ac.ChangeFrequency(1000/period)
                    glo.ac.ChangeDutyCycle(100 * (period - 20)/period)
                    print("AC ON")
                elif payload=='OFF':
                    glo.ac_on = False
                    print("AC OFF")
                    glo.ac.ChangeDutyCycle(0)
            
            elif feed_id == 'door':
                if payload=='Close':
                    print("close door")
                    glo.door.ChangeFrequency(1000/21.6)
                    glo.door.ChangeDutyCycle(100 * 1.6/21.6)
                    time.sleep(1)
                    glo.door.ChangeDutyCycle(0)
                elif payload=='Open':
                    glo.door.ChangeFrequency(1000/21.4)
                    glo.door.ChangeDutyCycle(100 * 1.4/21.4)   
                    time.sleep(1)
                    glo.door.ChangeDutyCycle(0) 
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
                #print(payload)
                if payload == "0":
                    print(payload)
                    glo.hum.ChangeDutyCycle(0)
                    #GPIO.output(17, GPIO.HIGH) # Turn on
                elif payload == "1":
                    print(payload)
                    glo.hum.ChangeFrequency(5)
                    glo.hum.ChangeDutyCycle(50)
                elif payload == "2":
                    glo.hum.ChangeFrequency(8)
                    glo.hum.ChangeDutyCycle(50)
                elif payload == "3":
                    glo.hum.ChangeFrequency(10)
                    glo.hum.ChangeDutyCycle(50)
                elif payload == "4":
                    glo.hum.ChangeFrequency(15)
                    glo.hum.ChangeDutyCycle(50)
                else:
                    glo.hum.ChangeFrequency(20)
                    glo.hum.ChangeDutyCycle(50)

    def publish_init():
        time.sleep(1)
        lock.acquire()
        glo.ac_on = True
        client.publish(ACTEM, 26)
        client.publish(AUTO, "Auto")
        time.sleep(1)
        #client.publish(ACON, "OFF")
        client.publish(DOOR, "OFF")
        #client.publish("humidity", glo.humid)
        time.sleep(1)
        client.publish(HUMID, 0)
        glo.hum.ChangeDutyCycle(0)
        lock.release()
    
    def publish_off():
        time.sleep(1)
        #client.publish(SYSTEMON, "ON")
        client.publish(AUTO, "Manual")
        glo.auto_start = False
        lock.acquire()

        time.sleep(1)
        client.publish(ACON, "OFF")

        glo.ac_on = False
        glo.ac.ChangeDutyCycle(0)

        time.sleep(1)
        client.publish(DOOR, "OFF")
        
        time.sleep(1)
        client.publish(LIGHT, "OFF")
        GPIO.output(26, GPIO.LOW)

        time.sleep(1)
        client.publish(HUMID, 0)
        glo.hum.ChangeDutyCycle(0)

        lock.release()
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

    def update_status():
        while glo.code_run:
            client.publish("humidity", glo.humid)
            time.sleep(10)
            client.publish("temperature", glo.temp)
            time.sleep(10)
            client.publish("lux", glo.light)
            time.sleep(10)

    time.sleep(0.3)

    t_dash = threading.Thread(target=update_status, name='status')
    t_dash.start()

    while glo.code_run:
        print("system" + str(glo.start_system))
        print("auto: " + str(glo.auto_start))
        
        if glo.start_system and glo.auto_start:
            print("temp: " + str(glo.temp))
            lock.acquire()
            if glo.temp > 30:
                glo.set_temp = 22
                glo.ac_on = True
                client.publish(ACON, "ON")
                period = 21.5 + 0.2 *((33 - glo.set_temp)/16)
                glo.ac.ChangeFrequency(1000/period)
                glo.ac.ChangeDutyCycle(100 * (period - 20)/period)
                client.publish(ACTEM, 22)
            elif glo.temp > 24:
                glo.set_temp = 25
                glo.ac_on = True
                client.publish(ACON, "ON")
                period = 21.5 + 0.2 *((33 - glo.set_temp)/16)
                glo.ac.ChangeFrequency(1000/period)
                glo.ac.ChangeDutyCycle(100 * (period - 20)/period) 
                client.publish(ACTEM, 25)
            else:
                print("Close the AC")
                client.publish(ACON, "OFF") 
                glo.ac_on = False
                glo.ac.ChangeDutyCycle(0)          
            time.sleep(1)
            print("humid: " + str(glo.humid))
            if glo.humid < 10:
                print("Level1")
                client.publish(HUMID, 5)
                glo.hum.ChangeFrequency(20)
                glo.hum.ChangeDutyCycle(50)
            elif glo.humid < 20:
                print("Level2")
                client.publish(HUMID, 3)
                glo.hum.ChangeFrequency(10)
                glo.hum.ChangeDutyCycle(50)
            elif glo.humid < 30:
                client.publish(HUMID, 1)
                glo.hum.ChangeFrequency(5)
                glo.hum.ChangeDutyCycle(50)
            else:
                client.publish(HUMID, 0)
                glo.hum.ChangeDutyCycle(0)

            time.sleep(1)
            print("Light: " + str(glo.light))
            if glo.light < 500:
                client.publish(LIGHT, "ON")
                GPIO.output(26, GPIO.HIGH)
            else:
                client.publish(LIGHT, "OFF")
                GPIO.output(26, GPIO.LOW)
            lock.release()
        time.sleep(10)

    GPIO.cleanup()
    #t_control.join()
    #t_dash.join()









