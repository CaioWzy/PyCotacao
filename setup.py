import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("pycotacao/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="pycotacao",
    version=version,
    url="https://github.com/CaioWzy/PyCotacao",
    project_urls={
        "Code": "https://github.com/CaioWzy/PyCotacao",
        "Issue tracker": "https://github.com/CaioWzy/PyCotacao/issues",
    },
    license="MIT",
    author="CaioWzy",
    author_email="mail@caiowzy.dev",
    maintainer="CaioWzy",
    maintainer_email="mail@caiowzy.dev",
    description="Wrapper API for X-Rates from Banco Central.",
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.6.*",
    install_requires=[
        "python-dateutil==2.8.1",
    ],
)