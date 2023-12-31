import RPi.GPIO as GPIO

import time

import requests



GPIO.setmode(GPIO.BCM)



#samain sama pin di raspi

GPIO_TRIGGER = 18

GPIO_ECHO = 24

GPIO_TRIGGER1 = 5

GPIO_ECHO1 = 6

GPIO_TRIGGER2 = 23

GPIO_ECHO2 = 25

#GPIO_TRIGGER3 = 20

#GPIO_ECHO3 = 21



#inisialisasi pin raspi

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)

GPIO.setup(GPIO_ECHO1, GPIO.IN)

GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)

GPIO.setup(GPIO_ECHO2, GPIO.IN)

#GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)

#GPIO.setup(GPIO_ECHO3, GPIO.IN)



#cek di ubidots

TOKEN = "BBFF-bEBRPk4JfouuwB1JBwoVQ9dcCEfnKL"

DEVICE_LABEL = "sintia"

VARIABLE_LABEL_1 = "sensor1"

VARIABLE_LABEL_2 = "sensor2"

VARIABLE_LABEL_3 = "sensor3"

#VARIABLE_LABEL_4 = "sensor4"



#buat ukur kapasitas

def distance(trigger_pin, echo_pin):

    GPIO.output(trigger_pin, True)

    time.sleep(0.00001)

    GPIO.output(trigger_pin, False)



    StartTime = time.time()

    StopTime = time.time()



    while GPIO.input(echo_pin) == 0:

        StartTime = time.time()



    while GPIO.input(echo_pin) == 1:

        StopTime = time.time()



#perhitungan kapasitas

    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

    distance = distance / 30 #panjang tempat sampah

    distance = distance * 100



    return distance



def send_data_to_ubidots(variable_label, value):

    url = "http://industrial.api.ubidots.com/api/v1.6/devices/{device_label}/{variable_label}/values"

    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    payload = {"value": value}



    try:

        response = requests.post(url.format(device_label=DEVICE_LABEL, variable_label=variable_label), headers=headers, json=payload)

        if response.status_code == 201:

            print("Data sent to Ubidots successfully.")

        else:

            print("Failed to send data to Ubidots. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:

        print("An error occurred while sending data to Ubidots:", str(e))



if __name__ == '__main__':

    try:

        while True:

            dist1 = distance(GPIO_TRIGGER, GPIO_ECHO)

            print("Kapasitas Terukur 1 = %.1f " % dist1)

            send_data_to_ubidots(VARIABLE_LABEL_1, dist1)



            dist2 = distance(GPIO_TRIGGER1, GPIO_ECHO1)

            print("Kapasitas Terukur 2 = %.1f " % dist2)

            send_data_to_ubidots(VARIABLE_LABEL_2, dist2)



            dist3 = distance(GPIO_TRIGGER2, GPIO_ECHO2)

            print("Kapasitas Terukur 3 = %.1f " % dist3)

            send_data_to_ubidots(VARIABLE_LABEL_3, dist3)



            #dist4 = distance(GPIO_TRIGGER3, GPIO_ECHO3)

           # print("Kapasitas Terukur 4 = %.1f " % dist4)

            #send_data_to_ubidots(VARIABLE_LABEL_4, dist4)



            time.sleep(1)



    except KeyboardInterrupt:

        print("Measurement stopped by User")

        GPIO.cleanup()

