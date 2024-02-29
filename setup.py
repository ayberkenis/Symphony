from setuptools import setup, find_packages

setup(
    name='web-symphony',
    version='0.0.2',
    packages=find_packages(),
    author="ayberkenis",
    author_email="ayberkenis@gmail.com",
    description="A quick REST API framework with microservice architecture.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    
    ],
    python_requires='>=3.9',
    repository="web-symphony",
    install_requires=[
        "colored==2.2.4",
    ],
    
)