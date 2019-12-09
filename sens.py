import smbus
import json
import requests

def piReadSensorHuhData():
    DEVICE_BUS = 1
    DEVICE_ADDR = 0x17

    TEMP_REG = 0x01
    LIGHT_REG_L = 0x02
    LIGHT_REG_H = 0x03
    STATUS_REG = 0x04
    ON_BOARD_TEMP_REG = 0x05
    ON_BOARD_HUMIDITY_REG = 0x06
    ON_BOARD_SENSOR_ERROR = 0x07
    BMP280_TEMP_REG = 0x08
    BMP280_PRESSURE_REG_L = 0x09
    BMP280_PRESSURE_REG_M = 0x0A
    BMP280_PRESSURE_REG_H = 0x0B
    BMP280_STATUS = 0x0C
    HUMAN_DETECT = 0x0D

    bus = smbus.SMBus(DEVICE_BUS)

    aReceiveBuf = []

    aReceiveBuf.append(0x00) # 占位符

    for i in range(TEMP_REG,HUMAN_DETECT + 1):
        aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

    if aReceiveBuf[STATUS_REG] & 0x01 :
        print("Off-chip temperature sensor overrange!")
        externalTemp='-'
    elif aReceiveBuf[STATUS_REG] & 0x02 :
        print("No external temperature sensor!")
        externalTemp='-'
    else :
        externalTemp =  aReceiveBuf[TEMP_REG]
        print("TempSensor: {} Celcius".format(externalTemp))
        #print("Current off-chip sensor temperature = %d Celsius" % aReceiveBuf[TEMP_REG])

    if aReceiveBuf[STATUS_REG] & 0x04 :
        print("Onboard brightness sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x08 :
        print("Onboard brightness sensor failure!")
    else :
        brightnessVal = aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]
        print("LightSensor: {} Lux".format(brightnessVal))
        #print("Current onboard sensor brightness = %d Lux" % (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]))

    tempOnboard = aReceiveBuf[ON_BOARD_TEMP_REG]
    humidity = aReceiveBuf[ON_BOARD_HUMIDITY_REG]
    print("Temp Onboard: {} Celcius".format(tempOnboard))
    print("Humidity: {}%".format(humidity))
    #print("Current onboard sensor temperature = %d Celsius" % aReceiveBuf[ON_BOARD_TEMP_REG])
    #print("Current onboard sensor humidity = %d %%" % aReceiveBuf[ON_BOARD_HUMIDITY_REG])

    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        print("Onboard temperature and humidity sensor data may not be up to date!")

    if aReceiveBuf[BMP280_STATUS] == 0 :
        barometerTemp = aReceiveBuf[BMP280_TEMP_REG]
        print("Barometer Temp: {}".format(barometerTemp))
        #print("Current barometer temperature = %d Celsius" % aReceiveBuf[BMP280_TEMP_REG])
        barometerPressure = aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 |  aReceiveBuf[BMP280_PRESSURE_REG_H] << 16
        print("Barometric Pressure: {} mBarr".format(barometerPressure/100))
        #print("Current barometer pressure = %d pascal" % (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
    else :
        print("Onboard barometer works abnormally!")

    if aReceiveBuf[HUMAN_DETECT] == 1 :
        infraredMotionDetected=True
        #print("Live body detected within 5 seconds!")
    else:
        infraredMotionDetected=False
        #print("No humans detected!")
    print("MotionDetected: {}".format(infraredMotionDetected))
    jStr='{}"TempExternal":{}, "TempOnboard":{}, "Brightness":{}, "Humidity":{}, "BaroTemp":{}, "BaroPressure":{}, "MotionDetected":"{}"{}'.format(
        "{", externalTemp, tempOnboard, brightnessVal, humidity, barometerTemp, barometerPressure/100, infraredMotionDetected,"}")
    #print(jStr)
    returnVal = json.loads(jStr)
    return returnVal

if __name__ == '__main__':
    retVal = piReadSensorHuhData()
    json.dump('data.json')
    r = requests.post('http://jattie.pythonanywhere.com/pisense', data = retVal)
    print(retVal, r)