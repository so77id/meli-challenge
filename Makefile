# Definir el nombre de la imagen
IMAGE_NAME=jupyter_env

# Puerto local para acceder a Jupyter Notebook
PORT=8888

# URL desde donde descargar el archivo models.zip
MODELS_URL=https://drive.google.com/uc?export=download&id=1otP77DL6_A-tmXWgaBnaIIWjLhTSH16u

# URL desde donde descargar el archivo data.zip
DATA_URL=https://drive.google.com/uc?export=download&id=1KxkmU7XEkkycf0Regkm1QNzL7szvVt-_

build:
	docker build -t $(IMAGE_NAME) Dockerfile.jupyter

run:
	docker run -p $(PORT):8888 -v "${PWD}:/home/jovyan/work" $(IMAGE_NAME)

init:
	# Descargar y preparar los modelos
	mkdir -p ./models
	wget -O models.zip "$(MODELS_URL)"
	unzip models.zip -d ./models
	rm models.zip

	# Descargar y preparar los datos
	mkdir -p ./data
	wget -O data.zip "$(DATA_URL)"
	unzip data.zip -d ./data
	rm data.zip

# Comando para facilitar el acceso al Jupyter Notebook desde localhost
# Asegúrate de reemplazar $(PORT) con el puerto específico que deseas utilizar si cambias el valor predeterminado
