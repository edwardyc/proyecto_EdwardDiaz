"""Lógica del sistema: datos, login, registros, diagnóstico e historia clínica."""
import hashlib
import json
import os
from datetime import datetime

from ayudas import (titulo, linea, ok, error, dato, pedir, pedir_numero,
                    pedir_email, pedir_telefono, pedir_contrasena, elegir)

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "datos", "datos.json")


# ---------- Guardar y leer el JSON ----------
def cifrar(contrasena):
    """Convierte la contraseña en un código para no guardarla en texto plano."""
    return hashlib.sha256(contrasena.encode()).hexdigest()


def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def cargar():
    """Lee el JSON. Si no existe, lo crea con el usuario Admin."""
    if not os.path.exists(ARCHIVO):
        admin = {"id": "0000", "nombres": "Admin", "apellidos": "Administrador",
                 "telefono": "555 000111", "email": "admin@acmeclinic.com",
                 "direccion": "Cl 185 # 26 - 85", "rol": "Administrativo",
                 "contrasena": cifrar("admin123")}
        guardar({"usuarios": [admin], "pacientes": [], "consultas": []})
    with open(ARCHIVO, encoding="utf-8") as f:
        return json.load(f)


def buscar(lista, id):
    """Busca una persona por su identificación. Devuelve None si no existe."""
    for persona in lista:
        if persona["id"] == id:
            return persona
    return None


# ---------- Login ----------
def login(datos):
    titulo("Clínica ACME - Inicio de sesión")
    while True:
        email = input("  Usuario (e-mail) o 'volver': ").strip().lower()
        if email == "volver":
            return None
        contrasena = input("  Contraseña: ")
        for u in datos["usuarios"]:
            if u["email"] == email and u["contrasena"] == cifrar(contrasena):
                ok(f"Bienvenido(a) {u['nombres']} {u['apellidos']} ({u['rol']})")
                return u
        error("Usuario o contraseña incorrectos.")


# ---------- Registros ----------
def pedir_persona(lista):
    """Pide los datos comunes de usuarios y pacientes."""
    id = pedir("No. de identificación")
    if buscar(lista, id):
        error("Ya existe alguien con esa identificación.")
        return None
    return {"id": id, "nombres": pedir("Nombres"), "apellidos": pedir("Apellidos"),
            "telefono": pedir_telefono(), "email": pedir_email(),
            "direccion": pedir("Dirección")}


def registrar_usuario(datos):
    titulo("Registrar usuario")
    usuario = pedir_persona(datos["usuarios"])
    if usuario is None:
        return
    if any(u["email"] == usuario["email"] for u in datos["usuarios"]):
        error("Ya existe un usuario con ese e-mail.")
        return
    usuario["rol"] = elegir("Rol:", ["Médico", "Administrativo"])
    usuario["contrasena"] = cifrar(pedir_contrasena())
    datos["usuarios"].append(usuario)
    guardar(datos)
    ok("Usuario registrado correctamente.")


def registrar_paciente(datos):
    titulo("Registrar paciente")
    paciente = pedir_persona(datos["pacientes"])
    if paciente is None:
        return
    paciente["genero"] = elegir("Género:", ["Masculino", "Femenino", "Otro"])
    paciente["estado_civil"] = elegir(
        "Estado civil:", ["Soltero(a)", "Casado(a)", "Unión libre", "Divorciado(a)", "Viudo(a)"])
    datos["pacientes"].append(paciente)
    guardar(datos)
    ok("Paciente registrado correctamente.")


# ---------- Diagnóstico ----------
def pedir_sintomas():
    print("\n  Síntomas (Enter vacío para terminar)")
    sintomas = []
    while True:
        s = input(f"    Síntoma {len(sintomas) + 1}: ").strip()
        if s:
            sintomas.append(s)
        elif sintomas:
            return sintomas
        else:
            error("Escriba al menos un síntoma.")


