import setuptools

setuptools.setup(
	name='ADC121C021',
    version='0.1.0',
    description='ADC121C021 Library',
    author='kai.xi@rakwireless.com',
    license='MIT',
	packages=setuptools.find_packages(include=['adc121c021']),
    install_requires=['smbus-cffi==0.5.1']
)
