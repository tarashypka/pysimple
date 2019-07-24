from setuptools import setup, find_packages


setup(
    name='pysimple',
    version='1.0.0',
    description='Utils functions to be used in other projects',
    url='',
    author='Taras Shypka',
    author_email='tarashypka@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False)
