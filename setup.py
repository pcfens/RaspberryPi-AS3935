from distutils.core import setup

setup(
    name='RPi_AS3935',
    version='0.0.9',
    description='Raspberry Pi <-I2C-> AS3935 lightning sensor communication library',
    author='Phil Fenstermacher',
    author_email='phillip.fenstermacher@gmail.com',
    url='https://github.com/pcfens/RaspberryPi-AS3935',
    packages=['RPi_AS3935'],
    keywords=['RaspberryPi', 'AS3935', 'lightning', 'weather'],
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Utilities',
    ],
)
