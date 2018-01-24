from distutils.core import setup

setup(
    name='Scrapify',
    packages=['Scrapify'],
    version='5.3',
    description='A simple and intuitive library that allows dead easy web scraping with 3 lines of code.',
    author='David Mellul',
    author_email='david.mellul@outlook.fr',
    url='https://github.com/DavidMellul/Scrapify',
    license='MIT',
    download_url='https://github.com/davidmellul/Scrapify/archive/5.2.tar.gz',
    install_requires=[
        'unidecode', 'requests', 'lxml'
    ],
    keywords=['networking', 'web', 'scraping', 'data', 'retrieval']
)
