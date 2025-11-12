# server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permite que o Netlify acesse o servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # coloca o domínio do Netlify aqui depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de conexões ativas
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            # Envia a mensagem pra todos conectados
            for conn in connections:
                await conn.send_text(message)
    except WebSocketDisconnect:
        connections.remove(websocket)
