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

##Buscamos la hoja que da los datos de material activo.
int_hoja_buscada = -1
str_info = "Info"
for ii in range(0,int_hojas):
    if arr_hojas[ii] == str_info:
        int_hoja_buscada = ii
        break
sht_hoja =pd.read_excel(fle_open,int_hoja_buscada)
material_activo = (sht_hoja.iloc[3,1])

boo_aceptar = False
#Tratamos de leerlo de manera automatizada. Buscamos los strings que dan algo.
flo_MA = -1
posicion_masa = -1

if posicion_masa == -1:
    posicion_masa = material_activo.find('mg de MA')
if posicion_masa == -1:
    posicion_masa = material_activo.find('mg de material activo')
if posicion_masa == -1:
    posicion_masa = material_activo.find('mg MA ')
if posicion_masa == -1:
    posicion_masa = material_activo.find('mg material activo')

#Si llegamos a algo, posicion deja de ser -1. Entonces, registramos.
if not posicion_masa == -1:
    print("Sufijo")
    try:
        flo_MA = float(material_activo[posicion_masa-5,posicion_masa-2])
    except:
        flo_MA = -1

#Si no, probamos con otra posicion.
if posicion_masa == -1:
    posicion_masa = material_activo.find('activo ')
    if not posicion_masa == -1:
        posicion_masa = posicion_masa + len('activo ')
if posicion_masa == -1:
    posicion_masa = material_activo.find('Activo ')
    print('Mayusculas' + str(posicion_masa))
    if not posicion_masa == -1:
        posicion_masa = posicion_masa + len('activo ')
if posicion_masa == -1:
    posicion_masa = material_activo.find('MA ')
    if not posicion_masa == -1:
        posicion_masa = posicion_masa + len('MA ')

#Ahora registramos otra cosa.
if not posicion_masa == -1:
    print("Prefijo")
    try:
        flo_MA = float(material_activo[posicion_masa:posicion_masa+3])
    except:
        print(material_activo[posicion_masa:posicion_masa+3])
        flo_MA = -1

if flo_MA > 0:
    boo_aceptar = True

#Si no, lo conseguimos manualmente...
boo_empezamos = True
while boo_aceptar == False:
    boo_empezamos = False
    try:
        print(material_activo)
        flo_MA = float(input("Por favor, introduzca la cantidad de material activo, en miligramos. "))
        if type(flo_MA) == float:
            boo_aceptar = True
    except:
        print("No se acepta ese valor. Favor de introducir el valor.")

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
arr_ciclos_limite = [0]
jj = 0 #Uso JJ para marcar el ultimo valor donde la corriente era distinta de 0.

#Refactorización: que lea cada valor una única vez.
flt_corriente = 0.0;
flt_paso=0;

#Esto extrae los ceros de corriente, que no interesan.
for ii in range(0, filas_interes):
    flt_corriente = sht_hoja["Current(A)"][ii]
    if not flt_corriente == 0:
        
        #Armamos la tupla.
        arr_append[0,1] = sht_hoja["Voltage(V)"][ii]
        if flt_corriente > 0:
            arr_append[0,0] = sht_hoja["Charge_Capacity(Ah)"][ii] * 1000000 / flo_MA
        else:
            arr_append[0,0] = sht_hoja["Discharge_Capacity(Ah)"][ii] * 1000000 / flo_MA

        #Verificamos que seguimos en el mismo paso. De no ser así, abrimos un nuevo paso.
        flt_paso = sht_hoja["Step_Index"][ii]
        if not int_ultimo_paso == flt_paso:
            int_ultimo_paso = flt_paso
            arr_existe = False

            #El primer ciclo, se salta.
            if int_primer_paso:
                int_primer_paso = False
            else:
                arr_ciclos_tiempo[-1] = sht_hoja["Step_Time(s)"][jj]
                arr_ciclos_tiempo = arr_ciclos_tiempo + [0]
                arr_ciclos_limite = arr_ciclos_limite + [0]
                if flt_corriente < 0:
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
        arr_ciclos_limite[-1] = 1 + arr_ciclos_limite[-1]

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

#Verificamos que tenemos todos los valores que necesitamos.
arr_decir = len(arr_ciclos_tiempo)
#for ii in range(0, arr_decir):
    #print("Ciclo " + str(ii) + " de " + str(arr_ciclos_tipo[ii]) + " dura " + str(int(arr_ciclos_tiempo[ii])) + " seg, " + str(arr_ciclos_limite[ii]) + " lecturas.")

#Ahora los dibujamos.
#Vamos a usar la funcion exec.
#Es un agujero negro en la seguridad, pero esto es de uso en academia, no sale de aca.
#poit = 'arr_archivar[0:200,2],arr_archivar[0:200,3], "b," '

argumentos = ''

#Inicializar colores.
color = ('FF0000', '0000AA', '00AA00', '999900', '009999', '990099', '555555', '000000', 'FF8888', 'FF0000')
jj=0

arr_eficiencias = ()
arr_descargas = ()

#Refactorizado para que tenga menos líneas.
for kk in range(0, arr_decir):
    ##Se leen en sentido inverso, desde el último hasta el primero, para estar seguros de que el más viejo se vea por encima.
    ii = -1-kk
    argumento = '' + 'arr_archivar[0:' + str(arr_ciclos_limite[ii]) + ',' + str(2*ii) + '],'            #Introducir coord x.
    argumento = argumento + 'arr_archivar[0:' + str(arr_ciclos_limite[ii]) + ',' + str(2*ii+1) + '],'   #Introducir coord y.
    argumento = argumento + "'#" + color[jj] + "'"                                                      #Introducir argumentos de color.

    #Verificar si podemos hablar de eficiencias y de descargas.
    #print('arr_archivar[' + str(arr_ciclos_limite[ii]) + ',' + str(2*ii) + ']' )
    #print(arr_archivar[arr_ciclos_limite[ii]-1,2*ii])
    

    ##Esto busca si empezó un nuevo ciclo, y si es así, cambia el color.
        
    if arr_ciclos_tipo[ii] == ['Carga']:
        if kk != arr_decir-1:
            flt_carga = arr_archivar[arr_ciclos_limite[ii]-1,2*ii]
            flt_eficiencia = 100*arr_descargas[-1]/flt_carga
            if flt_eficiencia > 200:
                flt_eficiencia = 0
            arr_eficiencias = arr_eficiencias + (flt_eficiencia,)
            
        jj = jj +1
        if (jj > len(color)-1):
            jj = 0
    else:
        arr_descargas = arr_descargas + (arr_archivar[arr_ciclos_limite[ii]-1,2*ii],)

    #Cerrar string cuando terminemos.
    if not ii == arr_decir:
        argumento = argumento + ','

    #Agregar a los argumentos totales.
    argumentos = argumentos + argumento

#exec('pl.plot(' + argumentos + ')')

#Mostrar que hemos hecho algo.
#pl.show()

#Luego, invertimos estos arrays.
arr_eficiencias = arr_eficiencias[::-1]
arr_descargas = arr_descargas[::-1]

#Refactorizar esto.
arr_equis = range(1,len(arr_descargas)+1)
#pl.plot(arr_equis[1:],arr_eficiencias,arr_equis,arr_descargas)

color = 'tab:red'

fig, ax1 = pl.subplots()
ax1.set_xlabel("Ciclo")
ax1.set_ylabel('Capacidad de Descarga[mAh/g]', color = color)
ax1.plot(arr_equis, arr_descargas, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Eficiencia[%]',color = color)
ax2.plot(arr_equis[1:], arr_eficiencias, color = color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
pl.show()
