from setuptools import setup

setup(
    name='InterWorkshop',
    version='1.0.0.dev1',
    packages=['gmad', 'workshop'],
    url='doctor-internet.dev',
    license='MIT',
    author='John Internet',
    author_email='jonjon1234.github@gmail.com',
    description='A Python binding for the Steam Workshop API',
    install_requires=[
        'certifi==2019.6.16',
        'chardet==3.0.4',
        'discord-webhook==0.4.1',
        'environs==5.2.1',
        'idna==2.8',
        'marshmallow==2.20.1',
        'protobuf==3.18.3',
        'python-dotenv==0.10.3',
        'requests==2.22.0',
        'six==1.12.0',
        'urllib3==1.26.5'
    ]
)
