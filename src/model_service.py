import threading
from time import sleep
from prediction_queue import PredictionQueue  
import joblib
from tensorflow.keras.models import load_model
import numpy as np

from model import BaseModel, SklearnModel, KerasModel 


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
                    prediction = self.model.predict(data)
                    future.set_result(prediction)
                except Exception as e:
                    future.set_exception(e)
            else:
                sleep(0.1)  # Espera un poco antes de revisar de nuevo la cola

    def stop(self):
        self.running = False
        self.process_thread.join()
