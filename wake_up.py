from espeak import espeak
import time
import datetime
import requests

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.OUT)


    

hours = 9
mins = 52
if mins > 0 and hours < 13:
    espeak.synth("I will wake you up at " + str(hours) + "  " + str(mins) + "am. Good night,sir")

elif mins > 0 and hours >= 13:
    espeak.synth("I will wake you up at " + str(hours) + "  " + str(mins) + "pm. Good night,sir")

elif mins <= 0 and hours >= 13:
    espeak.synth("I will wake you up at " + str(hours) + "pm. Good night,sir")

else:
    espeak.synth("I will wake you up at " + str(hours) + "am. Good night,sir")
    


espeak.set_voice("en")


while True:
    if GPIO.input(18) == 1 or GPIO.input(23) == 1:
        if GPIO.input(18) == 1:
            time.sleep(0.5)
            GPIO.output(24,True)
            time.sleep(0.40)
            GPIO.output(24,False)
            
            hours = hours + 1
            if hours == 24:
                hours = 00
            print(hours)

        if GPIO.input(23) == 1:
            time.sleep(0.5)
            GPIO.output(24,True)
            time.sleep(0.40)
            GPIO.output(24,False)
            mins = mins + 5
            if mins >= 60:
                mins = mins - 60
            print(mins)

    
    current_time = time.localtime()
    if current_time[3] == int(hours) and current_time[4] == int(mins) and current_time[5] <= 5:
        if current_time[3] < 13:
            espeak.synth("Good morning sir. The time is" + str(current_time[3]) + "hours" + str(current_time[4]) + "minutes")

        else:
            espeak.synth("Hello Sir. The time is" + str(current_time[3] - 12) + "hours" + str(current_time[4]) + "minutes")

        dat = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=641005,in&appid=fcc7cf88eaed21135af4a9e7d912de81").json()
        data_weather = dat["weather"][0]["description"]
        print(data_weather)
        data_temp = dat["main"]["temp"]
        print(data_temp)
        data_temp_c = data_temp - 273.16
        temp_c = int(round(data_temp_c, 0))
        time.sleep(3)
        if temp_c <= 28:
            espeak.synth("The weather is a cold" + str(temp_c) + "degrees celcius")
            time.sleep(2.5)
            espeak.synth("with" + data_weather)

        if temp_c > 28:
            espeak.synth("The weather is warm at" + str(temp_c) + "degrees celcius")
            time.sleep(2.5)
            espeak.synth("with" + data_weather)


##    time.sleep(20)
    
