import socket, shodan, requests, os, argparse

# Reemplaza con tu clave de API de Shodan y Security trails
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'
SECURITY_TRAILS_API_KEY = 'YOUR_SECURITY_TRAILS_API_KEY'

# Inicializar la API de Shodan
api = shodan.Shodan(SHODAN_API_KEY)


# Colores
RED = "\033[31m"
GREEN = "\x1b[38;5;83m"
YELLOW = "\x1b[38;5;226m"
ORANGE = "\033[38;5;208m"
BLUE = "\033[34m"
PURPLE = "\x1b[38;5;93m"
RESET = "\033[0m"


# Verificar y sacar domínios del fichero
def verificar_archivo(archivo):
    if not os.path.isfile(archivo):
        print(RED + f"\n[!] Error: El archivo '{archivo}' no existe o no es un fichero válido." + RESET)
        exit(1)

def leer_dominios(archivo):
    with open(archivo, 'r') as f:
        dominios = f.read().splitlines()
    return dominios


# Lista de dominios a analizar

def obtener_ip(dominio):
    try:
        ip = socket.gethostbyname(dominio)
        return ip
    except socket.gaierror:
        return None

def obtener_informacion_shodan(ip):
    try:
        resultados = api.host(ip)
        return resultados
    except shodan.APIError as e:
        return f"\n [!] Error en Shodan, es posible que la IP no se encuentre listada"

def obtener_informacion_security_trails(customdom):

    url = f"https://api.securitytrails.com/v1/domain/{customdom}"
    
    headers = {
        'apikey': f'{SECURITY_TRAILS_API_KEY}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        
        ip_organization = None
        a_domains = []
        a_ipv6 = []
        mx_domains = []
        
        # Extraer IP organization
        try:
            if 'current_dns' in data and 'a' in data['current_dns']:
                a_records = data['current_dns']['a']['values']
                if a_records:
                    ip_organization = a_records[0].get('ip_organization', 'No disponible')
        except Exception:
            ip_organization = [f"Not found"]

        # Extraer A records
        try:
            if 'current_dns' in data and 'a' in data['current_dns']:
                a_records = data['current_dns']['a']['values']
                a_domains = [record.get('ip', 'No disponible') for record in a_records]
        except Exception:
            a_domains = [f"Not found"]

        # Extraer AAAA records
        try:
            if 'current_dns' in data and 'aaaa' in data['current_dns']:
                aaaa_records = data['current_dns']['aaaa']['values']
                a_ipv6 = [record.get('ipv6', 'No disponible') for record in aaaa_records]
        except Exception:
            a_ipv6 = [f"Not found"]

        # Extraer MX records
        try:
            if 'current_dns' in data and 'mx' in data['current_dns']:
                mx_records = data['current_dns']['mx']['values']
                mx_domains = [record.get('hostname', 'No disponible') for record in mx_records]
        except Exception:
            mx_domains = [f"Not found"]
        
        return {
            'ip_organization': ip_organization,
            'a_domains': a_domains,
            'a_ipv6': a_ipv6,
            'mx_domains': mx_domains,
        }
    
    else:
        return f"Error en SecurityTrails, es posible que el dominio no se encuentre listado"


def analizar_dominios(dominios):
    for dominio in dominios:
        
        print(GREEN + f"\n Dominio: " + RESET + f"{dominio}")
        
        # Obtener IP
        ip = obtener_ip(dominio)
        if ip:
            print(GREEN + f"\n IP: " + RESET + f"{ip}\n")
        else:
            print(RED + "\n [!] No se pudo obtener la IP \n" + RESET)
            continue
        
        # Obtener información de Shodan
        info_shodan = obtener_informacion_shodan(ip)
        if isinstance(info_shodan, dict):
            puertos_abiertos = []
            paises = set()
            ciudades = set()
            proveedores = set()
            organizaciones = set()
            hostnames = set()  # To store hostnames

            for item in info_shodan.get('data', []):
                puertos_abiertos.append(str(item.get('port')))
                
                # Extraer localización
                location = item.get('location', {})
                if location.get('country_name'):
                    paises.add(location['country_name'])
                if location.get('city'):
                    ciudades.add(location['city'])
                                
                # Extraer hostnames
                hostnames.update(item.get('hostnames', []))

                if item.get('isp'):
                    proveedores.add(item.get('isp'))
                if item.get('org'):
                    organizaciones.add(item.get('org'))
            print(BLUE + f"------------------------------------" + RESET)
            print(YELLOW + f"\n Puertos abiertos:" + RESET + f" {', '.join(puertos_abiertos)}")
            print(YELLOW + f"\n Países:" + RESET + f" {', '.join(paises) if paises else 'No disponible'}")
            print(YELLOW + f"\n Ciudades:" + RESET + f" {', '.join(ciudades) if ciudades else 'No disponible'}")
            print(YELLOW + f"\n Hostnames:" + RESET + f" {', '.join(hostnames) if hostnames else 'No disponible'}")  
            print(YELLOW + f"\n Proveedores:" + RESET + f" {', '.join(proveedores) if proveedores else 'No disponible'}")
            print(YELLOW + f"\n Organizaciones:" + RESET + f" {', '.join(organizaciones) if organizaciones else 'No disponible'}")
            
        else:
            print(info_shodan)

        info_security_trails = obtener_informacion_security_trails(dominio)
        if isinstance(info_security_trails, dict):
            print(YELLOW + f"\n Hosting:" + RESET + f" {info_security_trails['ip_organization']}")
            print(YELLOW + f"\n Registros A IPs:" + RESET + f" {', '.join(info_security_trails['a_domains'])}")
            print(YELLOW + f"\n Registros AAAA IPv6s:" + RESET + f" {', '.join(info_security_trails['a_ipv6'])}")
            print(YELLOW + f"\n Registros MX:" + RESET + f" {', '.join(info_security_trails['mx_domains'])}")
            print(PURPLE + f"\n Listado completo de dominios asociados a la IP:" + RESET + f" https://securitytrails.com/app/auth/login?return=/list/ip/{ip}\n")
        else:
            print(RED + "\n [!] No se han encontrado registros asociados en Security Trails\n" + RESET)

        print(BLUE + f"------------------------------------\n" + RESET)
        print(ORANGE + f"#################################################### " + RESET)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Procesa los dominios contenidos en un archivo.")
    parser.add_argument('archivo', help='Ruta al archivo que contiene los dominios (1 por línea).')
    
    args = parser.parse_args()
    
    # Verificar si el archivo existe
    verificar_archivo(args.archivo)

    # Leer y procesar los dominios
    dominios = leer_dominios(args.archivo)
    analizar_dominios(dominios)


    #By @Slayer0x