# Mentiras Programadas

## Instalacion

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TomyVarasOviedo/mentiras-programadas-repositorio.git
   ```

2. Ejecutar el siguiente comando para hacer el build de docker:

   ```bash
   docker build -t mentiras-programadas:latest .
   ```

3. Ejecutar el siguiente comando para correr el contenedor:

    ```bash
    docker run docker run --rm -p 8000:8000 -v /ruta/local/models:/models -e MODEL_PATH=/models/SmolLM3-3B-GGUF/SmolLM3-3B-GGUF.gguf smollm3-chat:latest
    ```
