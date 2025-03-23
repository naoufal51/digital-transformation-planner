from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="digital-transformation-planner",
    version="0.1.0",
    author="Digital Transformation Team",
    author_email="your.email@example.com",
    description="AI-powered application for generating comprehensive digital transformation plans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/digital-transformation-planner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Business :: Planning",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "digital-transformation-planner=digital_transformation.app:main",
        ],
    },
) 