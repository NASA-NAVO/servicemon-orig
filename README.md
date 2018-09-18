# servicemon
Support for monitoring services.
# Setup
To create a development environment, either:
```bash
conda create -n servicemon_env python=3.6 astropy cython matplotlib requests notebook
conda activate servicemon_env
conda install -c astropy astroquery
```
or
```bash
conda env create -f servicemon_env.yml
conda activate servicemon_env
```
then
```bash
# do local (develop) install
pip install .
```
# Testing
To run the tests:
```bash
python setup.py test
```

