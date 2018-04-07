from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
exec(open('Definiciones.py').read())

class Preparado:
    def __init__(self, masa, planilla, tiempos, tipos, limites):
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

        self.skip = False

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('web.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        effiFile = QAction(QIcon('web2.png'), 'Eficiencias', self)
        effiFile.setShortcut('Ctrl+E')
        effiFile.setStatusTip('Mostrar Eficiencias')
        effiFile.triggered.connect(self.mostrar_eficiencias)

        ciclFile = QAction(QIcon('web3.png'), 'Ciclados', self)
        ciclFile.setShortcut('Ctrl+C')
        ciclFile.setStatusTip('Mostrar Ciclados')
        ciclFile.triggered.connect(self.mostrar_ciclados)

        exitFile = QAction(QIcon('web5.png'), 'Salir', self)
        exitFile.setShortcut('Ctrl+Q')
        exitFile.setStatusTip('Irse')
        exitFile.triggered.connect(self.cerrar_programa)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(effiFile)
        fileMenu.addAction(ciclFile)
        fileMenu.addAction(exitFile)
        
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
            self.Prep = Preparado(0.0,0.0,0.0,0.0,0.0)
            sh, ctm, cty, cl = separar_ciclos(hj, ma)
            
            self.Prep.masa = ma
            self.Prep.planilla = sh
            self.Prep.tiempos = ctm
            self.Prep.tipos = cty
            self.Prep.limites = cl
            
    def hay_algo(self):
        try:
            self.textEdit.setText(str(self.Prep.masa) + ", hay algo aquí.")
        except:
            self.textEdit.setText('No se ha seleccionado una grilla.')

    def generar_objeto(self):
        self.Prep = Preparado(0.0,0.0,0.0,0.0,0.0)

    def mostrar_eficiencias(self):
        self.skip = False
        try:
            sh = self.Prep.planilla
        except:
            self.textEdit.setText('No se ha podido leer la tabla de datos.')
            self.skip = True
        if self.skip == False:
            try:
                ctm = self.Prep.tiempos
            except:
                self.textEdit.setText('No se han podido leer los tiempos.')
                self.skip = True
        if self.skip == False:
            try:
                cty = self.Prep.tipos
            except:
                self.textEdit.setText('No se han podido leer los tipos de ciclo.')
                self.skip = True
        if self.skip == False:
            try:
                cl = self.Prep.limites
            except:
                self.textEdit.setText('No se han podido leer los límites.')
                self.skip = True
        if self.skip == False:
            try:
                al, ae, ad, xmi, xma, ymi, yma = hacer_graficas(sh, ctm, cty, cl)
                print('sh')
                print(sh)
                print ('ctm')
                print (ctm)
                print('cty')
                print(cty)
                print('cl')
                print(cl)
            except:
                self.textEdit.setText('No se ha podido hacer el gráfico.')
                self.skip = True
                print('sh')
                print(sh)
                print ('ctm')
                print (ctm)
                print('cty')
                print(cty)
                print('cl')
                print(cl)
        if self.skip == False:
            try:
                dibujar_eficiencias(ae,ad)
            except:
                self.textEdit.setText('No se pudieron dibujar los graficos.')

    def mostrar_ciclados(self):
        try:
            sh = self.Prep.planilla
            ctm = self.Prep.tiempos
            cty = self.Prep.tipos
            cl = self.Prep.limites
            al, xmi, xma, ymi, yma = hacer_graficas_ciclos(sh, ctm, cl)
            dibujar_capacidades(al, xmi, xma, ymi, yma)
        except:
            self.textEdit.setText('Debes elegir una planilla primero.')

    def cerrar_programa(self):
        sys.exit()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
