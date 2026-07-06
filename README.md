# 🚰 Sistema IoT - Estanque Inteligente

Proyecto desarrollado para la asignatura **Desarrollo de Software**, utilizando **ESP32, Python Flask, Supabase y GitHub**.

## 👥 Integrantes

- Benjamín Valdebenito
- Gustavo Fuentes

---

# 📖 Descripción

Este proyecto implementa un sistema IoT para el monitoreo y control del nivel de agua de un estanque.

El sistema utiliza dos placas ESP32:

- **ESP32 #1:** Simula el sensor de nivel mediante un potenciómetro y envía continuamente el porcentaje de agua al computador.
- **ESP32 #2:** Funciona como actuador y controla los indicadores LED según el estado del sistema.

Python Flask recibe la información enviada por el ESP32, procesa el nivel del estanque, almacena los eventos en Supabase y actualiza automáticamente la página web.

---

# 🏗 Arquitectura del sistema

```
              ESP32 #1
        (Sensor de Nivel)
               │
          Comunicación Serial
               │
        Python + Flask
               │
      ┌────────┴─────────┐
      │                  │
   Página Web        Supabase
      │
      │ HTTP
      │
   ESP32 #2
 (Actuadores LED)
```

---

# 🛠 Tecnologías utilizadas

- ESP32
- Arduino IDE
- Python
- Flask
- HTML5
- CSS3
- JavaScript
- Supabase
- GitHub

---

# ⚙ Funciones del sistema

✅ Monitoreo del nivel de agua.

✅ Actualización automática de la interfaz web.

✅ Cambio de estado según el nivel del estanque.

✅ Modos de operación:

- Automático
- Mantenimiento
- Falla

✅ Control remoto de LEDs mediante un segundo ESP32.

✅ Registro de eventos en Supabase.

---

# 📷 Capturas del proyecto

## Página principal

![Página Web](capturas/estanque.png)

---

## Sistema funcionando

![Sistema](capturas/estanque1.jpeg)

---

## ESP32

![ESP32](capturas/arduino.jpeg)

---

## Base de datos Supabase

![Supabase](capturas/supabase.jpeg)

---

# 📂 Estructura del proyecto

```
estanque-iot/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   └── js/
├── capturas/
├── README.md
└── requirements.txt
```

---

# 🚀 Ejecución

Instalar dependencias:

```bash
pip install flask
pip install pyserial
pip install requests
```

Ejecutar el proyecto:

```bash
python3 app.py
```

Abrir el navegador:

```
http://127.0.0.1:5000
```

---

# 📊 Base de datos

El sistema almacena automáticamente cada lectura del estanque en Supabase.

Cada registro contiene:

- Fecha y hora
- Nivel de agua
- Estado
- Modo de funcionamiento

---

# 📌 Estado del proyecto

✅ Proyecto finalizado.

- Lectura de nivel mediante ESP32.
- Interfaz web dinámica.
- Actualización automática.
- Comunicación con dos ESP32.
- Registro en Supabase.
- Código respaldado en GitHub.
