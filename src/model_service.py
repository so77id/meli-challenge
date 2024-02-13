import threading
from time import sleep
from prediction_queue import PredictionQueue  # Asume que esta clase ya está definida
import joblib
from tensorflow.keras.models import load_model
import numpy as np

# Asegúrate de que BaseModel, SklearnModel, y KerasModel estén definidos como antes
from model import BaseModel, SklearnModel, KerasModel  # Ajusta la importación según sea necesario


class ModelService:
    def __init__(self, model):
        self.queue = PredictionQueue()
        self.model = model
        self.running = True
        self.process_thread = threading.Thread(target=self.process_predictions, daemon=True)
        self.process_thread.start()

    def add_prediction_request(self, data):
        return self.queue.enqueue(data)

    def process_predictions(self):
        while self.running:
            if not self.queue.is_empty():
                data, future = self.queue.dequeue()
                try:
                    # Asume que data ya está en el formato adecuado para el modelo
                    prediction = self.model.predict(data)
                    future.set_result(prediction)
                except Exception as e:
                    future.set_exception(e)
            else:
                sleep(0.1)  # Espera un poco antes de revisar de nuevo la cola

    def stop(self):
        self.running = False
        self.process_thread.join()

# Nota: Asegúrate de adaptar las importaciones y las rutas de los archivos según tu estructura de proyecto.
