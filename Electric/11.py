#-*- coding:utf-8 -*-
import sys
from PyQt4.QtGui import QWidget,QPushButton,QApplication,\
    QMessageBox,QHBoxLayout,QVBoxLayout

class mywidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setGeometry(300,300,1000,1000)
        self.setWindowTitle('hello，pyqt4!')
        self.setToolTip('这是qt4程序')

        btok = QPushButton('ok',self)
        btcancel = QPushButton('cancel',self)
        btok.clicked.connect(self.close)
        
        hb = QHBoxLayout()
        hb.addStretch(1)
        hb.addWidget(btok)
        hb.addSpacing(20)
        hb.addWidget(btcancel)
        hb.addStretch(1)

        vb = QVBoxLayout()
        vb.addStretch(1)
        vb.addLayout(hb)
        vb.addSpacing(20)

        self.setLayout(vb)

    def closeEvent(self,event):
        quit = QMessageBox.question(self,'信息','是否退出',\
        QMessageBox.Yes|QMessageBox.No)
        if quit == QMessageBox.Yes:
            event.accept()
        else:event.ignore()

app = QApplication(sys.argv)
wg = mywidget()
wg.show()
sys.exit(app.exec_())