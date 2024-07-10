import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import DBConnector

db_connector = DBConnector()
db_connector.connect()


def plot_price_distribution():
    df = db_connector.fetch_data("SELECT price FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=20, color='blue')
    plt.title('Price Distribution', size=20)
    plt.xlabel('Price [PLN]')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/price_distribution.png')
    plt.show()


def plot_year_distribution():
    df = db_connector.fetch_data("SELECT year FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='year', palette='viridis')
    plt.title('Production Year Distribution', size=20)
    plt.xlabel('Year')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/year_distribution.png')
    plt.show()


def plot_mileage_distribution():
    df = db_connector.fetch_data("SELECT mileage FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['mileage'], bins=20, color='green')
    plt.title('Car Mileage Distribution', size=20)
    plt.xlabel('Mileage [km]')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/mileage_distribution.png')
    plt.show()


def plot_engine_capacity_distribution():
    df = db_connector.fetch_data("SELECT engine_capacity FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['engine_capacity'], bins=20, color='red')
    plt.title('Engine Capacity Distribution', size=20)
    plt.xlabel('Engine Capacity [cm³]')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/engine_capacity_distribution.png')
    plt.show()


def plot_engine_power_distribution():
    df = db_connector.fetch_data("SELECT engine_power FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['engine_power'], bins=20, color='purple')
    plt.title('Engine Power Distribution', size=20)
    plt.xlabel('Engine Power [Hp]')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/engine_power_distribution.png')
    plt.show()


def plot_fuel_type_distribution():
    df = db_connector.fetch_data("SELECT fuel_type FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='fuel_type', palette='muted')
    plt.title('Fuel Type Distribution', size=20)
    plt.xlabel('Fuel Type')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/fuel_type_distribution.png')
    plt.show()


def plot_transmission_distribution():
    df = db_connector.fetch_data("SELECT transmission FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='transmission', palette='pastel')
    plt.title('Transmission Distribution', size=20)
    plt.xlabel('Transmission')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/transmission_distribution.png')
    plt.show()


def plot_accident_free_distribution():
    df = db_connector.fetch_data("SELECT accident_free FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='accident_free', palette='Set1')
    plt.title('Accident Free Distribution', size=20)
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.xlabel('Accident Free')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/accident_free_distribution.png')
    plt.show()


def plot_origin_distribution():
    df = db_connector.fetch_data("SELECT origin FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='origin', palette='deep')
    plt.title('Origin Distribution', size=20)
    plt.xlabel('Number of Cars')
    plt.ylabel('Origin')
    plt.savefig('Graphs/origin_distribution.png')
    plt.show()


def plot_four_wheel_drive_distribution():
    df = db_connector.fetch_data("SELECT four_wheel_drive FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='four_wheel_drive', palette='cubehelix')
    plt.title('Four Wheel Drive Distribution', size=20)
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.xlabel('Four Wheel Drive')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/four_wheel_drive_distribution.png')
    plt.show()


def plot_invoice_vat_distribution():
    df = db_connector.fetch_data("SELECT invoice_vat FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='invoice_vat', palette='coolwarm')
    plt.title('Invoice VAT Distribution', size=20)
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.xlabel('Invoice VAT')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/invoice_vat_distribution.png')
    plt.show()


def plot_estate_distribution():
    df = db_connector.fetch_data("SELECT estate FROM passats")
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='estate', palette='autumn')
    plt.title('Body Type Distribution', size=20)
    plt.xticks([0, 1], ['Sedan', 'Estate'])
    plt.xlabel('Body Type')
    plt.ylabel('Number of Cars')
    plt.savefig('Graphs/estate_distribution.png')
    plt.show()


def plot_correlation_matrix():
    df = db_connector.fetch_data("SELECT year, mileage, engine_capacity, engine_power, price FROM passats")
    correlation_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation of Variables')
    plt.savefig('Graphs/correlation_matrix.png')
    plt.show()


def plot_predictions_multiple_models(models_dict: dict[str, pd.DataFrame]):
    plt.figure(figsize=(10, 6))

    for model_name, df in models_dict.items():
        plt.scatter(df['Predicted'], df['Actual'], alpha=0.77, edgecolors='w', label=f'{model_name} - Predicted')

    all_actuals = pd.concat([df['Actual'] for df in models_dict.values()])
    plt.plot([all_actuals.min(), all_actuals.max()], [all_actuals.min(), all_actuals.max()], color='red',
             linestyle='--', lw=2, label='Ideal Line')

    plt.title('Actual vs. Predicted Prices for Multiple Models')
    plt.xlabel('Predicted Prices')
    plt.ylabel('Actual Prices')
    plt.legend()
    plt.grid(True)
    plt.show()


def show_all_plots():
    plot_correlation_matrix()
    plot_price_distribution()
    plot_year_distribution()
    plot_mileage_distribution()
    plot_engine_capacity_distribution()
    plot_engine_power_distribution()
    plot_fuel_type_distribution()
    plot_transmission_distribution()
    plot_accident_free_distribution()
    plot_origin_distribution()
    plot_four_wheel_drive_distribution()
    plot_invoice_vat_distribution()
    plot_estate_distribution()
    db_connector.close()
