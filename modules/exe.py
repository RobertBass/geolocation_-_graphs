import time
from modules.services import *

async def exe():
    await load()
    print('=======================================================================')
    print('===================== SISTEMA DE GEOLOCALIZACION =====================')
    print('=======================================================================')
    print(f'\nCARGANDO...\n')
    time.sleep(10)
    while True:
        validate = True
        option = 0
        mainMenu()  # MOSTRAMOS EL MUNU PRINCIPAL AL USUARIO

        while validate:
            try:
                option = int(input('SELECCIONA UNA OPCION DEL MENU: '))
                validate = validateSelection(1, 5, option)
                time.sleep(1)
            except ValueError as e:
                print(f'\nERROR: {e} => DEBE INGRESAR UN NUMERO\n')



        if option == 1:
            showCities()
            validate2 = True
            time.sleep(5)
            while validate2 == True:
                try:
                    origin = input(f"\nINGRESE LA CIUDAD DE ORIGEN: ").upper()
                    if origin == 'CUENCA':
                        origin = 'CUENCA,EC'
                    validate2 = validateCity(origin)
                    time.sleep(1)
                except ValueError as e:
                    print(f'\nERROR: {e} => \n')
            validate2 = True
            while validate2 == True:
                try:
                    destination = input("INGRESE LA CIUDAD DE DESTINO: ").upper()
                    if destination == 'CUENCA':
                        destination = 'CUENCA,EC'
                    validate2 = validateCity(destination)
                    time.sleep(1)
                except ValueError as e:
                    print(f'\nERROR: {e} => \n')
            find_route(origin, destination)
            time.sleep(5)

        if option == 2:
            showCities()
            time.sleep(5)

        if option == 3:
            show_routes()
            time.sleep(5)

        if option == 4:
            validate2 = True
            while validate2 == True:
                try:
                    city = input('ESCRIBE EL NOMBRE DE LA CIUDAD QUE DESEAS INGRESAR: ').upper()
                    validate2 = await validateNewCity(city)
                    time.sleep(1)
                except ValueError as e:
                    print(f'\nERROR: {e} => \n')
            await add_city(city)
            print(f'\nCARGANDO...\n')
            time.sleep(10)

        # SALIR DEL PROGRAMA
        if option == 5:
            print('SALIENDO DEL PROGRAMA, VUELVA PRONTO...')
            time.sleep(1)
            exit(0)



