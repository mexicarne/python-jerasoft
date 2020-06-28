from setuptools import setup, find_packages

description="Jerasoft VCS API wrapper"

setup(
    name="python-jerasoft",
    version="1.0",
    description=description,
    author="Ruslan Makhmatkhanov",
    author_email="rm@FreeBSD.org",
    url="https://github.com/mexicarne/python-jerasoft",
    packages=find_packages(),
    install_requires=["requests"],
    license="BSD",
    long_description=description,
    platforms=["any"],
)
