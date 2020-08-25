"""
Flask-Saved
-------------

This is the description for that library
"""
from setuptools import setup
import os
import flask_softdeletes

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-SoftDeletes',
    version=flask_softdeletes.__version__,
    url='',
    license='MIT',
    author='renjianguo',
    author_email='renjianguo@kanhebei.cn',
    description='基于flask-sqlalchemy的软删除实现',
    long_description=long_description,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=1.1.2', 'Flask-SQLAlchemy>=2.4.4'
    ],
    packages=['flask_softdeletes'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)