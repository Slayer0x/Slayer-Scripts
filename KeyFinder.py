import requests, json, time, argparse, os

#Colors
GREEN = '\033[92m'
ORANGE = '\033[38;5;214m'
RESET = '\033[0m' 
RED = '\033[0;31m' 
CYAN = '\033[0;36m' 

# Verificar y sacar domínios del fichero
def verificar_archivo(archivo):
    if not os.path.isfile(archivo):
        print(RED + f"\n[!] Error: El archivo '{archivo}' no existe o no es un fichero válido." + RESET)
        exit(1)

# Función para leer los nombres desde un archivo
def leer_nombres(fichero):
    with open(fichero, 'r') as f:
        nombres = f.read().splitlines()
    return nombres

# Función para hacer la solicitud GET y obtener el resultado
def hacer_get_request(nombre):
    url = f"{'https://api.proxynova.com/comb?query=' + nombre + '&start=0&limit=100'}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Asumiendo que la respuesta sea un JSON
    else:
        return {"error": f"[+] Error {response.status_code} obteniendo los datos de {nombre}"}

# Función para guardar los resultados en un archivo con formato
def guardar_resultados(resultados, fichero_salida):
    with open(fichero_salida, 'w') as f:
        for nombre, resultado in resultados.items():
            # Convertir a JSON con indentación para mejor legibilidad
            resultado_formateado = json.dumps(resultado, indent=4)
            f.write(ORANGE + f"\n ######## Dumps para {nombre} ######## \n" + RESET + f"{resultado_formateado}" + "\n")

# Función principal
def main(fichero_entrada, fichero_salida):
    nombres = leer_nombres(fichero_entrada)
    resultados = {}

    for nombre in nombres:
        time.sleep(1) #Sleep one seccond for API limitations.
        resultado = hacer_get_request(nombre)
        resultados[nombre] = resultado
        # Mostrar en la terminal formateado
        print(ORANGE + f"\n######## Dumps para {nombre} ########" + RESET)
        print(json.dumps(resultado, indent=4))
        print(ORANGE + "-" * 50 + RESET)  # Separador visual en la terminal

    guardar_resultados(resultados, fichero_salida)
    print(GREEN + f"\n\n [V] Resultados guardados en {fichero_salida}\n" + RESET)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Procesa los correos electrónicos, palabras o contenidos en un archivo en busca de leaks públicos.")
    parser.add_argument('archivo', help='Ruta al archivo que contiene los correos , palabras o contenidos (1 por línea).')
    args = parser.parse_args()
    verificar_archivo(args.archivo)

    fichero_entrada = (args.archivo)  
    fichero_salida = 'resultados.txt'

    print(CYAN + """          
        ██╗  ██╗███████╗██╗   ██╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
        ██║ ██╔╝██╔════╝╚██╗ ██╔╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
        █████╔╝ █████╗   ╚████╔╝     █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
        ██╔═██╗ ██╔══╝    ╚██╔╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
        ██║  ██╗███████╗   ██║       ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
        ╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
         """+ RED + "@By Slayer0x""" + RESET)
    
    main(fichero_entrada, fichero_salida)