# Producto Integrador de Aprendizaje, Estructura de datos y su procesamiento.

from collections import namedtuple
import sys
import sqlite3
from sqlite3 import Error
from datetime import date, datetime
import os.path
from os import path
import datetime

# Declaraciones iniciales
separador = ('-' * 45)

print('Bienvenido(a) al negocio de venta de llantas')
print(separador)

def creacionBD_PIA():
    if path.exists("BD_PIA.db") == False:
        # Creación de Base de datos con el Folio y Descripcion Ventas
        try:
            with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
                cursorPIA = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
                cursorPIA.execute("CREATE TABLE IF NOT EXISTS Folios (folio INTEGER PRIMARY KEY NOT NULL, fecha TEXT NOT NULL);") #3 Envio instrucciones mediante el curosr
                cursorPIA.execute("CREATE TABLE IF NOT EXISTS DescVentas (descripcion TEXT NOT NULL, cantidad INTEGER NOT NULL, precio REAL NOT NULL, folio INTEGER NOT NULL, FOREIGN KEY (folio) REFERENCES Folios (folio));") #3 Envio instrucciones mediante el cursor
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()
        print("No se identificó una base de datos, se creó (BD_PIA.db)")
        print(separador)
    else:
        print("Se identificó la base de datos (BD_PIA.db)")
        print(separador)

def Menu():
    while True:
        opcion = input('Menú de opciones:\n[1] Registrar una venta\n[2] Consultar venta(s) de un día específico\n[3] Salir\n» ')
        try:
            int(opcion)
            if 1 <= int(opcion) <= 3:
                break # La validación es correcta
            else:
                print("\nError #2: Introduzca un número de entre 1 y 3")
                print(separador)
        except ValueError:
            try:
                float(opcion)
                print("test")
            except ValueError:
                print("\nError #1: Introduzca un número")
                print(separador)
    return opcion

def RegistrarVenta():

    totalFinalUnitario = 0

    try:
        with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
            cursorPIA = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones

            while True:

                error3 = "Error #3 El folio ya existe"
                error4 = "Error #4 Introduzca un número mayor a 0"
                error5 = "Error #5 Lo introducido está vacío o contiene sólo espacios."
                error6 = "Error #6 intente con un número"

                # Sistema de obtención de fecha actual en sistema
                fecha = datetime.datetime.now()
                year = '{:02d}'.format(fecha.year)
                month = '{:02d}'.format(fecha.month)
                day = '{:02d}'.format(fecha.day)
                fecha = '{}/{}/{}'.format(day, month, year)
                print("Confirmación de fecha:",fecha)
                print(separador)

                # Sistema de validación de existencia de Folio de Venta (en BD)
                while True:
                    folioVenta = input("Ingrese el folio de la venta\n» ")
                    try:
                        int(folioVenta)
                        folioVenta = int(folioVenta)
                        if folioVenta > 0:
                            valor_folio = {"Folio":folioVenta} #Diccionario para evitar inyeccion de sql
                            cursorPIA.execute("SELECT folio FROM Folios WHERE folio = :Folio", valor_folio)
                            registro = cursorPIA.fetchall()
                            if registro:
                                print(error3)
                            else:
                                break
                        else:
                            print(error4)
                    except:
                        print(error6)

                # Mecanismo de inyección de datos a SQL en Folios
                folioVentaInt = int(folioVenta)
                valores_venta = {"folio":folioVentaInt, "fecha":fecha}
                cursorPIA.execute("INSERT INTO Folios VALUES(:folio, :fecha);", valores_venta)
                print(separador)

                while True: # While para varios productos en misma venta

                    # Sistema de obtención de descripción del producto
                    while True:
                        descripcion = input('Introduzca descripción del tipo de Llanta (Ej: Michelin)\n» ')
                        if descripcion and descripcion.strip():
                            break
                        else:
                            print(error5)

                    while True:
                        # Sistema de obtención de cantidad del producto
                        cantidadVenta = input('Introduzca cantidad a vender del tipo de llanta\n» ')
                        try:
                            int(cantidadVenta) # Validación TRY
                            if cantidadVenta and cantidadVenta.strip():
                                if int(cantidadVenta) > 0:
                                    break
                                else:
                                    print(error4)
                            else:
                                print(error5)
                        except:
                            print(error6)

                    # Sistema de obtención del precio del producto
                    validaNumeroFloat = False
                    while not validaNumeroFloat:
                        try:
                            precioVenta = float(input('Introduzca precio (sin iva) del tipo de llanta (por unidad)\n» $'))
                            if precioVenta > 0:
                                validaNumeroFloat = True
                            else:
                                print(error4)
                        except ValueError:
                            print(error6)

                    # Sistema temporal de almacenamiento de total
                    totalFinalUnitario = totalFinalUnitario + ( int(precioVenta) * int(cantidadVenta) )

                    # Mecanismo de inyección de datos a SQL en DescVentas
                    folioVentaInt = int(folioVenta)
                    valores_articulo = {"descripcion":descripcion, "cantidad":cantidadVenta, "precio":precioVenta, "folio":folioVentaInt}
                    cursorPIA.execute("INSERT INTO DescVentas VALUES(:descripcion, :cantidad, :precio, :folio);", valores_articulo)
                    print(separador)
                    while True:
                        try:
                            pregunta = int(input("¿Quiere seguir registrando? [1] Si [2] No\n» "))
                            if pregunta <= 0 or pregunta >= 3:
                                print("Ingrese una opción válida (1 ó 2)")
                                print(separador)
                            else:
                                break
                        except:
                            print(error6)
                    if int(pregunta) == 1:
                        print(separador)
                    else:
                        break
                print(separador)
                print('\nEl subtotal a pagar es » ${:.2f}'.format(totalFinalUnitario))
                print('El total a pagar es » ${:.2f}'.format(totalFinalUnitario+totalFinalUnitario*.16))

                break
    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()

