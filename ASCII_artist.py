import PIL.Image
import os
import sys

from PIL import ImageFont
from PIL import ImageDraw
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap,QFont
import PyQt5.QtCore

global new_width
global image_path
global text_to_image_text
global width_s
global height_s


new_width = 0
image_path = ''
text_to_image_text = ''
width_s = 0
height_s = 0





#saving format İmage
def ascii_to_jpeg():
    global text_to_image_text
    global width_s
    global height_s

    with open('ascii_image.txt','r') as a:
        ascii_styled = a.read()

    if a == '':
        QtWidgets.QMessageBox.warning(window,'warn','I dont find a any charachter in your ascii_image.txt file ')
    else:
        img = PIL.Image.open("data/background/white.png")
        img_2 = img.resize((width_s * 20, height_s * 16))

        draw = ImageDraw.Draw(img_2)
        # True type font gireceksin buraya, internetten indir istediğini.
        font = ImageFont.truetype("data/font/timesbd.ttf", size=20)
        # draw.text((x, y),"Metin",(r,g,b))
        draw.text((0, 0), ascii_styled, (0, 0, 0), font=font)
        img_2.save('Output.jpg')
        os.startfile('Output.jpg')


# ascii characters used to build the output text "-","S","-", ["B","S","#","&","@","$","%","*","!",":","."]
ASCII_CHARS = ["@", "#", "%","S", "?", "*", "+", ";", ":", ",", "."]



# resize image according to a new width
def resize_image(image):
    global new_width
    global width_s,height_s
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    width_s = int(new_width)
    height_s= new_height
    print(resized_image.size)
    return (resized_image)


# convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    return (grayscale_image)


# convert pixels to a string of ascii characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return (characters)


def main(image_road):
    global new_width,text_to_image_text
    # attempt to open image from user-input
    path = image_road
    #try:
    image = PIL.Image.open(path)
    #except:
        #print(path, " is not a valid pathname to an image.")
        #return

    # convert image to ascii
    new_image_data = pixels_to_ascii(grayify(resize_image(image)))

    # format
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, pixel_count, new_width)])

    # save result to "ascii_image.txt"
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)

    return ascii_image

# run program main()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        global new_width
        super(Ui, self).__init__()
        uic.loadUi('data/UI/Main.ui', self)
        self.show()

        #Logom = PIL.Image.open('data/UI/Logo.png')
        #Logom.resize((121,121))
        #Logom.save('Logo_s.png')

        Your_image_width  = 231
        Your_image_height = 171



        #QtWidgets.QLabel.setPixmap(self,QPixmap('data/UI/Logo.png'))
        self.Logo.setPixmap(QPixmap('data/UI/Logo_s.png'))

        #Button activite
        self.import_image.clicked.connect(self.Import_Image)
        self.Convert_image.clicked.connect(self.Convert_Image)
        self.Saveasimg.clicked.connect(self.Save_png)

    def Import_Image(self):
        global image_path

        İmage_File = QtWidgets.QFileDialog.getOpenFileName(self,'Choose File For Converting',os.getcwd(),'Image files (*.jpg *.png)')

        #if file is file check
        if str(İmage_File) == "('', '')":
            #print(İmage_File)
            QtWidgets.QMessageBox.warning(self,'Warn','You ar not choose a image file \n\n File path is not exist \n Because you aren\'t choise any path road')
        else:
            #print(İmage_File)
            image_path = str(İmage_File).replace("', 'Image files (*.jpg *.png)')",'').replace("('",'',1)
            #print(image_path)

            if os.path.isfile(image_path):
                review_ed = QPixmap(image_path)
                rew_res = review_ed.scaled(231,171,PyQt5.QtCore.Qt.KeepAspectRatio)
                rew_res.save('Thumbnail.png')
                self.Your_image.setPixmap(QPixmap('Thumbnail.png'))
            else:
                QtWidgets.QMessageBox.warning(self,'Warn','You ar not choose a image file \n\n File path is not exist \n{}'.format(image_path))


    def Convert_Image(self):
        global image_path
        global new_width

        new_width = int(self.width_new.text())
        if image_path == '':
            QtWidgets.QMessageBox.warning(self,'Warn','You ar not choose a image file \n\n File path is not exist \n Because you aren\'t choise any path road')
        else:
            self.ascii_output.setPlainText(main(image_path))
        #print(image_path)
    def Save_png(self):
        ascii_to_jpeg()
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
