# bmp280 Library Credits :
# Author David Stenwall Wahlund (david at dafnet.se)
# https://github.com/dafvid/micropython-bmp280

# import the required libraries
from bmp280 import *
from machine import Pin, I2C, PWM, Timer
import utime, _thread, math
from ssd1306 import SSD1306_I2C
from random import randint
from time import ticks_ms, sleep

led = Pin("LED", Pin.OUT)

  
print("creation d'un nouveau fichier")
r = randint (0,1000000000)
fichier =("BMP280_Tableau")+(str(r))+(".csv")
print(fichier)#juste pour verif le nom du fichier en debug
tableau_valeur = open(fichier,'w')
tableau_valeur.write('Temperature ; Pression ; Altitude ; Temps')
tableau_valeur.close()


sea_level_pressure = 1013.25
cpt=0
boutton = Pin(10, mode=Pin.IN, pull=Pin.PULL_UP)
buzzer = PWM(Pin(16))
buzzer.freq(400)
buzzer.duty_u16(1000)
utime.sleep(0.1)
buzzer.duty_u16(0)


# Caliberation error in pressure
# use it according to your situation
# it helps in calibrating altitude .It is optional, else put ERROR = 0 
ERROR = -3 # hPa 

# declare pins for I2C communication
sclPin = Pin(9) # serial clock pin
sdaPin = Pin(8) # serial data pin

# Initiate I2C 
i2c_object = I2C(0,              # positional argument - I2C id
                 scl = sclPin,   # named argument - serial clock pin
                 sda = sdaPin,   # named argument - serial data pin
                 freq = 1000000) # named argument - i2c frequency


WIDTH =128 
HEIGHT= 32
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c_object)
import framebuf

TH = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x04\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10\x00\x00\x08\x10\x00\x00\x00 \x00\x00\x00 \x00\x00\x00\x02\x00\x00\x00\x02\x00\x01\x00\x00\x00\t\x00\x00B\x02\x0f\xe0@\x00\x00\x00\x80\x00\x7f\xf8\x00\x00\x00\x00\x00\x07\xff\xfc\x80\x00\x00\x00\x00\x0f\xff\xfc\x00\x00\x00\x00\x00/\xff\xfe\x04\x00\n\x00\x00\x03\xff\xfe\x00\x00\x00\x00\x02\x03\xff\xff\x00\x02\x00\x00\x00\x00\x7f\xff?\xfc\x00P\x00\x00?\xff\xff\xff\x80\x00\x00\x00\x0f\xff\xff\xff\xf0\x08\x00\xbe\x07\xff\xff\xff\xfc\x10\x01\xff\x8f\xff\xff\xff\xfc\x10\x03\xff\xdf\xff\xff\xff\xfd\x80\x07\xe0\xdf\xff\xff\xff\xfd\xc0\x0f\x86_\xff\xff\xe7\xfd\xe0\x1f\x9e_\xff\xff\xc3\xfd\xf8?\x1e_\xff\xff\x81\xfd\xf8??_\xff\xff\x81\xfd\xfc?>_\xff\xff\x91\xfd\xfc?\x1e_\xff\xff\x81\xfd\xf8\x1f\x9e_\xff\xff\xc3\xfd\xf0\x0f\xc6_\xff\xff\xe7\xfd\xe4\x07\xe0\xdf\xff\xff\xff\xfd\xc0\x03\xff\xdf\xff\xff\xff\xff\x00\x01\xff\x8f\xff\xff\xff\xfc\x00\x00>\x07\xff\xff\xff\xfc\x00\x00\x04\x0f\xff\xff\xff\xf2\x00\x00\x00?\xff\xff\xff\x80\x00\x00\x00\x7f\xff?\xfc\x00\x00\x01\x01\xff\xff\x00\x00\x00\x00\x00\x03\xff\xfe\x00\x00\x00\x00@\x0f\xff\xfe\x00\x00\x00\x00\x04\x0f\xff\xfc\x04\x08@\x00\x00C\xff\xfc\x00\x00\x00\x00\x00@\x7f\xf9\x00\x00\x00\x00\x00\x80\x0f\xe0\x01\x00\x00\x00\x02\x10\x80\x00\x08\x00\x04 \x08\x02\x81\t\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\xa0\x02\x00\x00\x00\x00\x10\x00\x80\x08@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 @\x10\x00\x00\x10\x80\x08\x10\x00\x00\x00P\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00')

fb = framebuf.FrameBuffer(TH,128,32, framebuf.MONO_HLSB)
oled.fill(0)
oled.blit(fb,60,0)
oled.show()
utime.sleep(1)

