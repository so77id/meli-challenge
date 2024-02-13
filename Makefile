# Definir el nombre de la imagen
IMAGE_NAME=jupyter_env

# Puerto local para acceder a Jupyter Notebook
PORT=8888

build:
	docker build -t $(IMAGE_NAME) Dockerfile.jupyter

run:
	docker run -p $(PORT):8888 -v "${PWD}:/home/jovyan/work" $(IMAGE_NAME)

# Comando para facilitar el acceso al Jupyter Notebook desde localhost
# Asegúrate de reemplazar $(PORT) con el puerto específico que deseas utilizar si cambias el valor predeterminado
