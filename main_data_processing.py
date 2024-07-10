from cleaning_correcting import remove_outliers, assign_missing_origins, correct_engine_powers_all, \
    correct_engine_capacities_all
from utils import DBConnector
from visualization import show_all_plots
from profiling import do_profiling


def main():
    db_connector = DBConnector(database=None)
    db_connector.connect()
    db_connector.create_database_and_table()
    db_connector.load_from_csv("passats_raw.csv", "passats")
    db_connector.close()
    db_connector = DBConnector()
    db_connector.connect()
    df = db_connector.fetch_data("SELECT * FROM passats")
    df = remove_outliers(df)
    df = assign_missing_origins(df)
    df = correct_engine_capacities_all(df)
    df = correct_engine_powers_all(df)
    db_connector.update_table_from_df(df, 'passats')
    db_connector.save_to_csv("passats", "passats")
    do_profiling()
    show_all_plots()
    db_connector.close()


if __name__ == '__main__':
    main()
