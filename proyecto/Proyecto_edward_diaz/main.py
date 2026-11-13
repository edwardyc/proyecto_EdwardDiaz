"""Clínica ACME - programa principal. Ejecutar con: python main.py"""
from ayudas import titulo
from funciones import (cargar, login, registrar_usuario, registrar_paciente,
                       diagnosticar, historia_clinica)


def menu(datos, usuario):
    while True:
        titulo("Menú principal")
        print("  1. Registrar usuario")
        print("  2. Registrar paciente")
        print("  3. Diagnosticar paciente")
        print("  4. Historia clínica")
        print("  0. Cerrar sesión")
        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            registrar_usuario(datos)
        elif opcion == "2":
            registrar_paciente(datos)
        elif opcion == "3":
            diagnosticar(datos, usuario)
        elif opcion == "4":
            historia_clinica(datos)
        elif opcion == "0":
            return
        else:
            print("  ✖ Opción no válida.")


datos = cargar()
while True:
    titulo("Clínica ACME")
    print("  1. Iniciar sesión")
    print("  2. Registrarme")
    print("  0. Salir")
    opcion = input("\n  Opción: ").strip()
    if opcion == "1":
        usuario = login(datos)
        if usuario is not None:
            menu(datos, usuario)
    elif opcion == "2":
        registrar_usuario(datos)
    elif opcion == "0":
        print("\n  Hasta pronto.\n")
        break
    else:
        print("  ✖ Opción no válida.")
