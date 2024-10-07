from setuptools import setup, find_packages

setup(
    name='scholtrack',
    version='0.1.0',
    description='Effortlessly gather, trace, and manage citations for academic papers.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/sergeyprokudin/scholtrack',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'scholtrack=scholtrack.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

