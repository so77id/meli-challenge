# Utilizar la imagen oficial de Jupyter Notebook con Python 3 como base
FROM jupyter/scipy-notebook:latest

# Instalar dependencias adicionales
USER root

# Instalar todos los paquetes necesarios
RUN pip install --no-cache-dir tensorflow
RUN pip install --no-cache-dir scikit-learn 
RUN pip install --no-cache-dir lightgbm 
RUN pip install --no-cache-dir xgboost 
RUN pip install --no-cache-dir scikeras 
RUN pip install --no-cache-dir wordcloud
RUN pip install --no-cache-dir nltk


# Cambiar al usuario no root recomendado por Jupyter
USER ${NB_UID}

# Exponer el puerto por defecto de Jupyter
EXPOSE 8888

# Comando para ejecutar Jupyter Notebook
# No es necesario especificarlo ya que la imagen base ya contiene una configuración adecuada para ejecutar Jupyter Notebook
