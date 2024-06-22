# Thredup ETL Pipeline
This project involves creating a robust system to scrape data from an ecommerce website https://www.thredup.com/, process it for quality, and integrate it into a mobile application for efficient searching. It utilizes various technologies such as Python for web scraping, Pandas for data preprocessing, Algolia for indexing and search capabilities, Google Cloud Firestore for data storage, and Google Cloud Run with Kubernetes for deployment and orchestration.

## Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)


## Architecture
![diagram-export-6-22-2024-9_25_25-PM](https://github.com/faisal-fida/ETL-Pipeline-ThredUp-using-Algolia-and-Firestore/assets/69955157/7d2dade5-65ea-486c-acb1-c337663ef26c)




## Project Structure

The project repository contains the following directories and files:

- `data_processing/`: Contains scripts related to data processing and cleaning.
- `handle_database/`: Includes code for handling the product database and storage.
- `output/`: Stores output files generated during the data processing pipeline.
- `.dockerignore`: Specifies files and directories to be ignored when building and deploying Docker images.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `Dockerfile`: Defines the instructions to build a Docker image for this project.
- `Initial_Products_Scraper.ipynb`: Jupyter Notebook file containing the initial product scraping code.
- `Pipfile` and `Pipfile.lock`: Dependency files for the project.
- `main.py`: Main script for the project.
- `readme.md`: This README file.
- `requirements.txt`: Specifies the required Python packages for the project.
- `run_image.py`: Script to run the Docker image.
- `scraping_list_product_modules.py`: Contains modules for scraping product listings.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/faisal-fida/thredup-Scraper
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
