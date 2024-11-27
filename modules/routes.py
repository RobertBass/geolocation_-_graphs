import subprocess
import sys

# LIBRERIAS NECESARIAS
required_packages = ['geopy.distance','geopy.exc','geopy.geocoders', 'networkx']

def install(package):
    # Ejecuta el comando pip y usa "python -m pip" para mayor compatibilidad
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--break-system-packages'])

# Verificar e instalar cada librería si no está ya instalada
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando {package}...")
        try:
            install(package)
        except subprocess.CalledProcessError:
            print(f"Error al instalar {package}. Verifica los permisos o instala manualmente.")


import asyncio
import geopy.distance
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderServiceError, GeocoderUnavailable
from geopy.geocoders import Nominatim
import networkx as nx

geo = Nominatim(user_agent='App')

# CREACION DEL GRAFO
location = nx.DiGraph()

cities = ['AMBATO','GUAYAQUIL', 'CUENCA,EC']
distances = {}

async def get_coord(city):
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, geo.geocode, city)
    except GeocoderTimedOut:
        print(f"NO SE PUDO OBTENER LA UBICACION DE {city}...")
    except GeocoderQuotaExceeded:
        print("HA EXCEDIDO EL NUMERO DE SOLICITUDES.")
    except GeocoderServiceError:
        print("ERROR EN EL SERVICIO, INTENTE NUEVAMENTE")
    except GeocoderUnavailable:
        print("SERVICIO NO DISPONIBLE POR EL MOMENTO.")
    except Exception as e:
        print(f"ERROR: {e}")


async def load():
    # AGREGAR LOS NODOS (CIUDADES) AL GRAFO
    for city in cities:
        location.add_node(city)
    # OBTENER LAS DISTANCIAS ENTRE CIUDADES
    for i in range(len(cities)):
        orig = await get_coord(cities[i])
        if orig is None:
            print(f"Error: No se encontraron coordenadas para {cities[i]}")
            continue
        coord_origin = (orig.latitude, orig.longitude)
        for j in range(i + 1, len(cities)):
            dest = await get_coord(cities[j])
            if dest is None:
                print(f"ERROR: NO SE ENCONTRARON COORDENADAS PARA {cities[j]}")
                continue
            coord_destination = (dest.latitude, dest.longitude)
            dist = geopy.distance.distance(coord_origin, coord_destination)
            distances.update({(cities[i], cities[j]): dist.km})
    # ESTABLECER LAS RUTAS (ARISTAS) CON SUS NODOS (PESO)
    for i in range(len(cities) - 1):
        origin = cities[0]
        destination = cities[i + 1]
        distance = distances.get((origin, destination))
        location.add_edge(origin, destination, weight=distance)
        location.add_edge(destination, origin, weight=distance)


# FUNCION PARA BUSCAR LA MEJOR RUTA HACIA EL DESTINO
def find_route(origin, destination):
    # UTILIZAMOS EL ALGORITMO DE DIJKSTRA PARA ENCONTRAR LA RUTA MAS CORTA
    try:
        route = nx.dijkstra_path(location, origin, destination)
        total_distance = nx.dijkstra_path_length(location, origin, destination)
        # MOSTRAR LA RUTA Y LA DISTANCIA
        print(f"RUTA MAS CORTA ENTRE {origin} Y {destination}:")
        for i in range(len(route) - 1):
            actual_city = route[i]
            next_city = route[i + 1]
            distance = location[actual_city][next_city]['weight']
            print(f"{actual_city} -> {next_city} : {distance} km")
        print(f"DISTANCIA TOTAL: {total_distance} KMS\n")
    except nx.NetworkXNoPath:
        print(f"NO EXISTE UNA RUTA ENTRE {origin} y {destination}.\n")


# FUNCION PARA AGREGAR UNA UBICACION (CIUDAD)
async def add_city(city):
    try:
        cities.append(city)
        distances.clear()
        await load()
        print('CIUDAD REGISTRADA CORRECTAMENTE')
    except nx.exception.NodeNotFound as e:
        print(e)


# PRESENTAR RUTAS
def show_routes():
    for (origin, destination), distance in distances.items():
        if origin == 'CUENCA,EC':
            origin = 'CUENCA'
        if destination == 'CUENCA,EC':
            destination = 'CUENCA'
        print(f'({origin}, {destination}): {distance} KMS')