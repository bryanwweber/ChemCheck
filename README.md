# ChemCheck

This project creates a web-based application to visualize and diagnose errors in the conversion of CHEMKIN files to Cantera input files.
ChemCheck is developed in Django 2.2 and python 3.6, and it allows users edit and convert files on the website. The current version can
report error messages and codes around the error line when conversion fails. In this moment, we have not covered enough conversion errors.

Next Step: we will test different error files reported in Cantera users group to provide more error diagnosis.

### Initital setup

Initial setup, installing dependencies using conda:

    $ conda create -n chemcheck python=3.8 
    $ conda install -c conda-forge django\>=2.2.2 ruamel.yaml numpy
    $ conda activate chemcheck
    $ cd ChemCheck

Initial setup, installing dependencies using `pipenv`:

    $ pipenv install
    $ pipenv shell
    $ cd ChemCheck

Using pip:

    $ pip install -r requirements.txt
    $ cd ChemCheck

### Updates

First run or every time someone changes the models:

    $ python manage.py makemigrations
    $ python manage.py migrate

### Running

To launch the server:

    $ python manage.py runserver

then point a browser at http://127.0.0.1:8000/upload/
