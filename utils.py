import os
import random
import time

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from mysql.connector import Error

SEED = 36
random.seed(SEED)

# database data

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


####

def write_url_to_file(urls, failed=False):
    filename = "failed_urls.txt" if failed else "urls.txt"
    with open(filename, "a+", encoding='utf-8') as f:
        f.write("\n".join(urls) + "\n")


class DBConnector:
    def __init__(self, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                                      database=self.database)
            self.cursor = self.connection.cursor()
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def insert_car(self, car):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO passats (
                id, price, year, mileage, engine_capacity, engine_power,
                fuel_type, transmission, accident_free, origin, four_wheel_drive,
                invoice_vat, estate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                car.id, car.price, car.year, car.mileage, car.engine_capacity, car.engine_power, car.fuel_type,
                car.transmission, car.accident_free, car.origin, car.four_wheel_drive, car.invoice_vat, car.estate))
            self.connection.commit()
            print(f"Car with id {car.id} inserted successfully")
        except Error as e:
            print(f"Error while inserting car: {e}")

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def fetch_data(self, query):
        try:
            df = pd.read_sql(query, self.connection)
            self.connection.commit()
            return df
        except Error as e:
            print(f"Error while fetching data: {e}")
            return None

    def create_database_and_table(self):
        try:
            query = """
            CREATE DATABASE IF NOT EXISTS car_prices;
            USE car_prices;
            CREATE TABLE IF NOT EXISTS passats (
                id VARCHAR(255) PRIMARY KEY,
                price INT NOT NULL,
                year INT NOT NULL,
                mileage INT NOT NULL,
                engine_capacity INT NOT NULL,
                engine_power INT NOT NULL,
                fuel_type ENUM('Diesel', 'Petrol') NOT NULL,
                transmission ENUM('Automatic', 'Manual') NOT NULL,
                accident_free BOOLEAN NOT NULL,
                origin VARCHAR(50) NOT NULL,
                four_wheel_drive BOOLEAN NOT NULL,
                invoice_vat BOOLEAN NOT NULL,
                estate BOOLEAN NOT NULL
            );
            """
            for result in self.cursor.execute(query, multi=True):
                if result.with_rows:
                    print(f"Rows produced by statement '{result.statement}':")
                    print(result.fetchall())
                else:
                    print(f"Number of rows affected by statement '{result.statement}': {result.rowcount}")
            self.connection.commit()
            print("Database and table created successfully")
        except Error as e:
            print(f"Error while creating database and table: {e}")

    def create_backup(self):
        try:
            # day hour min for table name
            day_hour_min = time.strftime("%d%H%M")

            backup_query = f"CREATE TABLE passats_backup{day_hour_min} AS SELECT * FROM passats;"
            self.cursor.execute(backup_query)
            self.connection.commit()
            print("Backup of table passats created successfully")
        except Error as e:
            print(f"Error while creating backup of table passats: {e}")

    def update_table_from_df(self, df, table_name):
        try:
            # Delete all records from the table
            delete_query = f"DELETE FROM {table_name};"
            self.cursor.execute(delete_query)
            self.connection.commit()

            # Insert new records from the DataFrame
            for _, row in df.iterrows():
                insert_query = f"""
                INSERT INTO {table_name} (
                    id, price, year, mileage, engine_capacity, engine_power,
                    fuel_type, transmission, accident_free, origin, four_wheel_drive,
                    invoice_vat, estate
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(insert_query, (
                    row['id'], row['price'], row['year'], row['mileage'], row['engine_capacity'], row['engine_power'],
                    row['fuel_type'], row['transmission'], row['accident_free'], row['origin'], row['four_wheel_drive'],
                    row['invoice_vat'], row['estate']))
            self.connection.commit()
            print("Table updated successfully from DataFrame")
        except Error as e:
            print(f"Error while updating table from DataFrame: {e}")

    def save_to_csv(self, table_name, file_name=None):
        file_name = file_name or table_name
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.connection)
            # fix boolean columns
            bool_columns = ['accident_free', 'four_wheel_drive', 'invoice_vat', 'estate']
            for col in bool_columns:
                df[col] = df[col].astype('bool')
            df.to_csv(f"{file_name}.csv", index=False)
            print(f"Data from table {table_name} saved to {file_name}.csv")
        except Error as e:
            print(f"Error while saving data to CSV: {e}")

    def load_from_csv(self, file_name, table_name):
        try:
            df = pd.read_csv(file_name)
            # clear table
            delete_query = f"DELETE FROM {table_name};"
            self.cursor.execute(delete_query)
            self.connection.commit()

            # insert data from csv
            for _, row in df.iterrows():
                insert_query = f"""
                INSERT INTO {table_name} (
                    id, price, year, mileage, engine_capacity, engine_power,
                    fuel_type, transmission, accident_free, origin, four_wheel_drive,
                    invoice_vat, estate
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(insert_query, (
                    row['id'], row['price'], row['year'], row['mileage'], row['engine_capacity'], row['engine_power'],
                    row['fuel_type'], row['transmission'], row['accident_free'], row['origin'], row['four_wheel_drive'],
                    row['invoice_vat'], row['estate']))
            self.connection.commit()
            print(f"Data from {file_name} loaded into table {table_name} successfully")
        except Error as e:
            print(f"Error while loading data from CSV to table: {e}")

# #
# if __name__ == '__main__':
#     db_connector = DBConnector()
#     db_connector.connect()
#     db_connector.create_backup()
#     db_connector.close()
