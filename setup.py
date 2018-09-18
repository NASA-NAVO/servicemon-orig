from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='servicemon',
    version='0.1.0',
    description='Support for monitoring web services',
    long_description=readme,
    author='Tom Donaldson',
    author_email='',
    url='https://github.com/NASA-NAVO/servicemon',
    license=license,
    packages=find_packages(exclude=('docs')),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
