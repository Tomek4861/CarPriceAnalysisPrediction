
# Car Price Analysis and Prediction
## Introduction

This project involves analyzing and predicting the prices of Volkswagen Passat B8 cars based on various features. The data is gathered from Otomoto, a popular car listing site in Poland. The analysis includes data cleaning, correction, visualization, and predictive modeling.


## Table of Contents
1. [Introduction](#introduction)
2. [Instructions](#instructions)
   - [Installation](#installation)
   - [Data Processing](#data-processing)
   - [Predictive Modeling](#predictive-modeling)
   - [Data Scraping](#data-scraping)
3. [File Descriptions](#file-descriptions)
4. [Detailed Information](#detailed-information)
5. [License](#license)



## Instructions

### Installation

To set up the project, you need to install all the required dependencies. You can do this by running:

```bash
pip install -r requirements.txt
```

### Data Processing

#### Steps:
1. Ensure you have MySQL installed and running on your device.
2. Set up the MySQL connection details in the `utils.py` file.
3. Run the data processing script to create the database and table, and load the raw data:

   ```bash
   python main_data_processing.py
   ```

   This will create a table `passats` in the database with cleaned and corrected data.

### Predictive Modeling

#### Steps:
1. Run the training script to train and evaluate different regression models:

   ```bash
   python main_training.py
   ```

   This will generate results comparing the performance of various predictive models.

### Data Scraping

#### Steps:
1. Run the category scraper to gather links to car listings:

   ```bash
   python otomoto_category_scraper.py
   ```

2. Run the car page scraper to scrape car details from the gathered links and upload them to the database:

   ```bash
   python otomoto_car_page_scraper.py
   ```

   This will populate the database with detailed car listings.

## File Descriptions

### `cleaning_correcting.py`
Contains functions for cleaning and correcting car data, such as removing outliers, assigning missing origins, and correcting engine capacities and powers.

### `main_data_processing.py`
Creates the MySQL database and `passats` table, uploads data from `passats_raw.csv`, and performs a series of data cleaning and correction operations to update the table contents.

### `otomoto_category_scraper.py`
Fetches links to car listings from Otomoto categories and saves them to a file.

### `otomoto_car_page_scraper.py`
Scrapes car listing details from links in `urls.txt` and uploads them to the database.

### `passats.csv`
CSV file containing data on Volkswagen Passat B8 cars used for analysis and model training.

### `passats_data_profiling_report.html`
Contains a detailed data profiling report generated by ydata_profiling for Volkswagen Passat cars.

### `passats_raw.csv`
Contains raw data on Volkswagen Passat cars collected before data cleaning and correction.

### `profiling.py`
Script used to generate the ydata_profiling report.

### `training_best.py`
Script for training and evaluating different regression models, comparing their performance.

### `utils.py`
Contains utility functions for managing the MySQL database, including the `DBConnector` class for handling connections, inserts, fetches, and backups.

### `visualization.py`
Contains functions for generating plots from car data, including distributions of prices, years, mileages, technical parameters, and a correlation matrix.

### `README.md`
This file, containing the project description and instructions.

## Detailed Information
For detailed experiment procedures and conclusions, refer to the `raport.pdf` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


