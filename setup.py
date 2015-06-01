

from setuptools import setup, find_packages


setup(

    name='tdiff',
    version='0.0.0',
    description='Comparing translations of literary texts.',
    url='https://github.com/davidmcclure/tdiff',
    license='MIT',
    author='David McClure',
    author_email='david@dclure.org',
    scripts=['bin/tdiff'],
    packages=find_packages(),

    install_requires=[
        'textplot',
        'click',
    ]

)
