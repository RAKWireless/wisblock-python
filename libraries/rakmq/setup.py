import setuptools

setuptools.setup(
	name='rakmq',
    version='0.1.0',
    description='RAKwireless MQx Library',
    author='xikai',
    author_email='kai.xi@rakwireless.com',
    license='MIT',
	packages=setuptools.find_packages(include=['mqx']),
    install_requires=['smbus-cffi==0.5.1']
)
