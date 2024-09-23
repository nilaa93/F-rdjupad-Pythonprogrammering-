# Fördjupad-Pythonprogrammering-

# Data Processing Application

This project is a Python application that fetches data from an API, processes it, and updates a SQL database. It includes features such as data validation, duplicate checking, error logging, and automated testing. 

## Features

- **Fetch Data**: Retrieves data from the JSONPlaceholder API.
- **Data Processing**: Cleans and formats data for consistency.
- **Data Validation**: Ensures the correctness of data before database insertion.
- **Duplicate Check**: Prevents duplicate entries in the database.
- **Error Logging**: Logs errors to a file for easier troubleshooting.
- **Automated Testing**: Includes unit tests to ensure functionality.

## Getting Started

### Prerequisites

- Python 3.x
- Required libraries:
  - `requests`
  - `pyodbc`
  - `unittest`

You can install the required libraries using pip:

```bash
pip install requests pyodbc


# H1 Database Setup using SQL
CREATE TABLE todos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(255),
    completed BIT
);

## H2 Running application in the terminal
python process_data.py

## H2 Running tests to execute the tests defined in the test_process_data.py
python test_process_data.py
