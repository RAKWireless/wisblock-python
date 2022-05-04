from setuptools import find_packages, setup

setup(
    name='pi4ioesv96224',
    packages=find_packages(include=['pì4ioesv96224']),
    version='0.1.0',
    description='PI4IOE5V96224 GPIO Expander Library',
    author='xose.perez@rakwireless.com',
    license='MIT',
    install_requires=['smbus2==0.4.1']
)