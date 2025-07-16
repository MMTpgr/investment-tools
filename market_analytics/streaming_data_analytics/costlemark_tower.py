import requests
import websocket
from kafka import KafkaProducer

# Replace this with your own refresh token (generated from Questrade API Centre)
REFRESH_TOKEN = ""

def get_access_token(refresh_token):
    url = f"https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token={refresh_token}"
    res = requests.get(url).json()
    return {
        "access_token": res["access_token"],
        "api_server": res["api_server"]
    }

import requests, websocket, json

def start_rest_ws_stream(api_server, token, symbol_ids):
    url = f"{api_server}v1/markets/quotes?ids={','.join(map(str,symbol_ids))}&stream=true&mode=WebSocket"
    headers = {"Authorization": f"Bearer {token}"}
    port = requests.get(url, headers=headers).json()['streamPort']

    ws_url = f"wss://{api_server.replace('https://','').strip('/')}:{port}/v1/markets/quotes?ids={','.join(map(str,symbol_ids))}&stream=true&mode=WebSocket"
    ws = websocket.WebSocketApp(ws_url,
        on_open=lambda ws: ws.send(token),
        on_message=lambda ws, m: print("📈", m)      # need to send here to kafka
    )
    ws.run_forever()

'''night = get_access_token(REFRESH_TOKEN)
start_rest_ws_stream(night["api_server"],night['access_token'],[8049])'''


BOOTSTRAP_SERVERS = 'https://crestholm.servicebus.windows.net:9093'
EVENT_HUB_NAME = 'ma-veles'

# KafkaProducer config for Event Hubs
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='$ConnectionString',  
    sasl_plain_password=CONNECTION_STRING,    
)

# Send a test message
producer.send(EVENT_HUB_NAME, b'Hello from Kafka to Event Hub!')
producer.flush()
producer.close()

