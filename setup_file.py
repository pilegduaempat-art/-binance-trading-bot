"""
Setup configuration for Binance Trading Bot
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='binance-trading-bot',
    version='1.0.0',
    description='Advanced Multi-Strategy Trading Bot for Binance Futures',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/binance-trading-bot',
    license='MIT',
    
    packages=find_packages(),
    include_package_data=True,
    
    install_requires=read_requirements(),
    
    python_requires='>=3.8',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    
    keywords='binance trading bot cryptocurrency futures technical-analysis machine-learning',
    
    project_urls={
        'Documentation': 'https://github.com/yourusername/binance-trading-bot/blob/main/README.md',
        'Source': 'https://github.com/yourusername/binance-trading-bot',
        'Tracker': 'https://github.com/yourusername/binance-trading-bot/issues',
    },
    
    entry_points={
        'console_scripts': [
            'trading-bot=app:main',
        ],
    },
)
