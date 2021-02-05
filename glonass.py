# https://gitlab.com/TNThieding/exif

from exif import Image
import pyubx2
from serial import Serial
import serial.tools.list_ports
from time import sleep


GPS_ALTITUDE = 3  # Height
GPS_ALTITUDE_REF = 'GpsAltitudeRef.ABOVE_SEA_LEVEL'  # or ABOVE_GROUND_LEVEL
GPS_LATITUDE = (55.0, 28.0, 29.9)  # D, M, S
GPS_LATITUDE_REF = 'N'
GPS_LONGITUDE = (54.00, 53.0, 16.8)  # D, M, S
GPS_LONGITUDE_REF = 'E'

# config = [181, 98, 6, 62, 20, 0, 0, 0, 32, 2, 0, 8, 16, 0, 1, 0, 1, 1, 6, 8, 14, 0, 1, 0, 1, 1, 180, 118]
# print(config)
# data = Serial('/dev/tty.usbmodem14101', '9600')
# sleep(1)
# for i in config:
#     print(chr(i).encode('utf-8'))
#     data.write(chr(i).encode('utf-8'))
# while 1:
#     print(data.read(data.inWaiting()))
#     sleep(1.1)

def set_coordinates(file):
    f = open(file, 'rb')

    img = Image(f)
    meta = dir(img)

    img.set('gps_latitude', GPS_LATITUDE)
    img.set('gps_longitude', GPS_LONGITUDE)
    img.set('gps_altitude', GPS_ALTITUDE)

    for i in meta:
        print(i, img.get(i))

    new_f = open(file, 'wb')
    new_f.write(img.get_file())
    new_f.close()


def check_device():
    list_of_ports = serial.tools.list_ports.comports()
    glonass_ports = []
    for i in list_of_ports:
        port, name, dev_type = i
        if 'GNSS' in name:
            port = str(port)
            if '/cu.' in port:
                port = port.replace('/cu.', '/tty.')
            glonass_ports.append('USB-GLONASS - ' + port)
    return glonass_ports

