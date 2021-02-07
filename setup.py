from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


with open('requirements/base.txt') as f:
    requirements = f.read().splitlines()
    requirements = [x for x in requirements if x]


with open('requirements/test.txt') as f:
    test_requirements = f.read().splitlines()
    test_requirements = [x for x in test_requirements if x]


setup(
    name="headbot",
    url="https://github.com/headbot/headbot-python/",
    version="0.2.1",
    description=("python client for the headbot.io API"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ruslan Ksalov",
    author_email="rksalov@gmail.com",
    license="Apache 2",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.6,<=3.9",
    install_requires=requirements,
    tests_require=test_requirements,
    setup_requires=["pytest-runner"],
    packages=find_packages(exclude=["tests"]),
)
