from gdrive import Drive
from time import sleep
import datetime
from picamera import PiCamera
from os import remove
class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280,720)
        
    
    def take_picture(self) -> str:
        """
        take picture, save ke raspi, trus return nama filenya dan pathnya (misal 'D:/halo/kemas.jpg')
        """
        file_name = "/home/pi/Tes/"+ str(datetime.datetime.now().strftime("%H-%M-%S-%f")) + ".png"
        self.camera.capture(file_name)
        return file_name
        


def main():
    drive_service = Drive() 
    drive_service.make_folder()
    camera = Camera()
    while 1:
        try:
            filename = camera.take_picture() 
            try:
                print(f'Uploading {filename}')
                drive_service.upload(filename)
                print('Done')
                remove(filename)
            except :
                pass
        except KeyboardInterrupt:
            break
    camera.camera.close()

main()
