sudo python3 setup.py develop
sphinx-apidoc -l -f -M -e -o docs/source/generated uitdatabank uitdatabank/tests/
cd docs
make html
