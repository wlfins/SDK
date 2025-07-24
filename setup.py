from setuptools import setup, find_packages

setup(
    name='wlfins_sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'web3',
    ],
    author='WLFINS',
    author_email='wlfins@proton.me',
    description='A Python SDK for WLFI Name Service API and Smart Contracts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wlfins/SDK',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
