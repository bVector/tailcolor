from setuptools import setup

setup(name='tailcolor',
    version='0.1a',
    description="'tail -F' with color feedback based on how recent the line was seen",
    url='https://github.com/bVector/tailcolor',
    author='bVector',
    author_email='b@bvector.net',
    license='MIT',
    packages=['tailcolor'],
    scripts=['bin/tailcolor'],
    install_requires=[
        'blessings',
        'fabulous'
    ],
    zip_safe=False)

