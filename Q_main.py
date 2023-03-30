from GUI_struct import QApp
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
win = QApp()

win.show()
sys.exit(app.exec_())

'''
EVENTUALMENTE AGGIUNGERE QUI:
- file di configurazione
- calcolo delle curve di bortfeld e creazione file 'bortfeld_curves_mlfc.py' a partire dallo script 'bortfeld_curves_creator.py' con le specifiche del dispositivo
- costanti che possono variare tra un dispositivo e l'altro
'''