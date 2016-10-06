from setuptools import setup
from fortran_binary import __version__

setup(
    name="fortran-binary",
    author="Olav Vahtras",
    author_email="olav.vahtras@gmail.com",
    version=__version__,
    url="https://github.com/vahtras/fortran-binary",
    py_modules=["fortran_binary"],
    scripts=["forbin"],
    install_requires=["numpy"],
)
