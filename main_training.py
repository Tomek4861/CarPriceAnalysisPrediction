import matplotlib.pyplot as plt
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler
from sklearn.tree import DecisionTreeRegressor

from utils import SEED


class ModelEvaluator:
    def __init__(self, model_type: callable, model_nme: str):
        self.df = pd.read_csv('passats.csv')
        self.train_df, self.test_df = train_test_split(self.df, test_size=0.2, random_state=SEED)
        features = ['year', 'mileage', 'engine_capacity', 'engine_power', 'fuel_type', 'transmission', 'accident_free',
                    'origin', 'four_wheel_drive', 'invoice_vat', 'estate']
        target = 'price'
        self.X_train = self.train_df[features]
        self.y_train = self.train_df[target]
        self.X_test = self.test_df[features]
        self.y_test = self.test_df[target]
        self.model_type = model_type
        self.model = None
        self.model_name = model_nme
        self.results = dict()
        self.comparison_test_df = None

    def preprocess_data(self) -> ColumnTransformer:
        numerical_features = ['year', 'mileage', 'engine_capacity', 'engine_power']
        categorical_features = ['fuel_type', 'transmission', 'accident_free', 'origin', 'four_wheel_drive',
                                'invoice_vat', 'estate']
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')
        # preprocessor = ColumnTransformer(transformers=[('num', 'passthrough', numerical_features),
        #                                                ('cat', categorical_transformer, categorical_features)])
        preprocessor = ColumnTransformer(transformers=[('num', StandardScaler(), numerical_features),
            ('cat', categorical_transformer, categorical_features)])

        return preprocessor

    def build_model(self):
        self.model = Pipeline(steps=[('preprocessor', self.preprocess_data()), ('regressor', self.model_type)])

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)

    def run_prediction_and_get_stats(self) -> dict:
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        mse_train = mean_squared_error(self.y_train, y_train_pred)
        r2_train = r2_score(self.y_train, y_train_pred)
        mse_test = mean_squared_error(self.y_test, y_test_pred)
        mae_test = mean_absolute_error(self.y_test, y_test_pred)
        mae_train = mean_absolute_error(self.y_train, y_train_pred)
        r2_test = r2_score(self.y_test, y_test_pred)
        self.results = dict(mse_train=mse_train, r2_train=r2_train, mse_test=mse_test, r2_test=r2_test, mae=mean_absolute_error,
                            mae_train=mae_train, mae_test=mae_test)
        self.comparison_test_df = pd.DataFrame({'Actual': self.y_test, 'Predicted': y_test_pred})
        return self.results

    def show_results_nicely(self):
        results = self.run_prediction_and_get_stats()
        print(f"Training set Mean Squared Error: {results['mse_train']}")
        print(f"Training set R^2 Score: {results['r2_train']}")
        print(f"Training set Mean Absolute Error: {results['mae_train']}")
        print(f"Test set Mean Squared Error: {results['mse_test']}")
        print(f"Test set R^2 Score: {results['r2_test']}")
        print(f"Test set Mean Absolute Error: {results['mae_test']}")

        print("\nComparison on Training Set:")
        comparison_train = pd.DataFrame({'Actual': self.y_train, 'Predicted': self.model.predict(self.X_train)})
        print(comparison_train.head(10))
        print("\nComparison on Test Set:")
        print(self.comparison_test_df.head(10))

    def get_results(self):
        return self.results.copy()

    def get_comparison_test_df(self):
        return self.comparison_test_df.copy()

    def plot_predictions(self):
        plt.figure(figsize=(10, 6))

        plt.scatter(self.comparison_test_df['Predicted'], self.comparison_test_df['Actual'], alpha=0.6, color='blue',
                    edgecolors='w', label='Predicted')

        # plt.scatter(self.comparison_test_df['Predicted'], self.comparison_test_df['Predicted'], alpha=0.5,
        #             color='green', edgecolors='w', label='Ideal Prediction')
        plt.title(f'{self.model_name} - Actual vs. Predicted Prices')
        plt.xlabel('Predicted Prices')
        plt.ylabel('Actual Prices')
        plt.plot([self.comparison_test_df['Actual'].min(), self.comparison_test_df['Actual'].max()],
                 [self.comparison_test_df['Actual'].min(), self.comparison_test_df['Actual'].max()], color='red',
                 linestyle='--', lw=2, label='Ideal Line')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"GraphsModels/{self.model_name.replace(' ', '_')}.png")
        plt.show()


def run_comparison():
    models = {
        #  Linear
        'Linear Regression': LinearRegression(), 'Ridge Regression': Ridge(),
        # Polynomial Regression
        # using ridge because LinearRegression() gave awful resutls
        'Polynomial Regression D2': make_pipeline(PolynomialFeatures(degree=2), Ridge()),
        'Polynomial Regression D3': make_pipeline(PolynomialFeatures(degree=3), Ridge()),

        # Tree-based models
        'Decision Tree': DecisionTreeRegressor(random_state=SEED),
        'Random Forest': RandomForestRegressor(random_state=SEED),

        # Other
        'CatBoost': CatBoostRegressor(random_state=SEED, verbose=0, iterations=800),

    }

    results_dict = dict()

    for model_name, model in models.items():
        print(f"\nModel: {model_name}")
        prediction = ModelEvaluator(model_type=model, model_nme=model_name)
        prediction.build_model()
        prediction.train_model()
        prediction.run_prediction_and_get_stats()
        prediction.show_results_nicely()
        model_dict = dict(results=prediction.get_results(), dataframe=prediction.get_comparison_test_df())
        results_dict[model_name] = model_dict
        prediction.plot_predictions()

        print("-" * 50)

        # print headline
        print(f"{'Model Name':<30}{'MSE Train':<15}{'MAE Train':<15}{'R2 Train':<15}{'MSE Test':<15}{'MAE Test':<15}{'R2 Test':<15}")

    for model_name, model_results in results_dict.items():
        print(
            f"{model_name:<30}{model_results['results']['mse_train']:<15.4f}"
            f"{model_results['results']['mae_train']:<15.2f}"
            f"{model_results['results']['r2_train']:<15.4f}"
            f"{model_results['results']['mse_test']:<15.2f}"
            f"{model_results['results']['mae_test']:<15.2f}"
            f"{model_results['results']['r2_test']:<15.4f}"
        )


if __name__ == '__main__':
    run_comparison()
