import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as pl
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors

def abrir_archivo( filename):
    return pd.ExcelFile( filename)

def buscar_masa_MA (fle_open):
    #Busca la casilla con el valor de material activo.
    #print('Algo hemos llegado a leer.')
    int_hoja_buscada = -1
    str_info = "Info"
    arr_hojas = fle_open.sheet_names
    for ii in range(0,len(arr_hojas)):
        if arr_hojas[ii] == str_info:
            int_hoja_buscada = ii
            break
    sht_hoja = pd.read_excel(fle_open,int_hoja_buscada)
    #print('Algo hemos llegado a leer.')
    material_activo = (sht_hoja.iloc[3,1])
    #print('Algo hemos llegado a leer.')
    
    boo_aceptar = False
    flo_MA = False
    posicion_masa = -1
    if posicion_masa == -1:
        posicion_masa = material_activo.find('mg de MA')
    if posicion_masa == -1:
        posicion_masa = material_activo.find('mg de material activo')
    if posicion_masa == -1:
        posicion_masa = material_activo.find('mg MA ')
    if posicion_masa == -1:
        posicion_masa = material_activo.find('mg material activo')

    #print('Vamos a leer la casilla.' + material_activo[:posicion_masa])
    if not posicion_masa == -1:
        #print('Entrando al loop.')
        for i in range(1,5):
            str_ma = material_activo[posicion_masa-i:posicion_masa]
    #        print ('determinando' + str_ma)
            try:
                flo_MA = float(str_ma)
    #            print ("Es " + str(flo_MA))
            except:
    #            print ("no es")
                pass
    #print ('No se traba todavia.')
    if type(flo_MA) == float:
        #print (str(flo_MA) + ' es la respuesta y todavia no se traba.')
        return flo_MA
    #print('No encontramos la cantidad de masa con sufijo.')

    
    if posicion_masa == -1:
        posicion_masa = material_activo.find('activo ')
        if not posicion_masa == -1:
            posicion_masa = posicion_masa + len('activo ')
    if posicion_masa == -1:
        posicion_masa = material_activo.find('Activo ')
        if not posicion_masa == -1:
            posicion_masa = posicion_masa + len('activo ')
    if posicion_masa == -1:
        posicion_masa = material_activo.find('MA ')
        if not posicion_masa == -1:
            posicion_masa = posicion_masa + len('MA ')
    if not posicion_masa == -1 and (type(flo_MA)!=float):
        try:
            flo_MA = float(material_activo[posicion_masa:posicion_masa+3])
        except:
            flo_MA = -1
    if flo_MA > 0:
        boo_aceptar = True
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
    return flo_MA

def buscar_hoja_ciclados( fle_open ):
    str_hojas = "Channel"
    arr_hojas = fle_open.sheet_names
    int_hojas = len(arr_hojas)
    for ii in range(0, int_hojas):
        if arr_hojas[ii][:7] == str_hojas:
            int_hoja_buscada = ii
            break
    if arr_hojas[int_hoja_buscada][:7] != str_hojas:
        return 'No se encuentra una hoja con el nombre predeterminado.'
    return (ii)

def generar_hoja( fle_open ):
    int_hoja_buscada = buscar_hoja_ciclados( fle_open )
    arr_columnas = (pd.read_excel(fle_open,int_hoja_buscada)).columns
    arr_interes = ['Data_Point', 'Test_Time(s)', 'Date_Time', 'Step_Time(s)', 'Step_Index',
           'Cycle_Index', 'Current(A)', 'Voltage(V)', 'Charge_Capacity(Ah)',
           'Discharge_Capacity(Ah)']
    arr_seleccion = []
    int_columnas = len(arr_columnas)
    int_interes = len(arr_interes)
    for ii in range(0, int_columnas):
        for jj in range (0, int_interes):
            if (arr_columnas[ii] == arr_interes[jj]):
                arr_seleccion.append(ii)
    return pd.read_excel(fle_open,int_hoja_buscada,usecols=arr_seleccion)

def separar_ciclos ( sht_hoja , flo_MA ):
    arr_interes = list(sht_hoja.columns.values)
    int_columnas_a_usar = len(arr_interes)
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
    arr_append = np.zeros((1,2))
    arr_existe = False;
    arr_archivo = False;
    filas_interes=sht_hoja.shape[0]
    int_ultimo_paso = -1;
    int_primer_paso = True
    arr_ciclos_tiempo = [0]
    arr_ciclos_tipo = ['Carga']
    arr_ciclos_limite = [0]
    jj = 0
    flt_corriente = 0.0;
    flt_paso=0;
    for ii in range(0, filas_interes):
        flt_corriente = sht_hoja["Current(A)"][ii]
        if not flt_corriente == 0:
            arr_append[0,1] = sht_hoja["Voltage(V)"][ii]
            if flt_corriente > 0:
                arr_append[0,0] = sht_hoja["Charge_Capacity(Ah)"][ii] * 1000000 / flo_MA
            else:
                arr_append[0,0] = sht_hoja["Discharge_Capacity(Ah)"][ii] * 1000000 / flo_MA
            flt_paso = sht_hoja["Step_Index"][ii]
            if not int_ultimo_paso == flt_paso:
                int_ultimo_paso = flt_paso
                arr_existe = False
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
            if arr_existe == False:
                arr_graficar = arr_append
                arr_existe = True
            else:
                arr_graficar = np.append(arr_graficar,arr_append,axis=0)

            jj = ii
            arr_ciclos_limite[-1] = 1 + arr_ciclos_limite[-1]
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
    return arr_archivar, arr_ciclos_tiempo, arr_ciclos_tipo, arr_ciclos_limite




