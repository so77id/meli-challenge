# Usa una imagen oficial de Python como imagen base
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente de la aplicación al directorio de trabajo
COPY ./src/* .
COPY ./models ./models

# Expone el puerto que Flask utilizará
EXPOSE 3000

# Comando para ejecutar la aplicación en el puerto 3000
CMD ["python", "./src/app.py", "--host=0.0.0.0", "--port=3000"]
