#!python3

from distutils.core import setup


setup( name='gaffer', 
    version='0.0.11', 
    author='Jean-Pierre Gygax',
    author_email='gygax@practicomp.ch',
    scripts=['gaffer.py'],
    packages=['lib'],
    entry_points= {
        'console_scripts': [
            'gaffer = gaffer.py:main'
            ]
        },
    install_requires= ['GitPython']
    )