def hacer_graficas(arr_archivar, arr_ciclos_tiempo, arr_ciclos_tipo, arr_ciclos_limite):
    #Verificamos que tenemos todos los valores que necesitamos.
    arr_decir = len(arr_ciclos_tiempo)
    jj=0
    arr_eficiencias = ()
    arr_descargas = ()
    arr_lineas = ()
    x_min = 1000;
    x_max = -1;
    y_min = 1000;
    y_max = -1;

    #Refactorizado para que tenga menos líneas.
    for kk in range(0, arr_decir):
        ##Se leen en sentido inverso, desde el último hasta el primero, para estar seguros de que el más viejo se vea por encima.
        ii = -1-kk
        ##Ahora, armamos algo más dinámico.
        arr_armado = np.zeros(((arr_ciclos_limite[ii]),2));
        arr_armado[:,0] = arr_archivar[0:arr_ciclos_limite[ii],2*ii]
        x_min = min(x_min,arr_armado[:,0].min())
        x_max = max(x_max,arr_armado[:,0].max())
        arr_armado[:,1] = arr_archivar[0:arr_ciclos_limite[ii],2*ii+1]
        y_min = min(y_min,arr_armado[:,1].min())
        y_max = max(y_max,arr_armado[:,1].max())
        arr_lineas = arr_lineas + (arr_armado,)
        
        if arr_ciclos_tipo[ii] == ['Carga']:
            if kk != arr_decir-1:
                flt_carga = arr_archivar[arr_ciclos_limite[ii]-1,2*ii]
                flt_eficiencia = 100*arr_descargas[-1]/flt_carga
                if flt_eficiencia > 200:
                    flt_eficiencia = 0
                arr_eficiencias = arr_eficiencias + (flt_eficiencia,)
        else:
            arr_descargas = arr_descargas + (arr_archivar[arr_ciclos_limite[ii]-1,2*ii],)
    return arr_lineas, arr_eficiencias, arr_descargas, x_min, x_max, y_min, y_max


def hacer_graficas_ciclos(arr_archivar, arr_ciclos_tiempo, arr_ciclos_limite):
    arr_decir = len(arr_ciclos_tiempo)
    jj=0
    arr_eficiencias = ()
    arr_descargas = ()
    arr_lineas = ()
    x_min = 1000;
    x_max = -1;
    y_min = 1000;
    y_max = -1;
    for kk in range(0, arr_decir):
        ii = -1-kk
        arr_armado = np.zeros(((arr_ciclos_limite[ii]),2));
        arr_armado[:,0] = arr_archivar[0:arr_ciclos_limite[ii],2*ii]
        x_min = min(x_min,arr_armado[:,0].min())
        x_max = max(x_max,arr_armado[:,0].max())
        arr_armado[:,1] = arr_archivar[0:arr_ciclos_limite[ii],2*ii+1]
        y_min = min(y_min,arr_armado[:,1].min())
        y_max = max(y_max,arr_armado[:,1].max())
        arr_lineas = arr_lineas + (arr_armado,)
    return arr_lineas, x_min, x_max, y_min, y_max



def dibujar_capacidades (arr_lineas, x_min, x_max, y_min, y_max):
    fig, ax = pl.subplots()
    #colors = [mcolors.to_rgba(c)
    #      for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    coulores = ('black', 'black','blue','blue','purple','purple','red','red','green','green','cyan','cyan','orange','orange','pink','pink','darkgreen','darkgreen')
    line_segments = LineCollection(arr_lineas, colors=coulores)
    ax.add_collection(line_segments)
    ax.set_xlim(x_min,x_max)
    ax.set_ylim(y_min,y_max)
    pl.show()
    return None

def dibujar_eficiencias (arr_eficiencias, arr_descargas):
    arr_eficiencias = arr_eficiencias[::-1]
    arr_descargas = arr_descargas[::-1]
    arr_equis = range(1,len(arr_descargas)+1)
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
    return None

#Para probar.
if False:
    bi = abrir_archivo('bar.xls')
    bo = buscar_masa_MA(bi)
    bu = generar_hoja(bi)
    bf, ctm, cty, cl = separar_ciclos(bu, bo)
    al, ae, ad, xm, xM, ym, yM = hacer_graficas(bf, ctm, cty, cl)
    dibujar_capacidades(al, xm, xM, ym, yM)
    dibujar_eficiencias(ae, ad)
