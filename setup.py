from setuptools import setup, find_packages


setup(
    name="ehr-library",                   
    version="0.1.0",                     
    author="Wendrew Oliveira",                   
    author_email="about.wendrew@gmail.com",
    description="A library like the others. ENJOY!!!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ONEMANCOMPANY/ehr",  
    packages=find_packages(),  
    license="The Freedom Reciprocal License (FRL)",          
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: FreedomForge",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",             
    install_requires=[
        "ipython>=8.29.0",
        "setuptools>=75.6.0",
        "urllib3>=2.2.3",
        "wheel>=0.45.1",                  
    ],
)
