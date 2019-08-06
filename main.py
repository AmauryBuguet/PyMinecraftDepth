# This Python file uses the following encoding: utf-8

#!/usr/bin/env python


from PyQt5.QtCore import Qt, QTimer
#from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPixmap, QImage, QColor, QTextCursor
from PyQt5.QtWidgets import (QApplication, QGridLayout, QTextEdit, QMainWindow,
    QLabel, QPushButton, QWidget, QTextEdit)
#import test1Scalable #code pour gerer les pins de la raspberry

# les seules valeurs a toucher sont les 5 suivantes :
# période d'affichage (ms)
periode = 200

# taille écran
screenH = 768
screenW = 1366

# valeurs d'affichage
nbBlocsD = 4 # nombre de blocs de distance
nbBlocsH = 4 # nombre de blocs de hauteur

# TESTS HAUTEUR:
# 10 blocs de haut a 10 blocs de distance = ~500 pixels -> 50 pix/blocs
# 5 blocs de haut a 10 blocs de distance = ~300 pixels -> 30 pix/blocs
# 10 blocs de haut a 5 blocs de distance = ~750 pixels -> 150 pix/blocs
# 5 blocs de haut a 5 blocs de distance = ~450 pixels -> 90 pix/blocs

# CONCLUSION:
# nbPix = A*nbBlocsH + B
# avec A = 4(20-nbBlocsD)
# et B = 10(20-nbBlocsD)
# d'ou au final pour calculer l'étendue des pixels à surveiller on a :
# nbPix = 4*nbBlocsH*(20-nbBlocsD) + 10*(20-nbBlocsD)
# avec nbBlocsH (resp. nbBlocsD) le nombre de blocs de hauteur (resp. de distance) que l'on veut afficher

# TESTS COULEUR:
# 10 blocs de distance = valeur du pixel à 60 en inversé -> 6/blocs
# 5 blocs de distance = valeur du pixel à 40 en inversé -> 8/blocs

# CONCLUSION:
# couleur = 4*nbBlocsD+20
# nbBlocsD = (couleur-20)/4

# EXEMPLES:
# pour un affichage 10x10 on va regarder:
#    nbPix = 500 pixels de hauteur sur l'écran
#    couleur de 0 à 60
# pour un affichage 4x3 ( 4 de distance et 3 de hauteur) on va regarder:
#    nbPix = 352 pixels de hauteur sur l'écran
#    couleur de 0 à 36

# après tests il faudrait en fait un nb de pixels adaptable en fonction de la distance
# ou écarter les "prises de pixels" aux extrémités

#nbPixels = 4*nbBlocsH*(20-nbBlocsD) + 10*(20-nbBlocsD)
nbPixels = 500
couleurMax =  4*nbBlocsD+20
couleurMin = 15 # en dessous de cette valeur le bloc est considéré comme étant juste devant

def sendDataToDisplay(motif1,x,y,motifMult=1,frequence=0.5,sleeptime=0.5):
	#print("motifL220",motif1)
	if motifMult==1:
		motifMult=len(motif1)
		#print("MotifMult",motifMult)
	else:
		motifMult=1
	motifF=[[[0 for i in range(x)] for j in range(y)]for z in range(motifMult+1)]
	for z in range(motifMult+1):
		for i in range(x):
			for j in range(y):
				if z<motifMult:
					if motifMult==1:
						motifF[z][i][j]=motif1[i][j]
					else:
						motifF[z][i][j]=motif1[z][i][j]
				else:
					motifF[z][i][j]=0
	#motifF=convertMap(motifF,x,y)
	test1Scalable.convertToHexa(motifF,x,y,frequence,sleeptime)#ici les commentaires pour marcher sans rasberry

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.pixelRow = QLabel()
        self.pixelRow.setFixedSize( 20, nbPixels )

        self.matrixDisplay = QTextEdit()
        self.matrixDisplay.setFixedSize( 165, 180 )

#        self.valuesDisplay = QTextEdit()
#        self.valuesDisplay.setFixedSize( 50, nbPixels )

        # CHART
#        self.serie = QLineSeries()

#        self.chart = QChart()
#        self.chart.addSeries( self.serie )
#        self.chart.legend().hide()
#        self.chart.layout().setContentsMargins( 0, 0, 0, 0 )

#        self.xAxis = QValueAxis()
#        self.xAxis.setTitleText( "Height" )
#        self.xAxis.setLabelFormat( "%d" )
#        self.xAxis.setRange( 0, nbPixels )

#        self.yAxis = QValueAxis()
#        self.yAxis.setLabelFormat( "%d" )
#        self.yAxis.setTitleText( "Distance " )
#        self.yAxis.setRange( 0, couleurMax )

