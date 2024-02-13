import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import unicodedata
from sklearn.preprocessing import MultiLabelBinarizer

class DataPreprocessor:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.stemmer = SnowballStemmer('spanish')
        self.stop_words = set(stopwords.words('spanish'))

    def clean_text(self, text):
        if not text:
            return ""
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.stemmer.stem(word) for word in tokens]
        return ' '.join(tokens)

    def preprocess_json(self, json_data):
        df = pd.DataFrame([json_data])
        
        # Eliminar columnas no deseadas
        columns_to_delete = ['differential_pricing', 'subtitle', 'catalog_product_id', 
                             'original_price', 'official_store_id', 'video_id', 'seller_address', 
                             'shipping', 'site_id', 'parent_item_id', 'category_id', 'id', 
                             'currency_id', 'listing_source', 'international_delivery_mode', 
                             'thumbnail', 'secure_thumbnail', 'permalink', 'sub_status', 
                             'deal_ids', 'variations', 'attributes', 'coverage_areas', 'tags', 
                             'descriptions', 'pictures', 'base_price', 'seller_id', 
                             'accepts_mercadopago', 'automatic_relist']
        df.drop(columns=columns_to_delete, axis=1, inplace=True)
        
        # Limpieza y preprocesamiento del texto
        df['title_clean'] = df['title'].apply(self.clean_text)
        df['warranty_clean'] = df.get('warranty', "").apply(self.clean_text)
        
        # One-Hot Encoding para variables categóricas
        # for column in ['shipping_mode', 'listing_type_id', 'buying_mode', 'status']:
        for column in ['listing_type_id', 'buying_mode', 'status']:
            dummies = pd.get_dummies(df[column], prefix=column)
            df = pd.concat([df, dummies], axis=1)
        
        # Codificación de columnas multilabel
        mlb = MultiLabelBinarizer()
        df['non_mercado_pago_payment_methods_categorical'] = df['non_mercado_pago_payment_methods'].apply(
            lambda x: [item.get('description') for item in x] if isinstance(x, list) else [])
        encoded_data = mlb.fit_transform(df['non_mercado_pago_payment_methods_categorical'])
        new_column_names = [f"payment_methods_{c}" for c in mlb.classes_]
        encoded_df = pd.DataFrame(encoded_data, columns=new_column_names, index=df.index)
        df = pd.concat([df, encoded_df], axis=1)
        
        # Extracción de año y mes
        df['last_updated_year'] = pd.to_datetime(df['last_updated']).dt.year
        df['last_updated_month'] = pd.to_datetime(df['last_updated']).dt.month
        df['date_created_year'] = pd.to_datetime(df['date_created']).dt.year
        df['date_created_month'] = pd.to_datetime(df['date_created']).dt.month
        
        # Cálculo de la diferencia de duración
        df['diff_start_time_stop_time'] = (pd.to_datetime(df['stop_time']) - pd.to_datetime(df['start_time'])).dt.days
        
        # Mantener solo las columnas deseadas para la predicción
        desired_columns = ['title_clean', 'warranty_clean'] + [col for col in df.columns if col.startswith('payment_methods_') or col.startswith('shipping_mode_') or col.startswith('listing_type_id_') or col.startswith('buying_mode_') or col.startswith('status_') or col.endswith('_year') or col.endswith('_month') or col == 'diff_start_time_stop_time' or col in ['price', 'initial_quantity', 'sold_quantity', 'available_quantity']]
        
        df_final = df[desired_columns].copy()

        review_cols = ['shipping_mode_custom', 'shipping_mode_me1', 'shipping_mode_me2', 'shipping_mode_not_specified', 'listing_type_id_free', 'listing_type_id_gold', 'listing_type_id_gold_premium', 'listing_type_id_gold_pro', 'listing_type_id_gold_special', 'listing_type_id_silver', 'buying_mode_auction', 'buying_mode_classified', 'status_closed', 'status_not_yet_active', 'status_paused', 'payment_methods_American Express', 'payment_methods_Cheque certificado', 'payment_methods_Contra reembolso', 'payment_methods_Diners', 'payment_methods_Giro postal', 'payment_methods_MasterCard', 'payment_methods_Mastercard Maestro', 'payment_methods_MercadoPago', 'payment_methods_Tarjeta de crédito', 'payment_methods_Visa', 'payment_methods_Visa Electron']

        for col in review_cols:
            if col not in df.columns:
                df_final[col] = 0    
        
        return df_final