texte_complet = fichier
longueur = len(texte_complet)
for n in range(0,longueur - 1):
    oled.fill(0)    
    texte = texte_complet[n:16 + n]
    oled.text(texte,0,15)
        #lignes horizontales
    oled.hline(0,7,127,1)
    oled.hline(0,30,127,1)
    oled.show()
    utime.sleep(0.1)

texte_complet = "Appuie long RAZ      "
longueur = len(texte_complet)
for n in range(0,longueur - 1):
    oled.fill(0)    
    texte = texte_complet[n:16 + n]
    oled.text(texte,0,15)
        #lignes horizontales
    oled.hline(0,7,127,1)
    oled.hline(0,30,127,1)
    oled.show()
    utime.sleep(0.1)

#oled.fill(0)
oled.text("Bon vol !", 30, 16)
oled.show()

# create a BMP 280 object
bmp280_object = BMP280(i2c_object,
                       addr = 0x76, # change it 
                       use_case = BMP280_CASE_INDOOR)

# configure the sensor
# These configuration settings give most accurate values in my case
# tweak them according to your own requirements

bmp280_object.power_mode = BMP280_POWER_NORMAL

bmp280_object.oversample = BMP280_OS_HIGH

bmp280_object.temp_os = BMP280_TEMP_OS_8

bmp280_object.press_os = BMP280_TEMP_OS_4


bmp280_object.standby = BMP280_STANDBY_250

bmp280_object.iir = BMP280_IIR_FILTER_2

# Function for calculation altitude from pressure and temperature values
# because altitude() method is not present in the Library

def altitude_HYP(hPa , temperature):
    # Hypsometric Equation (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 # hPa      
    pressure_ratio = sea_level_pressure/local_pressure # sea level pressure = 1013.25 hPa
    h = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return h


# altitude from international barometric formula, given in BMP 180 datasheet
def altitude_IBF(pressure):
    local_pressure = pressure    # Unit : hPa
    sea_level_pressure = 1013.25 # Unit : hPa
    #sea_level_pressure = 1009 # QNH Unit : hPa
    
    pressure_ratio = local_pressure / sea_level_pressure
    
    altitude = 44330*(1-(pressure_ratio**(1/5.255)))
    return altitude

def affichage(afficheur) :
    if afficheur ==0 :
        oled.text("Alt_ref :", 0, 0)
        oled.text(str(round(altitude0,2)), 70, 0)
        oled.text("Alt:", 0, 8)
        oled.text(str(round(altitude,2)), 70, 8)
        oled.text("Alt_M:", 0, 16)
        oled.text(str(round(altitude_max,2)), 70, 16)
        oled.text("Tps (s):",00,24)
        oled.text(str(elapsed_time/1000),70,24)
        oled.text(str(r), 0, 48)
        oled.show()
        led.off()

    if afficheur ==1:
        oled.text("Alt_ref :", 0, 0)
        oled.text(str(round(altitude0,2)), 70, 0)
        oled.text("Haut:", 0, 8)
        oled.text(str(round(altitude-altitude0,2)), 70, 8)
        oled.text("Haut_M:", 0, 16)
        oled.text(str(round(altitude_max-altitude0,2)), 70, 16)
        oled.text("Tps (s):",00,24)
        oled.text(str(elapsed_time/1000),70,24)
        oled.show()
        led.off()

    if afficheur ==2:
        oled.text("Temperature:", 0, 0)
        oled.text(str(round(temperature_c,1)), 0, 8)
        oled.text("Pression actuelle :", 0, 16)
        oled.text(str(round(pressure_hPa,2)), 0, 24)
        oled.show()
        led.off()

    if afficheur == 3:
        oled.text("Num fichier:", 0, 0)
        oled.text(str(r), 0, 8)
        oled.show()
        led.off()


altitude_max = -999
utime.sleep (0.5)
#oled.text("Appuyer sur le bouton pour calibrer le QFE", 0, 8)
#oled.show()
#pressure = bmp280_object.pressure



temperature_c = bmp280_object.temperature # degree celcius
    
    # convert celcius to kelvin
temperature_k = temperature_c + 273.15
    
    # accquire pressure value
pressure = bmp280_object.pressure  # pascal
    
    # convert pascal to hectopascal (hPa)
    # 1 hPa = 100 Pa
    # Therefore 1 Pa = 0.01 hPa
pressure_hPa = ( pressure * 0.01 ) + ERROR # hPa
    
    # accquire altitude values from HYPSOMETRIC formula
h = altitude_HYP(pressure_hPa, temperature_k)
    
    # accquire altitude values from International Barometric Formula
altitude0 = altitude_IBF(pressure_hPa)

