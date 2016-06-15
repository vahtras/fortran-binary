from setuptools import setup

setup(
    name="fortran-binary",
    author="Olav Vahtras",
    author_email="olav.vahtras@gmail.com",
    version="1.0",
    url="https://github.com/vahtras/fortran-binary",
    py_modules=["unformatted"],
    scripts=["fb.py"],
    install_requires=["numpy"],
)
