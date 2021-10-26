from gdrive import Drive
from time import sleep
def take_picture() -> str:
    """
    take picture, save ke raspi, trus return nama filenya dan pathnya (misal 'D:/halo/kemas.jpg')
    """
    filename = ""
    raise NotImplementedError
    return filename

def main():
    #silahkan tambah fungsi setup kameranya disini
    drive_service = Drive() 
    drive_service.make_folder()
    while 1:
        filename = take_picture()
        drive_service.upload(filename)
        sleep(10) #masukan interval pengambilan foto disini


