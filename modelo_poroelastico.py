#Libs
import pandas as pd
import math

#Funcion para calcular los cambios de presión de poro inducidos por la lluvia
#############################################################################

#Variables:
#h, profundidad en metros
#c, difusividad hidraulica entre 0.1 y 10 m^2/s
#sampling, muestreo en segundos, para calculos diarios es igual a 24*3600 s
#rain, lluvia acumulada en MILÍMETROS


#Devuelve:
#Serie de tiempo del cambio de presiones que, posteriormente se puede empatar con una lista de fechas

def talwani_model(h, c, sampling, rain):
    
    #Inicia el cálculo de las cargas de agua 
    mean_rain = rain.mean()
    water_change = ((rain - mean_rain)**2)**0.5          #Desviación lineal entre cada medida de lluvia y el promedio
    water_change_pa = (water_change/1000) * 9.81 * 997   #Coversión a presiones en PASCALES
    
    #Fórmula y diccionario para calcular el valor de erfc en función de la diferencia de días
    def calc_erfc(h, c, sampling, x):
        y = math.erfc(h/math.sqrt(c*4*sampling*x))
        return y
    
    indexes_dict = range(1,len(rain)+100)
    dict_erfc = {}
    for value in indexes_dict:
        dict_erfc[value] = calc_erfc(h=h,c=c,sampling=sampling,x=value)
    dict_erfc[0] = 0
    
    
    #Inicia el cálculo de los cambios de presión
    model = []
    
    for ind,value in enumerate(water_change_pa):
        i = ind
        n = -i-1
        result = 0
        counter = 0
        while counter > n:
            partial = water_change_pa[i+counter] * dict_erfc[-counter]  
            result += partial
            counter -= 1
        model.append(result)
    #return model

    
    def pore_pressure_change(series):
        pp_change = []
        for ind,value in enumerate(series):
            if ind < len(model)-1:
                pp_change.append(series[ind+1] - series[ind])
            else:
                break
        return pp_change
    
    #Resultado
    talwani_sol = pore_pressure_change(model)
    talwani_sol = pd.Series(talwani_sol)
    return(talwani_sol)