#        self.chart.setAxisX( self.xAxis )
#        self.chart.setAxisY( self.yAxis )

#        self.serie.attachAxis( self.xAxis )
#        self.serie.attachAxis( self.yAxis )

#        self.chart.setTitle( "Profile line" )

#        self.chartView = QChartView( self )
#        self.chartView.setChart( self.chart )
#        self.chartView.rotate( 90 )
#        self.chartView.setGeometry( 20, 195, 450, 400 )
        #end CHART

        self.timer = QTimer( self )
        self.timer.setInterval( periode )
        self.timer.start
        self.timer.timeout.connect( self.refresh )

        self.startButton = QPushButton( "START" )
        self.startButton.setDefault( True )
        self.startButton.clicked.connect( self.startTimer )
        self.startButton.setFixedSize( 100, 50 )

        self.stopButton = QPushButton( "STOP" )
        self.stopButton.setDefault( True )
        self.stopButton.clicked.connect( self.stopTimer )
        self.stopButton.setFixedSize( 100, 50 )

        topLayout = QGridLayout()
        topLayout.addWidget( self.startButton, 0, 0 )
        topLayout.addWidget( self.stopButton, 1, 0 )

        mainLayout = QGridLayout()
        mainLayout.addLayout( topLayout, 0, 0 )
        mainLayout.addWidget( self.pixelRow, 0, 1, 2, 1 )
#        mainLayout.addWidget( self.valuesDisplay, 0, 2, 2, 1 )
#        mainLayout.addWidget( self.chartView, 1, 0 )
        mainLayout.addWidget( self.matrixDisplay, 1, 0 )

        mainwidget = QWidget()
        mainwidget.setLayout( mainLayout )
        self.setCentralWidget( mainwidget )

        self.setWindowTitle( "Minecraft Depth Map" )

    def startTimer( self ):
        self.timer.start()

    def stopTimer( self ):
        self.timer.stop()

    def refresh( self ):
#        self.serie.clear()
#        self.valuesDisplay.clear()
        screen = app.primaryScreen()
        #grabWindow(wID, x, y, w, h)
        pix = QPixmap(screen.grabWindow( 0, int((screenW*3)/4)-10, int((screenH-nbPixels)/2), 20, nbPixels ))
        self.pixelRow.setPixmap( pix )
        img = QImage( pix.toImage() )

        array=[0 for i in range( nbBlocsH )]

        for i in range( nbBlocsH ):
            y = nbPixels - (i*(nbPixels/nbBlocsH) + (nbPixels/(2*nbBlocsH)))
            colorvalue = 255 - QColor(img.pixel( 10, y ) ).black()
#            self.valuesDisplay.append( str(colorvalue) )
#            self.valuesDisplay.append( "\n" )
#            self.serie.append(y, colorvalue)

            #convert colors from 0->couleurMax to 0->nbBlocsD
            if colorvalue > couleurMax:
                colorvalue = nbBlocsD
            elif colorvalue < couleurMin:
                colorvalue = 0
            else:
                colorvalue = int(colorvalue/(couleurMax/nbBlocsD))
            array[i]=colorvalue

        self.convertToMatrix(array)

    def convertToMatrix(self, array):

        matrix=[[0 for j in range(nbBlocsD)] for i in range(nbBlocsH)]
	motifS=[[0 for i in range(x)] for j in range(y)]
	motifS=[[0, 0, 0, 0], 
	 [1, 1, 1, 1], 
	 [0, 0, 0, 0], 
	 [0, 0, 0, 0]] 

        for i in range(nbBlocsH):
            if array[i]<nbBlocsD:
                matrix[i][array[i]]=1
                if i<(nbBlocsH-1):
                    if array[i+1] > (array[i]+1):
                        for j in range(array[i]+1,min(nbBlocsD,array[i+1])):
                            matrix[i][j]=1
                if i>0:
                    if array[i-1] > (array[i]+1):
                        for j in range(array[i]+1,min(nbBlocsD,array[i-1])):
                            matrix[i][j]=1

        sendDataToDisplay(matrix,nbBlocsD,nbBlocsH)
        self.displayMatrix(motifS)

    def displayMatrix(self, matrix):
        self.matrixDisplay.clear()
        for j in range(nbBlocsD-1,-1,-1):
            line = ""
            for i in range(nbBlocsH):
                line = line + str(matrix[i][j]) + "  "
                #self.matrixDisplay.append( line)
                #self.matrixDisplay.append( str(matrix[i][j]) + "  ")
                #self.matrixDisplay.moveCursor( QTextCursor.EndOfLine )
            self.matrixDisplay.append( line)
            #self.matrixDisplay.append("\n" )


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainwd = MainWindow()
    mainwd.show()
    sys.exit(app.exec_())
