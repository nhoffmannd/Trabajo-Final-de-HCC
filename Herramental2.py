from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
exec(open('Definiciones.py').read())

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        
        self.initUI()
        
        
    def initUI(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()
        
        
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\EQTEST')
        if fname[0]:
            f = (fname[0])
            f = abrir_archivo(fname[0])
            ma = buscar_masa_MA(f)
            hj = generar_hoja(f)
            sh, ctm, cty, cl = separar_ciclos(hj, ma)
            al, ae, ad, xmi, xma, ymi, yma = hacer_graficas(sh, ctm, cty, cl)
            dibujar_eficiencias(ae,ad)
            dibujar_capacidades(al, xmi, xma, ymi, yma)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
