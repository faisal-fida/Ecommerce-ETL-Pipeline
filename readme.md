# Ecommerce Mobile Search Pipeline
In this project, I developed a robust system to scrape data from an ecommerce website [Thredup](https://www.thredup.com/), process it for quality, and integrate it into a mobile application for efficient searching. It utilizes various technologies such as Python for web scraping, Pandas for data preprocessing, Algolia for indexing and search capabilities, Google Cloud Firestore for data storage, and Google Cloud Run with Docker for deployment.


## Architecture 🚀



<p align="center">Part 1: Web Scraping Architecture</p>

![1](https://github.com/faisal-fida/Ecommerce-ETL-Pipeline/assets/69955157/911443a0-ed7f-4dbf-8853-7abe35366674)

<p align="center">Part 2: Data Processing and Validation Workflow</p>

![2](https://github.com/faisal-fida/Ecommerce-ETL-Pipeline/assets/69955157/fc4477e8-8dfc-4f10-b18f-d056ec942e93)

<p align="center">Part 3: Data Pipeline Workflow</p>

![3](https://github.com/faisal-fida/Ecommerce-ETL-Pipeline/assets/69955157/38a8b3c2-538c-4afd-8775-b402d38c3d40)


## Project Structure

The project repository contains the following directories and files:

- `data_processing/`: Contains scripts related to data processing and cleaning.
- `handle_database/`: Includes code for handling the product database and storage.
- `output/`: Stores output files generated during the data processing pipeline.
- `Dockerfile`: Defines the instructions to build a Docker image for this project.
- `Initial_Products_Scraper.ipynb`: Jupyter Notebook file containing the initial product scraping code.
- `run_image.py`: Script to run the Docker image on GCP.
- `scraping_list_product_modules.py`: Contains modules for scraping product listings.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/faisal-fida/Ecommerce-ETL-Pipeline
```

2. Install the required Python dependencies using Pipenv:

```
pipenv install
```

3. Set up any necessary configurations and environment variables.

4. Run the main script:
```
python main.py
```
