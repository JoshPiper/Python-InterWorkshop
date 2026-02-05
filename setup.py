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
        'certifi==2024.7.4',
        'chardet==3.0.4',
        'discord-webhook==0.4.1',
        'environs==5.2.1',
        'idna==3.7',
        'marshmallow==2.20.1',
        'protobuf==5.29.6',
        'python-dotenv==0.10.3',
        'requests==2.32.4',
        'six==1.12.0',
        'urllib3==1.26.19'
    ]
)
