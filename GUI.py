from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from camera import Camera
import os
from time import sleep
import threading
import glonass


class tech_control_gui:
    def __init__(self, top):
        self.root = top
        self.camera = Camera()
        top.geometry("800x480")
        top.title("Фотофиксация ТО-1")
        top.configure(background="#FFFFFF")
        top.configure(highlightcolor="white")
        fontExample = ("Roboto", 14)

        self.CameraImageFile = ImageTk.PhotoImage(Image.open("images/camera.png").resize((15, 12), Image.ANTIALIAS))
        self.GPSPointImageFile = ImageTk.PhotoImage(
            Image.open("images/gps_point.png").resize((10, 14), Image.ANTIALIAS))
        self.SaveFileImageFile = ImageTk.PhotoImage(
            Image.open("images/save_file.png").resize((12, 16), Image.ANTIALIAS))
        self.MakePicImageFile = ImageTk.PhotoImage(Image.open("images/make_pic.png").resize((26, 20), Image.ANTIALIAS))
        self.CameraDisabledStateImageFile = ImageTk.PhotoImage(
            Image.open("images/red_circle.png").resize((11, 11), Image.ANTIALIAS))
        self.CameraEnabledStateImageFile = ImageTk.PhotoImage(
            Image.open("images/green_circle.png").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteRedImageFile = ImageTk.PhotoImage(
            Image.open("images/red_circle.png").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteOrangeImageFile = ImageTk.PhotoImage(
            Image.open("images/orange_circle.png").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteYellowImageFile = ImageTk.PhotoImage(
            Image.open("images/yellow_circle.png").resize((11, 11), Image.ANTIALIAS))
        self.GPSSatelliteGreenImageFile = ImageTk.PhotoImage(
            Image.open("images/green_circle.png").resize((11, 11), Image.ANTIALIAS))
        self.camera_image = None
        self.file_path = ''
        self.ListOfCameras = ['Выберите камеру...']

        self.ListOfGPSModules = ['Устройство GLONASS...']

        self.AppStyle = ttk.Style()
        self.AppStyle.configure('MakePic.TButton', background="#ff2525")

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
                                  borderwidth="3")
        self.CameraResult.place(relx=.01,
                                rely=.01,
                                relheight=.98,
                                relwidth=.98)

        self.VideoImage = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                image=self.CameraImageFile)
        self.VideoImage.place(relx=.01,
                              rely=.01,
                              relheight=.03,
                              relwidth=.1)

        self.CameraType = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                text="USB Камера",
                                font=fontExample)
        self.CameraType.place(relx=.12,
                              rely=.01,
                              relheight=.03,
                              relwidth=.3)

        self.VideoImage = Label(self.ToolsFrame,
                                background="#FFFFFF",
                                image=self.CameraDisabledStateImageFile)
        self.VideoImage.place(relx=.9,
                              rely=.01,
                              relheight=.03,
                              relwidth=.1)

        self.ListOfAvailableCameras = ttk.Combobox(self.ToolsFrame,
                                                   background="#FFFFFF",
                                                   values=self.ListOfCameras,
                                                   style="TCombobox")
        self.ListOfAvailableCameras.bind('<Button-1>', self.camera_list_update)
        self.ListOfAvailableCameras.current(0)
        self.ListOfAvailableCameras.place(relx=.01,
                                          rely=.06,
                                          relheight=.05,
                                          relwidth=.98)

        self.GPSPointImage = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   image=self.GPSPointImageFile)
        self.GPSPointImage.place(relx=.01,
                                 rely=.13,
                                 relheight=.03,
                                 relwidth=.1)

        self.GPSModuleType = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   text="GPS Модуль")
        self.GPSModuleType.place(relx=.12,
                                 rely=.13,
                                 relheight=.03,
                                 relwidth=.3)

        self.GPSPointImage = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   image=self.GPSSatelliteRedImageFile)
        self.GPSPointImage.place(relx=.9,
                                 rely=.13,
                                 relheight=.03,
                                 relwidth=.1)

        self.ListOfAvailableGPSModules = ttk.Combobox(self.ToolsFrame,
                                                      background="#FFFFFF",
                                                      values=self.ListOfGPSModules,
                                                      style="TCombobox",
                                                      font=fontExample)
        self.ListOfAvailableGPSModules.bind('<Button-1>', self.glonass_device_update)
        self.ListOfAvailableGPSModules.current(0)
        self.ListOfAvailableGPSModules.place(relx=.01,
                                             rely=.18,
                                             relheight=.05,
                                             relwidth=.98)

        self.SaveFileImage = Label(self.ToolsFrame,
                                   background="#FFFFFF",
                                   image=self.SaveFileImageFile)
        self.SaveFileImage.place(relx=.01,
                                 rely=.25,
                                 relheight=.03,
                                 relwidth=.1)

        self.SaveFilePathLabel = Label(self.ToolsFrame,
                                       background="#FFFFFF",
                                       text="Директория")
        self.SaveFilePathLabel.place(relx=.12,
                                     rely=.25,
                                     relheight=.03,
                                     relwidth=.3)

        self.SaveFilePathLabel = Entry(self.ToolsFrame,
                                       background="#FFFFFF")
        self.SaveFilePathLabel.insert(0, self.file_path)
        self.SaveFilePathLabel.place(relx=.01,
                                     rely=.30,
                                     relheight=.05,
                                     relwidth=.98)

        self.GPSTimeLabel = Label(self.ToolsFrame,
                                  justify=LEFT,
                                  background="#FFFFFF",
                                  text="Время")
        self.GPSTimeLabel.place(relx=.01,
                                rely=.40,
                                relheight=.03,
                                relwidth=.3)

        self.GPSTime = Label(self.ToolsFrame,
                             justify=RIGHT,
                             background="#FFFFFF",
                             text="11:12:13")
        self.GPSTime.place(relx=.41,
                           rely=.40,
                           relheight=.03,
                           relwidth=.5)

        self.GPSDateLabel = Label(self.ToolsFrame,
                                  justify=LEFT,
                                  background="#FFFFFF",
                                  text="Дата")
        self.GPSDateLabel.place(relx=.01,
                                rely=.45,
                                relheight=.03,
                                relwidth=.3)

        self.GPSDate = Label(self.ToolsFrame,
                             background="#FFFFFF",
                             justify=RIGHT,
                             text="01.01.2021")
        self.GPSDate.place(relx=.41,
                           rely=.45,
                           relheight=.03,
                           relwidth=.5)

        self.GPSLatitudeLabel = Label(self.ToolsFrame,
                                      justify=LEFT,
                                      background="#FFFFFF",
                                      text="Широта")
        self.GPSLatitudeLabel.place(relx=.01,
                                    rely=.5,
                                    relheight=.03,
                                    relwidth=.3)

        self.GPSLatitude = Label(self.ToolsFrame,
                                 justify=RIGHT,
                                 background="#FFFFFF",
                                 text='32.211234')
        self.GPSLatitude.place(relx=.41,
                               rely=.5,
                               relheight=.03,
                               relwidth=.5)

        self.GPSLongitudeLabel = Label(self.ToolsFrame,
                                       justify=LEFT,
                                       background="#FFFFFF",
                                       text="Долгота")
        self.GPSLongitudeLabel.place(relx=.01,
                                     rely=.55,
                                     relheight=.03,
                                     relwidth=.3)

        self.GPSLongitude = Label(self.ToolsFrame,
                                  justify=RIGHT,
                                  background="#FFFFFF",
                                  text='23.345245')
        self.GPSLongitude.place(relx=.41,
                                rely=.55,
                                relheight=.03,
                                relwidth=.5)

        self.CopyButton = ttk.Button(self.ToolsFrame,
                                     text='Скопировать данные')
        self.CopyButton.place(relx=.01,
                              rely=.62,
                              relheight=.15,
                              relwidth=.98)

        self.MakePicButton = ttk.Button(self.ToolsFrame,
                                        text='Сделать Снимок',
                                        style='MakePic.TButton',
                                        compound="left",
                                        image=self.MakePicImageFile,
                                        command=self.capture)
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
        width = self.CameraResult.winfo_width()
        height = self.CameraResult.winfo_height()
        self.camera.set_camera(int(str(self.ListOfAvailableCameras.get()).split(' - ')[1]) - 1)
        self.camera.make_a_capture(self.get_file_path())
        image = Image.open(os.path.join(self.get_file_path(), "image.jpg"))
        w, h = image.size
        height = int(height * (height / h))
        image = image.resize((width, height), Image.ANTIALIAS)
        self.camera_image = ImageTk.PhotoImage(image)
        self.CameraResult.configure(image=self.camera_image)
        # self.CameraResult.update()

    def camera_list_update(self, *args):
        self.ListOfCameras = self.camera.get_list_of_available_cameras()
        for i in range(len(self.ListOfCameras)):
            self.ListOfCameras[i] = 'USB Камера - ' + str(self.ListOfCameras[i] + 1)
            self.VideoImage.configure(image=self.CameraEnabledStateImageFile)
        if not self.ListOfCameras:
            self.ListOfCameras = ['USB Камера не подключена']
            self.VideoImage.configure(image=self.CameraDisabledStateImageFile)
        self.ListOfAvailableCameras.configure(values=self.ListOfCameras)

    def glonass_device_update(self, *args):
        self.ListOfGPSModules = glonass.check_device()
        print(self.ListOfGPSModules)
        if not self.ListOfGPSModules:
            self.ListOfGPSModules = ['Устройство GLONASS...']
            self.GPSPointImage.configure(image=self.GPSSatelliteRedImageFile)
        else:
            self.GPSPointImage.configure(image=self.GPSSatelliteOrangeImageFile)
        self.ListOfAvailableGPSModules.configure(values=self.ListOfGPSModules)

    def run(self):
        self.root.mainloop()

    def video_stream(self, *args):
        if self.camera.cam != None:
            width = self.CameraResult.winfo_width()
            height = self.CameraResult.winfo_height()
            image = self.camera.video_stream()
            w, h = image.size
            height = int(height * (height / h))
            image = image.resize((width, height), Image.ANTIALIAS)
            ImgTk = ImageTk.PhotoImage(image=image)
            self.CameraResult.ImgTk = ImgTk
            self.CameraResult.configure(image=ImgTk)
            self.CameraResult.after(1, self.video_stream)
        else:
            try:
                self.camera.set_camera(int(str(self.ListOfAvailableCameras.get()).split(' - ')[1]) - 1)
            except:
                pass
            finally:
                self.CameraResult.after(1, self.video_stream)



a = tech_control_gui(Tk())
a.run()


# 1 Видео поток
