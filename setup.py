from setuptools import setup, find_packages


setup(
    name='pysimple',
    version='1.0.1',
    description='Utils functions to be used in other projects',
    url='',
    author='Taras Shypka',
    author_email='tarashypka@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False)