oled.fill(0)
oled.text("Alt_0:", 0, 16)
oled.text(str(round(altitude0,2)), 70, 16)
oled.show()
utime.sleep(1)

#_thread.start_new_thread(thread_anim, ()) 

tableau_valeur = open(fichier,'a') #ouverture
start_time = 0
start = 0
stop = 0
elapsed_time = 0
afficheur = 0
apogee = 0
alt2=altitude0+1.5

while True:
    #elapsed_time = ticks_ms() - start_time  # Calcule le temps écoulé
    #print(f"Temps écoulé: {elapsed_time} millisecondes")
    oled.fill(0)
#    rled.on()
    # accquire temperature value in celcius
    temperature_c = bmp280_object.temperature # degree celcius
    
    # convert celcius to kelvin
    temperature_k = temperature_c + 273.15
    
    # accquire pressure value
    pressure = bmp280_object.pressure  # pascal
    
    # convert pascal to hectopascal (hPa)
    # 1 hPa = 100 Pa
    # Therefore 1 Pa = 0.01 hPa
    pressure_hPa = ( pressure * 0.01 ) + ERROR # hPa
    
    # accquire altitude values from HYPSOMETRIC formula
    h = altitude_HYP(pressure_hPa, temperature_k)
    
    # accquire altitude values from International Barometric Formula
    altitude = altitude_IBF(pressure_hPa)
    
    #print("Temperature : ",temperature_c," Degree Celcius")
    #print("Pressure : ",pressure," Pascal (Pa)")
    #print("Pressure : ",pressure_hPa," hectopascal (hPa) or millibar (mb)")
    #print("Altitude (Hypsometric Formula) : ", h ," meter")
    #print("Altitude (International Barometric Formula) : ", altitude ," meter")

    temp =str(temperature_c)
    press = str(pressure_hPa)
    alt=str(altitude)
    pt = str(elapsed_time/1000)
    tableau_valeur = open(fichier,'a')
    tableau_valeur.write("\n")
    tableau_valeur.write(temp+";"+press+";"+alt+";"+pt)
    tableau_valeur.close()
    led.on()

    if boutton.value()==0:
        utime.sleep(0.5)
        if boutton.value()==0:
            altitude_max=0
            altitude0 = altitude_IBF(pressure_hPa)
            alt2=altitude0+1.5
            elapsed_time = 0
            apogee = 0
            start = 0
            oled.fill(0)
            led.on()
            oled.text("RAZ Altitude max", 0, 16)
            oled.show()
            utime.sleep(0.8)
            led.off()
            oled.fill(0)
        
        else :
            afficheur += 1
            if afficheur == 4 :
                afficheur = 0
    
    
    if altitude>altitude_max : 
        altitude_max=altitude
    
    #alt=altitude0+2
    #print (alt2)
    # Démarrage chrono lorsque l'altitude dépasse celle de départ plus 1,5m pour pallier aux dérives de pression :
    if altitude > alt2 and start == 0:
        #print ("c'est parti !")
        tableau_valeur = open(fichier,'a')
        tableau_valeur.write("\n")
        tableau_valeur.write("Départ")
        tableau_valeur.close()
        start = 1
        start_time = ticks_ms()
        
    
    # Défilement du chrono à condition qu'il soit parti et que l'altitude soit supérieur à celle du départ plus 1,5m, la condition sur start permet de remettre le chrono à zero :
    if altitude > alt2 and start == 1 :
        elapsed_time = ticks_ms() - start_time  

    #détection de l'apogée (-1m pour éviter que ça se déclenche avec la dérive):
    if altitude < altitude_max-1 and start == 1 :
        tableau_valeur = open(fichier,'a')
        tableau_valeur.write("\n")
        tableau_valeur.write("Apogée !")
        tableau_valeur.close()
        apogee = 1
    
    # Arrêt du chrono et remise à zero suite à un atterrissage :
    if altitude <= altitude0 and start == 1 :
        tableau_valeur = open(fichier,'a')
        tableau_valeur.write("\n")
        tableau_valeur.write("Atterrissage")
        tableau_valeur.close()
        start = 0
        #Pour éviter que ça se remette à zéro intempestivement :
        alt2 = alt2+10
    
        #Buzzer pour retrouver la fusée au sol  
    #if altitude<altitude_max :
        #print (round(altitude-altitude0,0))
        #if round(altitude-altitude0,0) < 2 :
    if apogee == 1 : 
        buzzer.freq(400)
        buzzer.duty_u16(1000)
        utime.sleep(0.05)
        buzzer.duty_u16(0)
    
    #print (alt2)
    
    affichage(afficheur)    
 
