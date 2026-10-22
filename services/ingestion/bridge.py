# services/ingestion/bridge.py

import json
import time
import requests
import paho.mqtt.client as mqtt

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "hvacr/telemetry/#"
API_ENDPOINT = "http://localhost:8000/api/v1/telemetry"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[BRIDGE] Connecté avec succès au broker MQTT.")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"[BRIDGE] Échec de la connexion, code d'erreur : {rc}")

def on_message(client, userdata, msg):
    try:
        # Décodage du message MQTT reçu
        payload_str = msg.payload.decode('utf-8')
        data = json.loads(payload_str)
        
        print(f"[MQTT REÇU] Sujet : {msg.topic} | Données : {data}")

        # Transformation / Adaptation du format pour l'API si nécessaire
        # On s'assure d'avoir les champs attendus par l'API FastAPI
        telemetry_payload = {
            "equipment_id": data.get("equipment_id", "eq_chambre_01"),
            "room_temp": data.get("roomTemp", 4.0),
            "suction_pressure_bar": data.get("suctionPressure", 2.2),
            "discharge_pressure_bar": data.get("dischargePressure", 12.0),
            "compressor_status": data.get("isCompressorOn", False)
        }

        # Envoi des données vers l'API REST
        response = requests.post(API_ENDPOINT, json=telemetry_payload, timeout=3.5)
        
        if response.status_code == 200:
            res_data = response.json()
            print(f"[API SYNC] OK - Alertes détectées : {res_data.get('alerts_triggered', 0)}")
            if res_data.get('messages'):
                for alert in res_data['messages']:
                    print(f"  -> 🚨 {alert}")
        else:
            print(f"[API SYNC] Erreur HTTP {response.status_code} : {response.text}")

    except json.JSONDecodeError:
        print("[ERREUR] Impossible de décoder le message JSON reçu.")
    except requests.exceptions.ConnectionError:
        print("[ERREUR] Impossible de joindre l'API FastAPI. Vérifiez qu'elle est bien démarrée.")
    except Exception as e:
        print(f"[ERREUR INATTENDUE] {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"[BRIDGE] Tentative de connexion au broker MQTT {MQTT_BROKER}:{MQTT_PORT}...")
    
    # Boucle de reconnexion automatique
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            print(f"[BRIDGE] Connexion perdue ou impossible ({e}). Nouvel essai dans 5 secondes...")
            time.sleep(5)

if __name__ == "__main__":
    main()
Dépendances P