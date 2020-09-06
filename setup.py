import setuptools


setuptools.setup(
    name="pyawair-jwoglom",
    version="0.0.1",
    author="jwoglom forked from harperreed",
    description="A very simple python class to access the (private) awair api",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jwoglom/pyawair",
    packages=['pyawair'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
