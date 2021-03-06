


from pykeyboard import PyKeyboard
import paho.mqtt.client as mqtt
import re
import json
import time
data={
    'led_r':512,
    'led_g':0,
    'led_b':1023
}
host = 'www.bananalife.top'
port = 1883
'''
ctrl+alt+p   play/suspend
ctrl+alt+H   left
ctrl+alt+L   right
ctrl+alt+J   down
ctrl+alt+K   up
'''
k = PyKeyboard()
netcase = {
    'play': [k.control_key, k.alt_key, 'p'],
    'left': [k.control_key, k.alt_key, 'h'],
    'right': [k.control_key, k.alt_key, 'l'],
    'down': [k.control_key, k.alt_key, 'j'],
    'up': [k.control_key, k.alt_key, 'k'],
}


#

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe('beat')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = str(msg.payload)
    print(msg.topic + " " + data)
    for i in netcase:
        find = re.findall(i, data)
        if find:
            k.press_keys(netcase[i])
            return


client = mqtt.Client(client_id='zengfu', clean_session=True,)
client.username_pw_set('zengfunuaa@126.com','71451085a')
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, port)


while True:
    client.loop_start()
    client.publish('/mytopic', json.dumps(data))
    print len(json.dumps(data))
    time.sleep(2)
