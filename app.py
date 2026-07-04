from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import random

app = Flask(__name__)

modo_sistema = "AUTOMATICO"

def leer_estanque():
    global modo_sistema

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if modo_sistema == "MANTENIMIENTO":
        nivel = 50
        estado = "MANTENIMIENTO"
        led = "AMARILLO"
        mensaje = "Sistema detenido por mantenimiento"

    elif modo_sistema == "FALLA":
        nivel = 15
        estado = "FALLA"
        led = "ROJO"
        mensaje = "Alarma activada manualmente"

    else:
        nivel = random.randint(0, 100)

        if nivel >= 70:
            estado = "NORMAL"
            led = "VERDE"
            mensaje = "Nivel de agua correcto"
        elif nivel >= 35:
            estado = "MEDIO"
            led = "AMARILLO"
            mensaje = "Nivel de agua en observación"
        else:
            estado = "BAJO"
            led = "ROJO"
            mensaje = "Alerta: nivel de agua bajo"

    return nivel, estado, led, mensaje, fecha, modo_sistema


@app.route("/")
def index():
    nivel, estado, led, mensaje, fecha, modo = leer_estanque()

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
    return redirect(url_for("index"))


@app.route("/mantenimiento")
def mantenimiento():
    global modo_sistema
    modo_sistema = "MANTENIMIENTO"
    return redirect(url_for("index"))


@app.route("/falla")
def falla():
    global modo_sistema
    modo_sistema = "FALLA"
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