def pedir_medicamentos():
    print("\n  Prescripción médica (Enter vacío para terminar)")
    medicamentos = []
    while True:
        nombre = input(f"    Medicamento {len(medicamentos) + 1}: ").strip()
        if nombre:
            medicamentos.append({"medicamento": nombre,
                                 "cantidad": pedir_numero("      Cantidad (unidades)"),
                                 "dosis": pedir("      Dosis diaria (ej: 1 cada 8 horas)"),
                                 "dias": pedir_numero("      Tiempo de aplicación (días)")})
        elif medicamentos:
            return medicamentos
        else:
            error("Escriba al menos un medicamento.")


def diagnosticar(datos, medico):
    titulo("Diagnosticar paciente")
    if medico["rol"] != "Médico":
        error("Solo los usuarios con rol Médico pueden diagnosticar.")
        return
    paciente = buscar(datos["pacientes"], pedir("Identificación del paciente"))
    if paciente is None:
        error("Paciente no registrado. Regístrelo primero.")
        return
    print(f"  Paciente: {paciente['nombres']} {paciente['apellidos']}")

    sintomas = pedir_sintomas()
    diagnostico = pedir("\n  Diagnóstico (enfermedad o patología)")
    medicamentos = pedir_medicamentos()

    ahora = datetime.now()
    consulta = {"fecha": ahora.strftime("%Y-%m-%d %H:%M:%S"),
                "id_paciente": paciente["id"], "id_medico": medico["id"],
                "sintomas": sintomas, "diagnostico": diagnostico,
                "medicamentos": medicamentos}
    datos["consultas"].append(consulta)
    guardar(datos)

    # Un archivo JSON por cada prescripción (asociado a fecha, paciente y médico)
    prescripcion = {"fecha": consulta["fecha"],
                    "paciente": {"id": paciente["id"],
                                 "nombre": f"{paciente['nombres']} {paciente['apellidos']}"},
                    "medico": {"id": medico["id"],
                               "nombre": f"{medico['nombres']} {medico['apellidos']}"},
                    "diagnostico": diagnostico,
                    "medicamentos": medicamentos}
    nombre = f"prescripcion_{paciente['id']}_{ahora.strftime('%Y%m%d_%H%M%S')}.json"
    ruta = os.path.join(CARPETA, "prescripciones", nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(prescripcion, f, ensure_ascii=False, indent=4)
    ok("Diagnóstico guardado.")
    ok(f"Prescripción generada: prescripciones/{nombre}")


# ---------- Historia clínica ----------
def historia_clinica(datos):
    titulo("Historia clínica")
    paciente = buscar(datos["pacientes"], pedir("Identificación del paciente"))
    if paciente is None:
        error("Paciente no registrado.")
        return

    print("\n  DATOS DEL PACIENTE")
    linea()
    dato("Identificación:", paciente["id"])
    dato("Nombre:", f"{paciente['nombres']} {paciente['apellidos']}")
    dato("Teléfono:", paciente["telefono"])
    dato("E-mail:", paciente["email"])
    dato("Dirección:", paciente["direccion"])
    dato("Género:", paciente["genero"])
    dato("Estado civil:", paciente["estado_civil"])

    consultas = [c for c in datos["consultas"] if c["id_paciente"] == paciente["id"]]
    consultas.sort(key=lambda c: c["fecha"], reverse=True)   # la más reciente primero
    print(f"\n  CONSULTAS ({len(consultas)})")
    linea()
    if not consultas:
        print("  El paciente aún no tiene consultas.")
    for c in consultas:
        medico = buscar(datos["usuarios"], c["id_medico"])
        dato("Fecha:", c["fecha"])
        dato("Médico:", f"{medico['nombres']} {medico['apellidos']}")
        dato("Síntomas:", ", ".join(c["sintomas"]))
        dato("Diagnóstico:", c["diagnostico"])
        print("  Medicamentos:")
        for m in c["medicamentos"]:
            print(f"    • {m['medicamento']} - {m['cantidad']} und - "
                  f"{m['dosis']} - {m['dias']} día(s)")
        linea()
