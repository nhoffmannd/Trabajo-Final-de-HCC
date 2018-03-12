#Nicolás Hoffmann: Setup para herramienta de evaluación de ciclos de batería.
#En primer lugar, debo importar pandas, numpy, y xlrd. Completos, por ahora.
import pandas as pd
import numpy as np
import xlrd
import matplotlib as mp
import matplotlib.pyplot as pl

#Ahora, vamos a probar la importación de un excel a Pandas.
#La función es xlsx = pd.ExcelFile('foo.xls'). Ya cambiaremos foo.
#Vamos a elegir una columna dentro de foo.

##YA NO SIRVE##xlsx = pd.ExcelFile('foo.xls')
##YA NO SIRVE##df = pd.read_excel(xlsx, 'Sheet1', usecols=[0,2,3])

#Siguiendo a partir de aquí, debemos elegir las columnas de interes.
#Esto nos lleva a necesitar un .xls similar a los que utilizaremos.
#Lo cargamos como 'bar.xls'.
fle_open = pd.ExcelFile('bar.xls')

#Tomando arr_rows, vemos si alguna fila es de la forma "Channel_1*".
#Iteramos sobre arr_hojas, para probar cuáles empiezan en Channel.
arr_hojas = fle_open.sheet_names
int_hojas = len(arr_hojas)

#No olvidemos los ":" si estás iterando en python.
str_hojas = "Channel"
for ii in range(0, int_hojas):
    if arr_hojas[ii][:7] == str_hojas:
        int_hoja_buscada = ii
        break

#Verificamos que todo haya salido bien. Para evitar else, hacemos un if/exit.
if arr_hojas[int_hoja_buscada][:7] != str_hojas:
    print ('No se encuentra una hoja con el nombre predeterminado.')
    exit

#Estando todo en orden, vamos a tomar la primera fila, los de interes.
#arr_interes = ['Data_Point','Test_time(s)','Step_time(s)','Step_Index','Cycle_Index','Voltage(V)','Charge_Capacity(Ah)','Discharge_Capacity(Ah)']
arr_columnas = (pd.read_excel(fle_open,int_hoja_buscada)).columns
#arr_columnas = sht_hoja.columns

#Para realizar análisis, vamos a ver unas columnas en particular.
arr_interes = ['Data_Point', 'Test_Time(s)', 'Date_Time', 'Step_Time(s)', 'Step_Index',
       'Cycle_Index', 'Current(A)', 'Voltage(V)', 'Charge_Capacity(Ah)',
       'Discharge_Capacity(Ah)']

#Ya usamos ii, podemos reutilizarlo.
arr_seleccion = []

int_columnas = len(arr_columnas)
int_interes = len(arr_interes)
for ii in range(0, int_columnas):
    for jj in range (0, int_interes):
        if (arr_columnas[ii] == arr_interes[jj]):
            arr_seleccion.append(ii)

#Entonces, tenemos la lista de arr_seleccion.
sht_hoja = pd.read_excel(fle_open,int_hoja_buscada,usecols=arr_seleccion)

equis = 0
yagriega = 0

#Vamos a elegir ahora dos columnas para probar.
int_columnas_a_usar = len(arr_seleccion)
for ii in range(0, int_columnas_a_usar):
    if (arr_interes[ii] == 'Charge_Capacity(Ah)'):
        equis = ii
    if (arr_interes[ii] == 'Voltage(V)'):
        yagriega = ii

#Esto nos devuelve sht_hoja, con lo que podremos tratar los resultados.
#pl.plot(sht_hoja.iloc[:,[equis]],sht_hoja.iloc[:,[yagriega]])
#pl.show()

#Esto anda. Ahora, lo que tenemos que hacer, es empezar a organizar una serie de valores de X y de Y.
#Vamos a hacer eso usando la columna Step_Index. Cada vez que cambie, vamos a saltar dos valores en n_secuencia.
#Eso nos genera una nueva columna para X, una nueva columna para Y.
##Reiniciamos el loop cada vez que cambia el step_index, o el cycle_index.
n_secuencia = 0
n_fila = 0

ciclo_actual = -1
paso_actual = -1
arr_graficar = []
ciclo_usado = False

#Aclarar: ciclo, paso, corriente, col_x, col_y



int_filas_a_trabajar = sht_hoja.shape[0]
for ii in range(0, int_filas_a_trabajar):
    ##Si cambiamos de ciclo, pasar a un ciclo más, SALVO que no se haya escrito nada en este ciclo.
    if !((sht_hoja.iloc[ii,ciclo] == ciclo_actual) && (sht_hoja.iloc[ii,paso] == paso_actual) && (ciclo_usado == False )):
        n_secuencia = n_secuencia+2
        n_fila = 0
        ciclo_actual = sht_hoja.iloc[ii, ciclo]
        paso_actual = sht_hoja.iloc[ii, ciclo]
    ##Incluir en el gráfico de ciclado si la corriente no vale cero.
    if (sht_hoja.iloc[ii,corriente] != 0):
        arr_graficar[n_fila,n_secuencia] = sht_hoja.iloc[ii, col_x]
        arr_graficar[n_fila+1,n_secuencia] = sht_hoja.iloc[ii, col_y]
        n_fila = n_fila +1

#Con el ciclaje terminado, podemos graficar.
