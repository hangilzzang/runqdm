from setuptools import setup, find_packages

setup(
    name="runqdm",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        'runqdm': ['running_man_frame/*.txt'],
    },
    include_package_data=True,
    install_requires=[],
    author="hangil",
    description="A running progress bar package",
    python_requires=">=3.6",
) 