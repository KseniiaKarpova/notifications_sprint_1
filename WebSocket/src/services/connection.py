from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id):
        try:
            self.active_connections.pop(user_id)
        except Exception:
            pass

    async def send_personal_message(self, user_id, message: str):
        websocket = self.active_connections.get(user_id, None)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for id, connection in self.active_connections.items():
            await connection.send_text(message)


connects_manager = None


async def get_manager():
    return connects_manager
