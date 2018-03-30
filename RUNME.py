from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
exec(open('Definiciones.py').read())

class Preparado:
    def __init__(self, masa, planilla, tiempos, tipos, limites):
        self.existe = True;
        self.masa = masa;
        self.planilla = planilla;
        self.tiempos = tiempos;
        self.tipos = tipos;
        self.limites = limites;

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('web.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        veriFile = QAction(QIcon('web2.png'), 'Verify', self)
        veriFile.setShortcut('Ctrl+V')
        veriFile.setStatusTip('Verificar que haya un elemento')
        veriFile.triggered.connect(self.hay_algo)

        geneFile = QAction(QIcon('web3.png'), 'Generar', self)
        geneFile.setShortcut('Ctrl+G')
        geneFile.setStatusTip('Generar un elemento')
        geneFile.triggered.connect(self.generar_objeto)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(veriFile)
        fileMenu.addAction(geneFile)
        
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
            #Prep = Preparado(ma, sh, ctm, cty, cl)
            #al, ae, ad, xmi, xma, ymi, yma = hacer_graficas(sh, ctm, cty, cl)
            #dibujar_eficiencias(ae,ad)
            #dibujar_capacidades(al, xmi, xma, ymi, yma)

    def hay_algo(self):
        try:
            self.textEdit.setText(float(Prep.ma))
        except:
            self.textEdit.setText('Nohay')

    def generar_objeto(self):
        Prep = Preparado(0,0,0,0,0)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
