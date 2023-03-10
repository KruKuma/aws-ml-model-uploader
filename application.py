import os

import numpy as np
import pandas as pd
import lightgbm as lgb
import pickle

from sklearn.preprocessing import StandardScaler

import utils


class Application:
    def __init__(self):
        project_directory = os.path.dirname(os.path.abspath(__file__))
        dot_env_file_path = os.path.join(project_directory, ".env")
        dot_env_file = utils.DotEnvFile(dot_env_file_path)
        aws_arguments = dot_env_file.load_aws_configurations()
        self._boto3_configuration = utils.Boto3Configuration(aws_arguments["access_id"],
                                                             aws_arguments["secret_key"],
                                                             aws_arguments["region"],
                                                             aws_arguments["bucket_name"])

    @staticmethod
    def load_heart_disease_dataset(url):
        df = pd.read_csv(url, header=None)
        col_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                     'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
        df.columns = col_names

        # Replace '?' values with NaN
        df.replace('?', np.nan, inplace=True)

        # Impute missing values with mean
        for col in df.columns:
            if df[col].dtype == 'float32':
                df[col].fillna(df[col].mean(), inplace=True)

        X = df.drop('target', axis=1)
        y = df['target']
        return X, y

    @staticmethod
    def train_lgbm(X_train, y_train):
        scaler = StandardScaler()

        # Train LightGBM model
        lgb_model = lgb.LGBMRegressor(objective='binary',
                                      num_leaves=31,
                                      learning_rate=0.05,
                                      n_estimators=20)

        X_train = scaler.fit_transform(X_train)
        lgb_model.fit(X_train, y_train)
        return lgb_model, scaler

    @staticmethod
    def save_model_and_scaler(model, scaler, model_path, scaler_path):
        model.booster_.save_model(model_path)
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)

    def upload_files(self):
        self._boto3_configuration.upload_model_files()


def main():
    # Initialize application
    app = Application()

    X, y = app.load_heart_disease_dataset(
        'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data')

    # Train LightGBM model on Amazon Sagemaker
    lgb_model, scaler = app.train_lgbm(X, y)

    # Save the model and scaler to local storage
    app.save_model_and_scaler(lgb_model, scaler, 'model.txt', 'scaler.pkl')

    # Upload the model and scaler to S3
    app.upload_files()


if __name__ == '__main__':
    main()
