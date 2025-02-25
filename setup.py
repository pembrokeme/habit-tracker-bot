from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="habit-tracker-bot",
    version="1.0.0",
    author="pembrokeme",
    author_email="plmlmrdt6337@hotmail.com",
    description="A Telegram bot for tracking daily habits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pembrokeme/habit-tracker-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "habit-tracker-bot=bot:main",
        ],
    },
)