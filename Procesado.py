#Para procesar la grilla de datos, debemos primero separarla en series.
#Estas hojas se obtienen del output de la función ahora en setup.py.
def procesar_grilla(grilla=="none")
    if grilla == "none"
        return "error; no se ha seleccionado un archivo."

##Habiendo seleccionado la grilla, se debe separar en series.
##Cada vez que se encuentran dos elementos de un mismo ciclo, se considera una serie nueva.
##Las series se van agrupando en una tabla, inicialmente vacía.
    series_a_graficar = []

##Empezamos a escribir una tabla en un .csv.
