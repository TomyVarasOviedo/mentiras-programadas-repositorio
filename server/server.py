import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from llama_cpp import Llama

MODEL_PATH = os.environ.get(
    "MODEL_PATH", "/models/SmolLM3-3B-GGUF/SmolLM3-3B-GGUF.gguf"
)

# Inicializar modelo (carga al iniciar la app)
# Ajusta los kwargs de Llama() según tu hardware (n_gpu_layers, n_ctx, etc.)
llm = Llama(model_path=MODEL_PATH)

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
  <head><title>Chat WebSocket</title></head>
  <body>
    <h3>Chat con SmolLM3 (via WebSocket)</h3>
    <textarea id="log" cols="80" rows="20"></textarea><br/>
    <input id="msg" size="80"/><button onclick="send()">Enviar</button>
    <script>
      const ws = new WebSocket("ws://" + location.host + "/ws");
      const log = document.getElementById("log");
      ws.onmessage = (e) => { log.value += "\\n" + e.data; };
      function send() {
        const m = document.getElementById("msg").value;
        ws.send(m);
      }
    </script>
  </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()
            # Simple prompt assembly: se podría mejorar guardando historial, etc.
            prompt = text

            # Llame a la API de llama-cpp-python.
            # Dependiendo de la versión de llama-cpp-python la llamada puede ser:
            #   response = llm(prompt, max_tokens=256)                    # forma simple
            #   response = llm.create_completion(prompt=prompt, max_tokens=256)  # otra forma
            #
            # A continuación usamos la interfaz simple (ajusta si tu versión es distinta).
            response = llm(prompt, max_tokens=256, do_sample=False)

            # 'response' suele ser un dict; aquí tomamos la primera salida textual.
            # Ajusta según la estructura real devuelta por tu versión.
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
