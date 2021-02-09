from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from camera import Camera
import os
from glonass import Glonass
from copypaste import copy
from datetime import datetime


class tech_control_gui:
    def __init__(self, top):
        self.root = top
        # self.root.bind("<Configure>", self.resize)
        self.camera = Camera()
        self.glonass = Glonass()
        top.geometry("800x480")
        top.resizable(0, 0)
        top.title('ФОТОФИКСАЦИЯ "ПМ-1"')
        top.configure(background="#FFFFFF")
        top.configure(highlightcolor="white")
        font = ('Roboto', 10)
        fg = '#7C7C7C'
        self.AppStyle = ttk.Style()
        self.AppStyle.configure('MakePic.TButton', background="#ff2525")

        self.PictureTime = ''
        self.PictureDate = ''
        self.PictureGPSLatitude = ''
        self.PictureGPSLongitude = ''
        self.PictureFileName = 'image.jpg'

        self.CameraImageFile = ImageTk.PhotoImage(Image.open("images/camera.png").resize((14, 14), Image.ANTIALIAS))
        self.GPSPointImageFile = ImageTk.PhotoImage(
            Image.open("images/gps_point.png").resize((14, 14), Image.ANTIALIAS))
        self.SaveFileImageFile = ImageTk.PhotoImage(
            Image.open("images/save_file.png").resize((14, 14), Image.ANTIALIAS))
        self.MakePicImageFile = ImageTk.PhotoImage(
            Image.open("images/redbutton.png").resize((270, 78), Image.ANTIALIAS))
        self.CopyImageFile = ImageTk.PhotoImage(
            Image.open("images/copybutton.png").resize((270, 66), Image.ANTIALIAS))
        self.CameraDisabledStateImageFile = ImageTk.PhotoImage(
            Image.open("images/red_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.CameraUpdateStateImageFile = ImageTk.PhotoImage(
            Image.open("images/orange_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.CameraEnabledStateImageFile = ImageTk.PhotoImage(
            Image.open("images/green_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteRedImageFile = ImageTk.PhotoImage(
            Image.open("images/red_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteOrangeImageFile = ImageTk.PhotoImage(
            Image.open("images/orange_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteYellowImageFile = ImageTk.PhotoImage(
            Image.open("images/yellow_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteGreenImageFile = ImageTk.PhotoImage(
            Image.open("images/green_circle.jpeg").resize((11, 11), Image.ANTIALIAS))
        self.camera_image = None
        self.file_path = ''
        self.ListOfCameras = ['Выберите камеру...']
        self.ListOfGPSModules = ['Выберите устройство GLONASS...']

        self.CameraFrame = Frame(top,
                                 background="#FFFFFF")
        self.CameraFrame.place(relx=.0,
                               rely=.0,
                               relheight=1,
                               relwidth=.66)

        self.ToolsFrame = Frame(top,
                                background="#FFFFFF")
        self.ToolsFrame.place(relx=.66,
                              rely=.0,
                              relheight=1,
                              relwidth=.33)

        self.CameraResult = Label(self.CameraFrame,
                                  background="#252525",
                                  relief=GROOVE,
                                  borderwidth="0")
        self.CameraResult.place(relx=.01,
                                rely=.01,
                                relheight=.98,
                                relwidth=.98)
        self.width = self.CameraResult.winfo_width()
        self.height = self.CameraResult.winfo_height()

        self.VideoImage = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                image=self.CameraImageFile)
        self.VideoImage.place(relx=.01,
                              rely=.015,
                              relheight=.03,
                              relwidth=.1)

        self.CameraType = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                width=10,
                                anchor='w',
                                fg=fg,
                                text="USB Камера",
                                font=font)
        self.CameraType.place(relx=.12,
                              rely=.01,
                              relheight=.04,
                              relwidth=.4)

        self.VideoImage = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                font=font,
                                image=self.CameraDisabledStateImageFile)
        self.VideoImage.place(relx=.9,
                              rely=.01,
                              relheight=.03,
                              relwidth=.1)
        self.combo_style = ttk.Style()
        self.combo_style.configure('TCombobox', foreground=fg)
        self.ListOfAvailableCameras = ttk.Combobox(self.ToolsFrame,
                                                   background="#FFFFFF",
                                                   font=font,
                                                   values=self.ListOfCameras,
                                                   state="readonly",
                                                   style="TCombobox")
        self.ListOfAvailableCameras.bind('<Button-1>', self.camera_list_update)
        self.ListOfAvailableCameras.current(0)
        self.ListOfAvailableCameras.place(relx=.01,
                                          rely=.05,
                                          relheight=.06,
                                          relwidth=.98)

        self.GPSPointImage = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   image=self.GPSPointImageFile)
        self.GPSPointImage.place(relx=.01,
                                 rely=.14,
                                 relheight=.03,
                                 relwidth=.1)

        self.GPSModuleType = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   width=10,
                                   anchor='w',
                                   font=font,
                                   fg=fg,
                                   text="GLONASS Модуль")
        self.GPSModuleType.place(relx=.12,
                                 rely=.14,
                                 relheight=.03,
                                 relwidth=.5)

        self.GPSPointImage = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   image=self.GPSSatelliteRedImageFile)
        self.GPSPointImage.place(relx=.9,
                                 rely=.14,
                                 relheight=.03,
                                 relwidth=.1)

        self.ListOfAvailableGPSModules = ttk.Combobox(self.ToolsFrame,
                                                      background="#FFFFFF",
                                                      font=font,
                                                      values=self.ListOfGPSModules,
                                                      style="TCombobox",
                                                      state="readonly")
        self.ListOfAvailableGPSModules.bind('<Button-1>', self.glonass_device_update)
        self.ListOfAvailableGPSModules.bind('<<ComboboxSelected>>', self.open_glonass)
        self.ListOfAvailableGPSModules.current(0)
        self.ListOfAvailableGPSModules.place(relx=.01,
                                             rely=.18,
                                             relheight=.06,
                                             relwidth=.98)

        self.SaveFileImage = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   image=self.SaveFileImageFile)
        self.SaveFileImage.place(relx=.01,
                                 rely=.27,
                                 relheight=.03,
                                 relwidth=.1)

        self.SaveFilePathLabel = Label(self.ToolsFrame,
                                       background="#FFFFFF",
                                       width=10,
                                       anchor='w',
                                       fg=fg,
                                       font=font,
                                       text="Директория")
        self.SaveFilePathLabel.place(relx=.12,
                                     rely=.27,
                                     relheight=.03,
                                     relwidth=.3)

        self.SaveFilePathLabel = Entry(self.ToolsFrame,
                                       font=font,
                                       background="#FFFFFF")
        self.SaveFilePathLabel.insert(0, self.file_path)
        self.SaveFilePathLabel.place(relx=.01,
                                     rely=.31,
                                     relheight=.05,
                                     relwidth=.58)
        self.SaveFilePathButton = Button(self.ToolsFrame,
                                         text="Выбрать",
                                         fg=fg,
                                         font=font,
                                         command=self.open_file_dialog)
        self.SaveFilePathButton.place(relx=.60,
                                      rely=.31,
                                      relheight=.05,
                                      relwidth=.38)

        self.GPSTimeLabel = Label(self.ToolsFrame,
                                  width=10,
                                  anchor='w',
                                  font=font,
                                  background="#FFFFFF",
                                  fg=fg,
                                  text="Время")
        self.GPSTimeLabel.place(relx=.01,
                                rely=.40,
                                relheight=.03,
                                relwidth=.3)

        self.time_of_gps = BooleanVar()
        self.time_of_gps.set(0)
        self.LocalTime = Checkbutton(self.ToolsFrame,
                                     text='GPS',
                                     font=font,
                                     fg=fg,
                                     variable=self.time_of_gps,
                                     onvalue=1, offvalue=0)
        self.LocalTime.place(relx=.25,
                             rely=.40,
                             relheight=.03,
                             relwidth=.2)

        self.GPSTime = Label(self.ToolsFrame,
                             width=10,
                             anchor='e',
                             font=font,
                             background="#FFFFFF",
                             fg=fg,
                             text=datetime.now().strftime("%H:%M:%S"))
        self.GPSTime.place(relx=.61,
                           rely=.40,
                           relheight=.03,
                           relwidth=.37)

        self.GPSDateLabel = Label(self.ToolsFrame,
                                  width=10,
                                  anchor='w',
                                  font=font,
                                  background="#FFFFFF",
                                  fg=fg,
                                  text="Дата")
        self.GPSDateLabel.place(relx=.01,
                                rely=.45,
                                relheight=.03,
                                relwidth=.3)
        self.GPSDate = Label(self.ToolsFrame,
                             width=10,
                             anchor='e',
                             font=font,
                             background="#FFFFFF",
                             fg=fg,
                             text=datetime.now().strftime("%d.%m.%Y"))
        self.GPSDate.place(relx=.41,
                           rely=.45,
                           relheight=.03,
                           relwidth=.57)

        self.GPSLatitudeLabel = Label(self.ToolsFrame,
                                      width=10,
                                      anchor='w',
                                      font=font,
                                      background="#FFFFFF",
                                      fg=fg,
                                      text="Широта")
        self.GPSLatitudeLabel.place(relx=.01,
                                    rely=.5,
                                    relheight=.03,
                                    relwidth=.3)

        self.GPSLatitude = Label(self.ToolsFrame,
                                 width=10,
                                 anchor='e',
                                 font=font,
                                 background="#FFFFFF",
                                 fg=fg,
                                 text='0')
        self.GPSLatitude.place(relx=.41,
                               rely=.5,
                               relheight=.03,
                               relwidth=.57)

        self.GPSLongitudeLabel = Label(self.ToolsFrame,
                                       width=10,
                                       anchor='w',
                                       font=font,
                                       background="#FFFFFF",
                                       fg=fg,
                                       text="Долгота")
        self.GPSLongitudeLabel.place(relx=.01,
                                     rely=.55,
                                     relheight=.03,
                                     relwidth=.3)

        self.GPSLongitude = Label(self.ToolsFrame,
                                  width=10,
                                  anchor='e',
                                  font=font,
                                  fg=fg,
                                  background="#FFFFFF",
                                  text='0')
        self.GPSLongitude.place(relx=.41,
                                rely=.55,
                                relheight=.03,
                                relwidth=.57)

        self.CopyButton = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                image=self.CopyImageFile)
        self.CopyButton.place(relx=.01,
                              rely=.62,
                              relheight=.15,
                              relwidth=.98)

        self.MakePicButton = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   compound="left",
                                   image=self.MakePicImageFile)
        # command=self.capture)
        self.MakePicButton.place(relx=.01,
                                 rely=.78,
                                 relheight=.2,
                                 relwidth=.98)

        self.glonass_device_update()
        self.video_stream()

    def get_file_path(self):
        self.file_path = self.SaveFilePathLabel.get()
        return self.file_path

    def capture(self):
        if self.camera.cam is not None:
            self.width = self.CameraResult.winfo_width()
            self.height = self.CameraResult.winfo_height()
            self.camera.set_camera(int(str(self.ListOfAvailableCameras.get()).split(' - ')[1]) - 1)
            self.camera.make_a_capture(self.get_file_path(), self.PictureFileName)
            image = Image.open(os.path.join(self.get_file_path(), self.PictureFileName))
            w, h = image.size
            self.height = int(self.height * (self.height / h))
            image = image.resize((self.width, self.height), Image.ANTIALIAS)
            self.camera_image = ImageTk.PhotoImage(image)
            self.CameraResult.configure(image=self.camera_image)

            self.GPSLongitude.config(text=self.glonass.longitude_text)
            self.GPSLatitude.config(text=self.glonass.latitude_text)
            self.PictureGPSLongitude = self.glonass.longitude_text
            self.PictureGPSLatitude = self.glonass.latitude_text

            if self.time_of_gps.get():
                self.GPSTime.config(text=self.glonass.GPS_TIME)
                self.GPSDate.config(text=self.glonass.GPS_DATE)
                self.PictureDate = self.glonass.GPS_DATE
                self.PictureTime = self.glonass.GPS_TIME
            else:
                self.glonass.GPS_TIME = datetime.now().strftime("%H:%M:%S")
                self.GPSTime.config(text=datetime.now().strftime("%H:%M:%S"))
                self.GPSDate.config(text=datetime.now().strftime("%d.%m.%Y"))
                self.PictureDate = datetime.now().strftime("%d.%m.%Y")
                self.PictureTime = datetime.now().strftime("%H:%M:%S")

            self.glonass.set_coordinates(os.path.join(self.file_path, self.PictureFileName))

    def camera_list_update(self, *args):
        self.VideoImage.configure(image=self.CameraUpdateStateImageFile)
        self.VideoImage.update()
        self.width = self.CameraResult.winfo_width()
        self.height = self.CameraResult.winfo_height()
        self.ListOfCameras = self.camera.get_list_of_available_cameras()
        for i in range(len(self.ListOfCameras)):
            self.ListOfCameras[i] = 'USB Камера - ' + str(self.ListOfCameras[i] + 1)
            self.VideoImage.configure(image=self.CameraEnabledStateImageFile)
        if not self.ListOfCameras:
            self.ListOfCameras = ['Выберите камеру']
            self.VideoImage.configure(image=self.CameraDisabledStateImageFile)
        self.ListOfAvailableCameras.configure(values=self.ListOfCameras)

    def glonass_device_update(self, *args):
        self.ListOfGPSModules = self.glonass.check_device()
        # print(self.ListOfGPSModules)
        if not self.ListOfGPSModules:
            self.ListOfGPSModules = ['Выберите устройство GLONASS']
            self.GPSPointImage.configure(image=self.GPSSatelliteRedImageFile)
        else:
            self.GPSPointImage.configure(image=self.GPSSatelliteOrangeImageFile)
        self.ListOfAvailableGPSModules.configure(values=self.ListOfGPSModules)

    def run(self):
        self.root.mainloop()

    def video_stream(self, *args):
        self.width = self.CameraResult.winfo_width()
        self.height = self.CameraResult.winfo_height()
        if self.camera.cam is not None:
            try:
                image = self.camera.video_stream()
                w, h = image.size
                self.height = int(self.height * (self.height / h))
                image = image.resize((self.width, self.height), Image.ANTIALIAS)
                ImgTk = ImageTk.PhotoImage(image=image)
                self.CameraResult.ImgTk = ImgTk
                self.CameraResult.configure(image=ImgTk)
                self.CameraResult.after(1, self.video_stream)
            except:
                pass
        else:
            try:
                self.camera.set_camera(int(str(self.ListOfAvailableCameras.get()).split(' - ')[1]) - 1)
            except:
                pass
            finally:
                self.CameraResult.after(1, self.video_stream)

    def resize(self, event):
        try:
            self.CameraResult.after(3, self.video_stream)
        except:
            pass

    def open_file_dialog(self):
        self.file_path = filedialog.askdirectory()
        self.SaveFilePathLabel.insert(0, self.file_path)

    def copy_data(self):
        data = 'Время - {0}\r\nДата - {1}\r\nШирота - {2}\r\nДолгота - {3}'.format(self.PictureTime,
                                                                                   self.PictureDate,
                                                                                   self.PictureGPSLatitude,
                                                                                   self.PictureGPSLongitude)
        copy(data)

    def open_glonass(self, *args):
        # print(self.ListOfAvailableGPSModules.get())
        self.glonass.open_glonass(str(self.ListOfAvailableGPSModules.get()).split(' - ')[1])
        self.start_glonass_monitor()

    def start_glonass_monitor(self, *args):
        self.glonass.parse_glonass_data()
        self.ListOfAvailableGPSModules.after(2000, self.start_glonass_monitor)


a = tech_control_gui(Tk())
a.run()
