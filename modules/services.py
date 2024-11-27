from modules.routes import *

# MENU PRINCIPAL
def mainMenu():
    print('\n******  MENU PRINCIPAL  ******')
    print('1. BUSCAR RUTA')
    print('2. LISTAR CIUDADES')
    print('3. LISTAR RUTAS')
    print('4. AGREGAR CIUDAD')
    print('5. SALIR\n')

def showCities():
    contador = 0
    for city in cities:
        contador += 1
        if city == 'CUENCA,EC':
            city = 'CUENCA'
        print(f'{contador}. {city}')


# VALIDAR SELECCION DEL MENU
def validateSelection(a, b, option):
    if option >= a and option <= b:
        return False
    else:
        print(f'\n*** OPCION NO VALIDA, DEBES ESCOGER UNA OPCION ENTRE {a} Y {b} ***\n')
        return True


# VALIDAR QUE LA CATEGORIA SEA VALIDA
def validateCity(city):
    if city in cities:
        return False
    else:
        print('\n*** LA CIUDAD NO SE ENCUENTRA EN EL SISTEMA, VUELVE A INTENTARLO ***\n')
        return True


async def validateNewCity(city):
    newCity = await get_coord(city)
    if newCity is None:
        print(f"Error: No se encontraron coordenadas para {city}")
        return True
    else:
        print(f'DATOS DE LA CIUDAD: {newCity}')
        return False