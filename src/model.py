from joblib import load

from sklearn.preprocessing import FunctionTransformer
        

def bool_to_int(x):
    return x.astype(int)
# Definir una función de identidad para usar con FunctionTransformer
def identity_function(X):
    return X    


class BaseModel:
    def predict(self, data):
        raise NotImplementedError

class SklearnModel(BaseModel):
    def __init__(self, model_path):
        self.model = load(model_path)

    def predict(self, data):
        return self.model.predict(data)

class KerasModel(BaseModel):
    def __init__(self, model_path):
        self.model = load_model(model_path)
        preprocessor= self.model.named_steps['preprocessor']

        # O si quieres acceder por nombre y el nombre es 'num' para el StandardScaler
        new_transformers = []
        for (name, func, cols) in preprocessor.transformers:
            if name == 'bool':
                func = FunctionTransformer(bool_to_int)
            if name == 'bool_as_int' or name == 'date_as_int':
                func = FunctionTransformer(identity_function)
            
            new_transformers.append((
                name,
                FunctionTransformer(bool_to_int),
                cols
            ))
            
        self.model.named_steps['preprocessor'] = new_transformers

    def predict(self, data):
        return np.round(self.model.predict(data)).flatten()
