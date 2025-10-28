from setuptools import setup, find_packages

setup(
    name='sankey-interactive',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for generating complex, interactive Sankey diagrams with features like time series visualization and adjustable metrics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sankey-interactive',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'plotly',
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)