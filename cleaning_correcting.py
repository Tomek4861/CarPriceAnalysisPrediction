import random

from pandas import DataFrame

from utils import DBConnector, SEED



def assign_missing_origins(df: DataFrame):
    # fill out missing origins with weighted random choice of foreign origins
    def random_foreign_origin():
        return random.choices(countries, probabilities)[0]

    # Filter out 'Polska' and 'Unknown' origins
    foreign_origins = df[(df['origin'] != 'Polska') & (df['origin'] != 'Unknown')]['origin'].value_counts(
        normalize=True)
    print(foreign_origins)

    # Get countries and their probabilities
    countries = foreign_origins.index.tolist()
    probabilities = foreign_origins.values.tolist()

    df['origin'] = df['origin'].apply(lambda x: random_foreign_origin() if x == 'Unknown' else x)

    return df


def correct_engine_capacities_all(df: DataFrame):
    def correct_engine_capacities_record(record):
        valid_engine_capacities = {
            "Petrol": [1395, 1498, 1798, 1984], "Diesel": [1598, 1968]
        }
        fuel_type = record['fuel_type']
        if record['engine_capacity'] not in valid_engine_capacities[fuel_type]:
            # find closest valid engine capacity
            closest = min(valid_engine_capacities[fuel_type], key=lambda x: abs(x - record['engine_capacity']))
            old_value = record['engine_capacity']
            record['engine_capacity'] = closest
            print(f"Corrected {fuel_type} engine capacity from {old_value} to {closest} {record['id']}")
        return record

    return df.apply(correct_engine_capacities_record, axis=1)


def correct_engine_powers_all(df: DataFrame):
    def correct_engine_powers_record(record):
        valid_engine_powers = [280, 272, 240, 220, 200, 190, 180, 150, 125, 122, 120]
        if record['engine_power'] not in valid_engine_powers:
            closest = min(valid_engine_powers, key=lambda x: abs(x - record['engine_power']))
            old_value = record['engine_power']
            record['engine_power'] = closest
            print(f"Corrected engine power from {old_value} to {closest} for record {record['id']}")
        return record

    return df.apply(correct_engine_powers_record, axis=1)


def remove_outliers(df: DataFrame):
    initial_count = df.shape[0]
    df = df[(df['price'] >= 30000) & (df['price'] <= 160000)]
    df = df[(df['year'] >= 2014) & (df['year'] <= 2023)]
    df = df[(df['mileage'] >= 10000) & (df['mileage'] <= 400000)]
    df = df[(df['engine_capacity'] >= 1300) & (df['engine_capacity'] <= 2001)]

    df = df[(df['engine_power'] >= 120) & (df['engine_power'] <= 280)]
    print(f"Removed {initial_count - df.shape[0]} outliers")
    return df


if __name__ == '__main__':
    db_connector = DBConnector()
    db_connector.connect()
    df = db_connector.fetch_data("SELECT * FROM passats")
    df = remove_outliers(df)
    df = assign_missing_origins(df)
    df = correct_engine_capacities_all(df)
    df = correct_engine_powers_all(df)
    db_connector.update_table_from_df(df, 'passats')
    db_connector.close()
