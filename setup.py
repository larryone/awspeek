from setuptools import setup, find_packages
read_file = lambda x: [l.strip() for l in open(x).readlines()]

setup(
    name='awspeek',
    author='Piotr Szymanski',
    author_email='piotr.szymanski@fieldaware.com',
    url='https://github.com/eddwardo/awspeek',
    license='MIT',
    version='0.0.1',
    description='Boto wrapper for checking what is happening on AWS',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=read_file('requirements.txt'),
    include_package_data=True,
    entry_points={
        'console_scripts': ['awspeek=awspeek.cli:cli'],
    }
)
