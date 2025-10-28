import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- Estilo general con tonos fríos ---
st.markdown("""
    <style>
        /* Fondo con degradado frío */
        .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #e8eaf6 50%, #ede7f6 100%);
            font-family: 'Poppins', sans-serif;
            color: #263238;
        }

        /* Título principal */
        h1, h2, h3 {
            background: linear-gradient(90deg, #4b6cb7, #6a85b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-weight: 700;
        }

        /* Header de Streamlit */
        header[data-testid="stHeader"] {
            background: linear-gradient(90deg, #6a85b6 0%, #bac8e0 50%, #c5cae9 100%);
            color: white !important;
        }

        /* Botones estilo frío */
        .stButton > button {
            background: linear-gradient(90deg, #7e57c2, #9575cd);
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            box-shadow: 0px 4px 12px rgba(123, 97, 255, 0.25);
            transition: 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #6a5ac7, #7b68ee);
            transform: scale(1.02);
        }

        /* Slider personalizado */
        input[type="range"]::-webkit-slider-thumb {
            background: #7e57c2 !important;
            border: 2px solid #5e35b1 !important;
        }

        input[type="range"]::-webkit-slider-runnable-track {
            background: linear-gradient(90deg, #b39ddb, #d1c4e9) !important;
            height: 6px;
            border-radius: 3px;
        }

        /* Texto oscuro para buena legibilidad */
        .stMarkdown, .stMarkdown p, label, div[data-testid="stWidgetLabel"], .stSlider label {
            color: #263238 !important;
            font-weight: 500;
        }

        /* Cuadro inferior de mensaje */
        .msg-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            background: linear-gradient(180deg, #e3f2fd 0%, #f3e5f5 100%);
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- Información de entorno ---
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# --- Título principal ---
st.title("Control MQTT")

# --- Botón ON ---
if st.button('Encender (ON)'):
    act1 = "ON"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)
else:
    st.write('')

# --- Botón OFF ---
if st.button('Apagar (OFF)'):
    act1 = "OFF"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)
else:
    st.write('')

# --- Slider de valores analógicos ---
values = st.slider('Selecciona el valor analógico', 0.0, 100.0)
st.write('Valor seleccionado:', values)

# --- Botón para enviar valor ---
if st.button('Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)
else:
    st.write('')

# --- Cuadro informativo ---
st.markdown("""
<div class="msg-box">
Usa los botones para controlar el dispositivo y el deslizador para enviar valores analógicos.
</div>
""", unsafe_allow_html=True)

