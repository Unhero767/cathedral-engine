import datetime
from fastapi import FastAPI, Request

def register_terminal_webhook(app: FastAPI):
    @app.post("/api/terminal/webhook")
    async def receive_terminal_webhook(request: Request):
        body = await request.json()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n[{timestamp}] [ASH TERMINAL ALERT] Severity: {body.get('severity')}")
        print(f"Source: {body.get('source')}")
        print(f"Payload: {body.get('message')}\n")
        
        return {"status": "received", "acknowledged_at": timestamp}
