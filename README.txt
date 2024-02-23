py -m venv drink_env

drink_env\Scripts\activate.bat
-or- (for unix)
source drink_env/bin/activate

pip install -r requirements
py data_setup.py
flask run
deactivate