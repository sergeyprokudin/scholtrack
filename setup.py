from setuptools import setup, find_packages

setup(
    name='scholtrack',
    version='0.1.0.1',
    description='Effortlessly gather, trace, and manage citations for academic papers',
    author='Sergey Prokudin',
    author_email='sergey.prokudin@gmail.com',
    url='https://github.com/sergeyprokudin/scholtrack',
    packages=find_packages(),
    include_package_data=True, 
    package_data={
        'scholtrack': ['collections/*.txt'],  
    },
    install_requires=[
        'requests',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
        'scholtrack=scholtrack.cli:main',
        ],
    }
)

