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

#Ordenamos nuestros stats.
int_columnas_a_usar = len(arr_seleccion)
for ii in range(0, int_columnas_a_usar):
    if (arr_interes[ii] == 'Cycle_Index'):
        ciclo = ii
    if (arr_interes[ii] == 'Step_Index'):
        paso = ii
    if (arr_interes[ii] == 'Current(A)'):
        corriente = ii
    if (arr_interes[ii] == 'Charge_Capacity(Ah)'):
        carga = ii
    if (arr_interes[ii] == 'Discharge_Capacity(Ah)'):
        descarga = ii
    if (arr_interes[ii] == 'Voltage(V)'):
        voltaje = ii
    if (arr_interes[ii] == 'Step_Time(s)'):
        tiempo = ii

#Vamos ahora a separar segmentos. Para cada uno, debemos decidir si corresponde carga o descarga. Para ello, generaremos un nuevo array.
arr_append = np.zeros((1,2))
arr_existe = False;
arr_archivo = False;
filas_interes=sht_hoja.shape[0]
int_ultimo_paso = -1;
int_primer_paso = True

#Para cada ciclo, registrar tiempo, de donde obtendremos C, tipo de ciclo, y 
arr_ciclos_tiempo = [0]
arr_ciclos_tipo = ['Carga']
jj = 0 #Uso JJ para marcar los que no valen 0.

#Esto extrae los ceros de corriente, que no interesan.
for ii in range(0, filas_interes):
    if not sht_hoja["Current(A)"][ii] == 0:
        
        #Armamos la tupla.
        arr_append[0,1] = sht_hoja["Voltage(V)"][ii]
        if sht_hoja["Current(A)"][ii] > 0:
            arr_append[0,0] = sht_hoja["Charge_Capacity(Ah)"][ii]
        else:
            arr_append[0,0] = sht_hoja["Discharge_Capacity(Ah)"][ii]

        #Verificamos que seguimos en el mismo paso. De no ser así, abrimos un nuevo paso.
        if not int_ultimo_paso == sht_hoja["Step_Index"][ii]:
            int_ultimo_paso = sht_hoja["Step_Index"][ii]
            arr_existe = False

            #El primer ciclo, se salta.
            if int_primer_paso:
                int_primer_paso = False
            else:
                arr_ciclos_tiempo[-1] = sht_hoja["Step_Time(s)"][jj]
                arr_ciclos_tiempo = arr_ciclos_tiempo + [0]
                if sht_hoja["Current(A)"][ii] < 0:
                    arr_ciclos_tipo[-1] = ['Carga']
                else:
                    arr_ciclos_tipo[-1] = ['Descarga']
                arr_ciclos_tipo = arr_ciclos_tipo + [0]
                
                if arr_archivo == True:
                    if not arr_archivar.shape[0] == arr_graficar.shape[0]:
                        if arr_archivar.shape[0] > arr_graficar.shape[0]:
                            arr_igualar = np.zeros((abs(arr_archivar.shape[0]-arr_graficar.shape[0]),arr_graficar.shape[1]))
                            arr_graficar = np.append(arr_graficar,arr_igualar, 0)
                        if arr_archivar.shape[0] < arr_graficar.shape[0]:
                            arr_igualar = np.zeros((abs(arr_archivar.shape[0]-arr_graficar.shape[0]),arr_archivar.shape[1]))
                            arr_archivar = np.append(arr_archivar,arr_igualar, 0)
                            
                    arr_archivar = np.append(arr_archivar,arr_graficar,1)
                else:
                    arr_archivo = True
                    arr_archivar = np.copy(arr_graficar)
                    
        #Registrar los ultimos valores en la ultima serie.
        if arr_existe == False:
            arr_graficar = arr_append
            arr_existe = True
        else:
            arr_graficar = np.append(arr_graficar,arr_append,axis=0)

        jj = ii

##OK, el loop ha finalizado.
arr_ciclos_tiempo[-1] = sht_hoja["Step_Time(s)"][jj]
if sht_hoja["Current(A)"][ii] > 0:
    arr_ciclos_tipo[-1] = ['Carga']
else:
    arr_ciclos_tipo[-1] = ['Descarga']

if not arr_archivar.shape[0] == arr_graficar.shape[0]:
    if arr_archivar.shape[0] > arr_graficar.shape[0]:
        arr_igualar = np.zeros((abs(arr_archivar.shape[0]-arr_graficar.shape[0]),arr_graficar.shape[1]))
        arr_graficar = np.append(arr_graficar,arr_igualar, 0)
    if arr_archivar.shape[0] < arr_graficar.shape[0]:
        arr_igualar = np.zeros((abs(arr_archivar.shape[0]-arr_graficar.shape[0]),arr_archivar.shape[1]))
        arr_archivar = np.append(arr_archivar,arr_igualar, 0)

arr_archivar = np.append(arr_archivar,arr_graficar,1)
##OK, estas listo.

#Ahora los dibujamos.
#Vamos a usar la funcion exec.
#Es un agujero negro en la seguridad, pero esto es de uso en academia, no sale de aca.
poit = 'arr_archivar[0:200,2],arr_archivar[0:200,3], "b," '
exec('pl.plot(' + poit + ')')

arr_decir = len(arr_ciclos_tiempo)
for ii in range(0, arr_decir):
    print("El ciclo numero " + str(ii) + " es de " + str(arr_ciclos_tipo[ii]) + " con una duracion de " + str(int(arr_ciclos_tiempo[ii])) + " segundos")

#Mostrame que hemos hecho.
pl.show()
