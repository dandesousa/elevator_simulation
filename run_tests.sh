#!/bin/sh

if [ ! -d env ]
then
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
fi
source env/bin/activate
python -m unittest discover tests
