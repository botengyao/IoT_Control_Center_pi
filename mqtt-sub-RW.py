# Example of using the MQTT client class to subscribe to a feed and print out
# any changes made to the feed.  Edit the variables below to configure the key,
# username, and feed to subscribe to for changes.

# Import standard python modules.
import sys
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
import random


# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = '66df32bd4a584ef1a4c0c3f742edc88b' 
ADAFRUIT_IO_USERNAME = 'Nature0505'  # See https://accounts.adafruit.com
                                                    # to find your username.

# Set to the ID of the feed to subscribe to for updates.
FEED_ID1 = 'ac'
FEED_ID2 = 'auto'
FEED_ID3 = 'aconff'
FEED_ID4 = 'door'
FEED_ID5 = 'humidifier'
FEED_ID6 = 'onoffbutton'
FEED_ID7 = 'light'
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
    client.subscribe(FEED_ID1)
    client.subscribe(FEED_ID2)
    client.subscribe(FEED_ID3)
    client.subscribe(FEED_ID4)
    client.subscribe(FEED_ID5)
    client.subscribe(FEED_ID6)
    client.subscribe(FEED_ID7)
    
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
   # if payload=='ON':
   #     print("ON")
    #GPIO.output(17, GPIO.HIGH) # Turn on
   # elif payload=='OFF':
   #     print("OFF")
    #print(payload)
# GPIO.output(17, GPIO.LOW) # Turn off
    
# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()
# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_background()
while True:
    print("s")
    time.sleep(10)
"""
while True:
    time.sleep(10)
    value = random.randint(16, 32)
    #print('Publishing {0} to {1}.'.format(value, FEED_ID))
    #client.publish(FEED_ID, value)
"""