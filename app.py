from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import serial
import threading
import time
import requests

app = Flask(__name__)

modo_sistema = "AUTOMATICO"
nivel_actual = 0
ultimo_guardado = 0

# IP DEL ESP32 ACTUADOR
ESP32_ACTUADOR = "http://10.119.61.85"

# SUPABASE
SUPABASE_URL = "https://erutzaxqskowdhaudlbc.supabase.co/rest/v1/eventos_estanque"
SUPABASE_KEY = "sb_publishable_WcNJVntiJvUrmIHSn2Cqew_pMscY3UU"


def enviar_orden(ruta):
    try:
        r = requests.get(ESP32_ACTUADOR + ruta, timeout=2)
        print("Orden enviada:", ruta, r.text)
    except Exception as e:
        print("Error enviando orden:", e)


def calcular_estado(nivel):
    if nivel >= 70:
        return "NORMAL", "VERDE", "Nivel de agua correcto"
    elif nivel >= 35:
        return "MEDIO", "AMARILLO", "Nivel de agua en observación"
    else:
        return "BAJO", "ROJO", "Alerta: nivel de agua bajo"


def guardar_supabase(nivel, estado, modo):
    global ultimo_guardado

    ahora = time.time()

    if ahora - ultimo_guardado < 5:
        return

    ultimo_guardado = ahora

    datos = {
        "nivel": nivel,
        "estado": estado,
        "modo": modo
    }

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(
            SUPABASE_URL,
            json=datos,
            headers=headers,
            timeout=3
        )
        print("Supabase:", r.status_code)
    except Exception as e:
        print("Error Supabase:", e)


def leer_serial():
    global nivel_actual

    try:
        puerto = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        time.sleep(2)

        while True:
            linea = puerto.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if linea.startswith("NIVEL:"):
                try:
                    nivel_actual = int(linea.replace("NIVEL:", ""))

                    estado, led, mensaje = calcular_estado(nivel_actual)

                    print("Nivel recibido:", nivel_actual)

                    guardar_supabase(
                        nivel_actual,
                        estado,
                        modo_sistema
                    )

                except:
                    pass

    except Exception as e:
        print("Error leyendo ESP32 sensor:", e)


hilo_serial = threading.Thread(
    target=leer_serial,
    daemon=True
)
hilo_serial.start()


def obtener_datos():

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if modo_sistema == "MANTENIMIENTO":
        estado = "MANTENIMIENTO"
        led = "AMARILLO"
        mensaje = "Sistema detenido por mantenimiento"

    elif modo_sistema == "FALLA":
        estado = "FALLA"
        led = "ROJO"
        mensaje = "Alarma activada manualmente"

    else:
        estado, led, mensaje = calcular_estado(nivel_actual)

    return (
        nivel_actual,
        estado,
        led,
        mensaje,
        fecha,
        modo_sistema
    )


@app.route("/")
def index():

    nivel, estado, led, mensaje, fecha, modo = obtener_datos()

    return render_template(
        "index.html",
        nivel=nivel,
        estado=estado,
        led=led,
        mensaje=mensaje,
        fecha=fecha,
        modo=modo
    )


@app.route("/automatico")
def automatico():
    global modo_sistema

    modo_sistema = "AUTOMATICO"

    enviar_orden("/verde")

    return redirect(url_for("index"))


@app.route("/mantenimiento")
def mantenimiento():
    global modo_sistema

    modo_sistema = "MANTENIMIENTO"

    enviar_orden("/amarillo")

    return redirect(url_for("index"))


@app.route("/falla")
def falla():
    global modo_sistema

    modo_sistema = "FALLA"

    enviar_orden("/rojo")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
