"""Ayudas: cómo se ve el programa (títulos, mensajes) y cómo se piden los datos."""
ANCHO = 60


def titulo(texto):
    print("\n" + "=" * ANCHO)
    print(texto.upper().center(ANCHO))
    print("=" * ANCHO)


def linea():
    print("-" * ANCHO)


def ok(texto):
    print(f"  ✔ {texto}")


def error(texto):
    print(f"  ✖ {texto}")


def dato(etiqueta, valor):
    """Muestra una línea 'Etiqueta: valor' alineada."""
    print(f"  {etiqueta:<16}{valor}")


def pedir(mensaje):
    """Pide un texto. No deja continuar si se deja vacío."""
    while True:
        valor = input(f"  {mensaje}: ").strip()
        if valor:
            return valor
        error("Este campo es obligatorio.")


def pedir_numero(mensaje):
    """Pide un número entero mayor que cero."""
    while True:
        valor = input(f"  {mensaje}: ").strip()
        if valor.isdigit() and int(valor) > 0:
            return int(valor)
        error("Escriba un número mayor que cero.")


def pedir_email():
    while True:
        valor = pedir("E-mail").lower()
        if "@" in valor and "." in valor.split("@")[-1] and " " not in valor:
            return valor
        error("E-mail no válido (ejemplo: nombre@correo.com).")


def pedir_telefono():
    while True:
        valor = pedir("Teléfono")
        if valor.replace(" ", "").replace("+", "").isdigit() and len(valor) >= 7:
            return valor
        error("Teléfono no válido (solo números, mínimo 7).")


def pedir_contrasena():
    while True:
        valor = input("  Contraseña (mín. 6 caracteres): ")
        if len(valor) >= 6:
            return valor
        error("La contraseña es muy corta.")


def elegir(mensaje, opciones):
    """Muestra una lista numerada y devuelve la opción elegida."""
    print(f"  {mensaje}")
    for numero, opcion in enumerate(opciones, 1):
        print(f"    {numero}. {opcion}")
    while True:
        valor = input("  Elija una opción: ").strip()
        if valor.isdigit() and 1 <= int(valor) <= len(opciones):
            return opciones[int(valor) - 1]
        error("Opción no válida.")