def ConsultarVenta():
    try:
        with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
            cursorPIA = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
            while True:
                fechaAConsultar = input("Ingrese la fecha a buscar (ej: 14/11/2021)\n» ")
                fecha = datetime.datetime.now()
                year = '{:02d}'.format(fecha.year)
                month = '{:02d}'.format(fecha.month)
                day = '{:02d}'.format(fecha.day)
                fecha = '{}/{}/{}'.format(day, month, year)

                if fechaAConsultar > fecha:
                    print("Error: La fecha no es valida, ingrese otra")
                else:

                    try:
                        sumaUnitariaTotal = 0
                        cursorPIA.execute("""SELECT DescVentas.folio, DescVentas.descripcion, DescVentas.cantidad, DescVentas.precio, Folios.fecha \
                                            FROM DescVentas\
                                            INNER JOIN Folios on DescVentas.folio = Folios.folio\
                                            WHERE Folios.fecha = ?""",(fechaAConsultar,))

                        resultados = cursorPIA.fetchall()
                        if resultados:

                            # Mecanismo de obtención de datos por fila
                            print(separador)
                            print("En la fecha:", fechaAConsultar, "se encontró:",len(resultados),"venta(s) dentro de la base de datos")
                            print(separador)
                            print("Folio |  Descripcion   | Cantidad | Precio unitario")
                            contador = 0
                            for row in zip(*resultados):
                                contador += 1
                                if contador == 1: # Columna 1
                                    columna1=[*row] # Guarda lista de columna
                                if contador == 2: # Columna 2
                                    columna2=[*row] # Guarda lista de columna
                                if contador == 3: # Columna 3
                                    columna3=[*row] # Guarda lista de columna
                                if contador == 4: # Columna 4
                                    columna4=[*row] # Guarda lista de columna

                            for valor in range(len(resultados)):
                                sumaUnitariaTotal = sumaUnitariaTotal + (columna3[valor]*columna4[valor])
                                print(" {:^4} | {:^14} | {:^8} | ${:.2f}".format(columna1[valor],columna2[valor],columna3[valor],columna4[valor]))
                            print(separador)

                            print("Subtotal: ${:.2f}".format(sumaUnitariaTotal))
                            print("IVA: ${:.2f}".format(sumaUnitariaTotal*.16))
                            print("Total: ${:.2f}".format(sumaUnitariaTotal+sumaUnitariaTotal*.16))
                            print(separador)

                        else:
                            print("Fecha no existe en la base de datos")
                            print(separador)

                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"Error: {sys.exc_info()[0]}")
                    break

    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()

while True:
    creacionBD_PIA()
    opcionElegida = Menu() # Manda a ejecutar menú y trae elección
    if int(opcionElegida) == 1:
        RegistrarVenta()
    if int(opcionElegida) == 2:
        ConsultarVenta()
    if int(opcionElegida) == 3:
        break