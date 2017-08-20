#!python3

from distutils.core import setup


setup( name='butler', 
    version='0.0.11', 
    author='Jean-Pierre Gygax',
    author_email='gygax@practicomp.ch',
    scripts=['butler.py'],
    packages=['lib'],
    entry_points= {
        'console_scripts': [
            'butler = butler.py:main'
            ]
        },
    install_requires= ['GitPython']
    )