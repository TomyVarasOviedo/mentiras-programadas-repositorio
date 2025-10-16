import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from transformers import pipeline
from transformers import AutoTokenier

model_id = "HuggingFaceTB/SmolLM3-3B"

tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer)

SYSTEM_PROMPT = """[INSTRUCCIONES]\nFrom now on, you will speak Spanish at all times."""


app = FastAPI()


@app.get("/")
async def get():
    file = open("index.html")
    html_content = file.read()
    file.close()
    return HTMLResponse(html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    message = [{"role": "system", "content": "/no_think"}]
    try:
        while True:
            text = await websocket.receive_text()
            # Simple prompt assembly: se podría mejorar guardando historial, etc.
            prompt = text

            Personaje = ""
            message.append(
                {
                    "role": "user",
                    "content": f"\n{SYSTEM_PROMPT}\n{prompt}\n{Personaje} ",
                }
            )
            response = pipe(message)

            text_out = None
            if isinstance(response, dict):
                # formatos comunes: {'choices': [{'text': '...'}], ...} o {'choices': [{'message': {'content': '...'}}]}
                choices = response.get("choices")
                if choices and len(choices) > 0:
                    c = choices[0]
                    # intento de cubrir formatos comunes:
                    text_out = c.get("text") or (
                        c.get("message") and c["message"].get("content")
                    )
            if text_out is None:
                # Fallback: stringify whole response
                text_out = str(response)

            await websocket.send_text(text_out)
    except WebSocketDisconnect:
        return
