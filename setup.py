from setuptools import setup, find_packages

setup(
    name="harmonix-backend",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "pydub>=0.25.1",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "mypy",
        ]
    },
    entry_points={
        "console_scripts": [
            "harmonix-cli=backend.main:main",
        ],
    },
)
