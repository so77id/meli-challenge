from flask import Flask, request
from flask_restx import Api, Resource, fields
import argparse
from model_service import ModelService
from data_preprocessor import DataPreprocessor
from joblib import load

app = Flask(__name__)
api = Api(app, version='1.0', title='Prediction API',
          description='A simple Prediction API')

# Argumentos de línea de comando
parser = argparse.ArgumentParser(description='Flask app running with custom host and port')
parser.add_argument('--host', type=str, default='127.0.0.1', help='Host for the Flask app')
parser.add_argument('--port', type=int, default=5000, help='Port for the Flask app')
args = parser.parse_args()

# Define el modelo de tu entrada esperada usando el modelado de Flask-RESTX
input_model = api.model('InputData', {
    'seller_address': fields.Nested(api.model('SellerAddress', {
        'country': fields.Nested(api.model('Country', {
            'name': fields.String,
            'id': fields.String
        })),
        'state': fields.Nested(api.model('State', {
            'name': fields.String,
            'id': fields.String
        })),
        'city': fields.Nested(api.model('City', {
            'name': fields.String,
            'id': fields.String
        }))
    })),
    'warranty': fields.String,
    # Continúa definiendo el resto de los campos de tu JSON aquí...
    'base_price': fields.Float,
    'shipping': fields.Nested(api.model('Shipping', {
        # Define los campos anidados aquí
    })),
    # Asegúrate de incluir todos los campos necesarios...
})


def bool_to_int(x):
    return x.astype(int)
# Definir una función de identidad para usar con FunctionTransformer
def identity_function(X):
    return X

# Asegúrate de tener esta clase definida correctamente
data_preprocessor = DataPreprocessor()
model = load('./models/RandomForestClassifier-model__n_estimators:200.joblib')
model_service = ModelService(model)

@api.route('/predict')
class Predict(Resource):
    @api.expect(input_model)  # Usar el modelo definido para la entrada
    def post(self):
        # Obtén el JSON de entrada de la solicitud
        json_data = request.json

        # Usa el DataPreprocessor para transformar el JSON en un DataFrame listo para el modelo
        df_ready_for_prediction = data_preprocessor.preprocess_json(json_data)

        # Ahora, usa el DataFrame procesado para hacer una predicción
        future = model_service.add_prediction_request(df_ready_for_prediction)

        # Espera el resultado de manera bloqueante
        prediction = future.result()  # Esto bloqueará hasta que el resultado esté disponible

        # Devuelve la predicción como respuesta JSON
        return {'prediction': prediction.tolist()}

if __name__ == '__main__':
    app.run(debug=True, host=args.host, port=args.port)
