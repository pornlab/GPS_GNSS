# https://gitlab.com/TNThieding/exif

from exif import Image
from serial import Serial
import serial.tools.list_ports


class Glonass:
    def __init__(self):
        self.GPS_LATITUDE = (0.0, 0.0, 0.0)  # D, M, S
        self.GPS_LATITUDE_REF = 'N'
        self.latitude_text = ''
        self.GPS_LONGITUDE = (0.0, 0.0, 0.0)  # D, M, S
        self.GPS_LONGITUDE_REF = 'E'
        self.longitude_text = ''
        self.GPS_DATE = ''
        self.GPS_TIME = ''
        self.GPS_SATELLITES = 0
        self.GLONASS_PORT = Serial()  # None
        self.port = ''

    def set_coordinates(self, file):
        #print(1234)
        f = open(file, 'rb')
        img = Image(f)
        meta = dir(img)
        img.set('gps_latitude', self.GPS_LATITUDE)
        img.set('gps_longitude', self.GPS_LONGITUDE)
        #img.set('gps_altitude', self.GPS_ALTITUDE)
        file = self.GPS_DATE + ' ' + self.GPS_TIME + ' ' + self.latitude_text + ' с.ш. ' + self.longitude_text + ' ю.д..jpg'

        new_f = open(file, 'wb')
        new_f.write(img.get_file())
        new_f.close()

    def check_device(self):
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

    def open_glonass(self, port):
        self.port = port
        try:
            self.GLONASS_PORT = Serial(self.port, '115200')
            self.GLONASS_PORT.read(self.GLONASS_PORT.inWaiting())
        except:
            pass

    def parse_glonass_data(self):
        data = self.GLONASS_PORT.read(self.GLONASS_PORT.inWaiting()).decode('ascii')
        data = data.split('$')
        for a in data:
            i = a.split(',')
            if i[0] == 'GPRMC':
                try:
                    self.GPS_TIME = i[1][0] + i[1][1] + ':' \
                                    + i[1][2] + i[1][3] + ':' \
                                    + i[1][4] + i[1][5]
                    self.GPS_DATE = i[9][0] + i[9][1] + '.' \
                                    + i[9][2] + i[9][3] + '.' \
                                    + i[9][4] + i[9][5]
                except:
                    pass

            if i[0] == 'GPGSV':
                try:
                    self.GPS_SATELLITES = i[3]
                except:
                    pass

            if i[0] == 'GPGGA':

                try:
                    lat = str(float(i[2]))
                    lat = lat.split('.')
                    lat[1] = float(lat[0][len(lat[0]) - 2] + lat[0][len(lat[0]) - 1] + '.' + lat[1])
                    lat[0] = float(lat[0][:len(lat[0]) - 2])

                    lon = str(float(i[4]))
                    lon = lon.split('.')
                    lon[1] = float(lon[0][len(lon[0]) - 2] + lon[0][len(lon[0]) - 1] + '.' + lon[1])
                    lon[0] = float(lon[0][:len(lon[0]) - 2])
                    self.GPS_LATITUDE = (lat[0], lat[1], 0.0)
                    self.GPS_LATITUDE_REF = i[3]
                    self.GPS_LONGITUDE = (lon[0], lon[1], 0.0)
                    self.GPS_LONGITUDE_REF = i[5]
                    self.latitude_text = str(int(lat[0])) + '˚ ' + str(lat[1]) + "' " + i[3]
                    self.longitude_text = str(int(lon[0])) + '˚ ' + str(lon[1]) + "' " + i[5]
                except:
                    pass

        #print(self.GPS_TIME, self.GPS_DATE)
        #print('SATELLITES = ', self.GPS_SATELLITES)
        #print("LATITUDE = ", self.GPS_LATITUDE, self.GPS_LATITUDE_REF)
        #print("LONGITUDE = ", self.GPS_LONGITUDE, self.GPS_LONGITUDE_REF)
