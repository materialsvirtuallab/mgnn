from setuptools import find_packages, setup
import numpy

VERSION = "0.1.0.dev"

setup(
    name="mgnn",
    version=VERSION,
    author="Tsz Wai Ko, Marcel Nassar, Ji Qi, Santiago Miret, Shyue Ping Ong",
    author_email="ongsp@eng.ucsd.edu",
    maintainer="Shyue Ping Ong",
    maintainer_email="ongsp@eng.ucsd.edu",
    description="MGNN is a reimplementation of MatErials Graph Network (MEGNet) and Materials 3-body Graph Networks "
    "(M3GNet) in Deep Graph Library (DGL).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=[
        "materials",
        "interatomic potential",
        "force field",
        "science",
        "property prediction",
        "AI",
        "machine learning",
        "graph",
        "deep learning",
    ],
    packages=find_packages(),
    package_data={
        "mgnn": ["*.json", "*.md"],
        "mgnn.utils": ["*.npy"],
    },
    include_package_data=True,
    install_requires=(
        "torch",
        "dgl",
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_dirs=[numpy.get_include()],
)
