# Product Search Database

![diagram-export-6-22-2024-9_25_25-PM](https://github.com/faisal-fida/ETL-Pipeline-ThredUp-using-Algolia-and-Firestore/assets/69955157/7d2dade5-65ea-486c-acb1-c337663ef26c)



## Table of Contents

- [Description](#description)
- [Project Structure](#project-structure)
- [Installation](#installation)

## Description

The **Product Search Database** is a data processing and scraping project aimed at creating a database of product listings for efficient search and retrieval. The project utilizes web scraping techniques to extract product data from an external website.

### Docker Integration
Docker is utilized to containerize the ETL pipeline and ensure consistent and reliable execution across different environments. The Dockerfile included in the repository defines the necessary configuration for 
building the Docker image. The .dockerignore file specifies which files and directories should be excluded during the Docker image build process. The run_image.py script can be used to run the Docker image once it is built.

### ETL Pipeline
The ETL pipeline consists of several components, including data processing, database handling, and Algolia database integration. The main.py script serves as the entry point for the pipeline and orchestrates the execution of various modules and scripts within the project. The data_processing directory contains scripts responsible for data processing and cleaning, while the handle_database directory includes scripts for handling the database and data uploading.

### Algolia Database Integration
The agolio_upload.py script is responsible for uploading data to the Algolia search database. This integration enables efficient and optimized search functionality for the product search database.

### Flutter Front-End
Although not included in this repository, the project also involves a front-end implementation using Flutter for the creation of a user-friendly interface to interact with the product search database.

Please note that this repository may include additional files and directories not listed here, but they may be specific to the project's implementation.

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
