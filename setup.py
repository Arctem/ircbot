from setuptools import setup

import ircbot

setup(name='ircbot',
    version='0.3',
    description='A simple library for making IRC bots.',
    url='http://github.com/Arctem/ircbot/',
    author='Russell White',
    author_email='rarctem@gmail.com',
    packages=['ircbot'],
    zip_safe=False,
    install_requires=['circuits', 'colorama', 'sqlalchemy'],
)
