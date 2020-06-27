import pandas as pd
import urllib3 as url3

def downloadFromURL(url, decode = "utf-8", sep = ",", sep_columnas = ",", del_comillas = False, del_n = False, del_r = False):
    try:
        http = url3.PoolManager() # crear el pool manager
        r = http.request('GET', url) # obtener datos por metodo get
        print("Estado de conexión:", r.status) # mostrar el estado de conexión, si es 200 es aceptable
        datos = (r.data).decode(decode).strip() # guardo los datos decodificados y sin espacios
        if del_comillas == True:
            datos = datos.replace('"',"") # elimino las comillas dobles
        if del_n == True:
            datos = datos.replace('\n',"") # elimino los saltos de linea
        if del_r == True:
            datos = datos.replace('\r',"") # elimino los \r que no se que son
        datos = datos.split(sep) # separo los datos 
        columnas = datos[0].split(sep_columnas) # separo las columnas
        main_dict = {columna:[] for columna in columnas}
        [main_dict[columnas[i]].append(datos[linea].strip().split(sep_columnas)[i]) for linea in range(1, len(datos)) for i in range(0, len(columnas))]
        df = pd.DataFrame(main_dict)
        df['positivos'] = df['positivos'].replace("","0")
        return df
    except UnicodeDecodeError:
        print(">>> Error: no se puede decodificar con UTF-8 por defecto, utilice 'utf-16' u otro decodificador.")

covid_df = downloadFromURL('https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Determinaciones.csv',
                          'utf-16',
                          del_comillas = True,
                           sep = '\r',
                           del_n = True
                          )
covid_df.head(10)