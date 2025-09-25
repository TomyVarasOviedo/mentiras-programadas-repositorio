# syntax=docker/dockerfile:1
FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV MODEL_PATH=/models/SmolLM3-3B-GGUF/SmolLM3-3B-GGUF.gguf
ENV LLAMA_CPP_DIR=/opt/llama.cpp

# Dependencias de sistema necesarias para compilar llama.cpp y paquetes Python
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  git build-essential cmake libssl-dev pkg-config curl \
  && rm -rf /var/lib/apt/lists/*

# Clonar y compilar llama.cpp (soporta GGUF)
RUN git clone --depth 1 https://github.com/ggerganov/llama.cpp.git ${LLAMA_CPP_DIR} \
  && cd ${LLAMA_CPP_DIR} \
  && make

# Actualizar pip e instalar dependencias Python
# llama-cpp-python detectará la build de llama.cpp si LLAMA_CPP_DIR está presente
RUN python -m pip install --upgrade pip setuptools wheel \
  && pip install --no-cache-dir \
  "llama-cpp-python>=0.1" \
  fastapi \
  "uvicorn[standard]" \
  websockets

# Directorio de la app
WORKDIR /app

# Copiamos server.py (archivo incluido más abajo)
COPY server.py /app/server/server.py

# Puerto para la API / websocket
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]


