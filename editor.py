from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QMainWindow 
from ui import Ui_MainWindow
from PIL import Image,ImageFilter,ImageEnhance
import os

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.workdir=''
        self.photo=None
        self.dilename=None
        self.save_dir="canged"
        self.ui.btn_dir.clicked.connect(self.open)
        self.ui.listWidget.itemClicked.connect(self.showchoosenimage)
        self.ui.btn_bw.clicked.connect(self.do_bw)
        self.ui.btn_blur.clicked.connect(self.do_blur)
        self.ui.pushButton_9.clicked.connect(self.do_diagonal)
        self.ui.btn_mirro_2.clicked.connect(self.do_mirror2)
        self.ui.btn_left.clicked.connect(self.do_left)
        self.ui.btn_right.clicked.connect(self.do_right)
        self.ui.btn_mirror_1.clicked.connect(self.do_mirror)
        self.ui.btn_contrast.clicked.connect(self.do_contrast)

    def loadimage(self,filename):
        self.filename=filename
        path=os.path.join(self.workdir,self.filename)
        try:
            self.photo=Image.open(path)
        except:
            win=QtWidgets.QMessageBox()
            win.setText("Не вдалось відкрити зображення")
            win.exec()

    def showimage(self,path):
        self.ui.image.hide()
        pix=QtGui.QPixmap(path)
        w,h=self.ui.image.width(),self.ui.image.height()
        pix=pix.scaled(w,h,QtCore.Qt.KeepAspectRatio)
        self.ui.image.setPixmap(pix)
        self.ui.image.show()

    def showchoosenimage(self):
        if self.ui.listWidget.selectedItems():
            filename=self.ui.listWidget.selectedItems()[0].text()
            self.loadimage(filename)
            path=os.path.join(self.workdir,self.filename)
            self.showimage(path)

    def do_bw(self):
        self.photo=self.photo.convert('L')
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    def do_blur(self):
        self.photo=self.photo.filter(ImageFilter.BLUR)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    def do_contrast(self):
        self.photo=ImageEnhance.Contrast(self.photo).enhance(1.5)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    def do_left(self):
        self.photo=self.photo.transpose(Image.ROTATE_90)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    def do_right(self):
        self.photo=self.photo.transpose(Image.ROTATE_270)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    def do_mirror(self):
        self.photo=self.photo.transpose(Image.FLIP_LEFT_RIGHT)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    def do_diagonal(self):
        self.photo=self.photo.rotate(45)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)
  
    def do_mirror2(self):
        self.photo=self.photo.transpose(Image.FLIP_TOP_BOTTOM)
        image_path=os.path.join(self.workdir,self.save_dir,self.filename)
        self.saveimage()
        self.showimage(image_path)

    
    def saveimage(self):
        path=os.path.join(self.workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        new_path=os.path.join(path,self.filename)
        self.photo.save(new_path)
    def open(self):
        try:
            self.workdir=QtWidgets.QFileDialog.getExistingDirectory()
            files=os.listdir(self.workdir)
            files_new=self.sort_files(files)
            self.ui.listWidget.clear()
            for file in files_new:
                self.ui.listWidget.addItem(file)
        except:
            alert=QtWidgets.QMessageBox()
            alert.setText("Шлях до папки не вибрано!")
            alert.exec()

    def sort_files(self,files):
        extensions=['.jpg','.png','.svg','.jpeg']
        result=[]
        for file in files:
            for ex in extensions:
                if file.endswith(ex):
                    result.append(file)
        return result


app=QtWidgets.QApplication([])
ex=ImageEditor()
ex.show()
app.exec()
