# Drink
Patron alcohol consumptiopn task

# Web App Setup Guide

This guide outlines the steps required to set up and run the web app

## Setting up the Virtual Environment

### Windows
py -m venv drink_env
drink_env\Scripts\activate.bat

### Unix/Mac
python3 -m venv drink_env
source drink_env/bin/activate

## Installing Requirements
pip install -r requirements.txt

## Running the Project
py data_setup.py
flask run

## Deactivating the Virtual Environment
deactivate

Make sure to activate the virtual environment before installing the requirements and running the project. After you're done working on the project, deactivate the virtual environment.
