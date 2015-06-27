# Automatically created by: scrapy deploy

from setuptools import setup, find_packages

setup(
    name         = 'metasearch',
    version      = '0.0.1',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = crawl.settings']},
)
