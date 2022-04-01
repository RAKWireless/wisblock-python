import setuptools

setuptools.setup(
	name='mq2',
    version='0.1.0',
    description='MQ2 Library',
    author='xikai',
    author_email='kai.xi@rakwireless.com',
    license='MIT',
	packages=setuptools.find_packages(include=['mq2']),
    install_requires=['smbus-cffi==0.5.1']
)
