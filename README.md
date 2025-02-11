
# Car Price Analysis and Prediction
## Overview  

This project analyzes and predicts prices of **Volkswagen Passat B8** cars based on various features.  
It uses data from **Otomoto**, a popular Polish car listing site, and applies **data cleaning, visualization, and machine learning models** to make price predictions.  


## Features  

- **Web Scraping**: Collects car data from Otomoto  
- **Data Cleaning & Processing**: Removes outliers, fills missing values, and standardizes features  
- **Exploratory Data Analysis**: Generates visualizations and a data profiling report  
- **Predictive Modeling**: Compares multiple regression models to predict car prices  



## Instructions

### Installation


To set up the project, install all required dependencies:  

```bash
pip install -r requirements.txt
```  


### Data Processing

#### Steps:
1. Ensure MySQL is installed and running.  
2. Create a `.env` file in the root directory with the following content:  

   ```plaintext
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=YourPasswordHere
   DB_NAME=car_prices
   ```  
3. Configure MySQL connection details in `utils.py`.  
4. Run the data processing script to create the database, clean data, and store it:  

   ```bash
   python main_data_processing.py
   ```  

   This will create a `passats` table in the database with cleaned data.  

### Predictive Modeling

#### Steps:
1. Train and evaluate regression models:  

   ```bash
   python main_training.py
   ```

   This will generate results comparing the performance of various predictive models.

### Data Scraping

#### Steps:
1. Scrape car listing URLs:  

   ```bash
   python otomoto_category_scraper.py
   ```

2. Scrape detailed car data and upload it to the database:  

   ```bash
   python otomoto_car_page_scraper.py
   ```

   This will populate the database with car listings.  

## File Descriptions  

### Data Processing  
- `cleaning_correcting.py` – Functions for data cleaning, removing outliers, and correcting missing values.  
- **`main_data_processing.py`** – Creates the database, loads data from `passats_raw.csv`, and cleans it.  

### Web Scraping  
- **`otomoto_category_scraper.py`** – Scrapes car listing URLs from Otomoto.  
- **`otomoto_car_page_scraper.py`** – Extracts car details from scraped URLs and saves them to the database.  

### Machine Learning  
- **`main_training.py`** – Trains and evaluates different regression models.  

### Utilities & Reports  
- **`profiling.py`** – Generates a **data profiling report**.  
- **`visualization.py`** – Creates **plots and charts** for data analysis.  
- **`utils.py`** – Database connection and helper functions.  

### Data Files  
- **`passats.csv`** – Cleaned dataset used for model training.  
- **`passats_raw.csv`** – Raw data before preprocessing.  


## Detailed Information
For experiment details and conclusions, see the [Report](raport.pdf).  

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


