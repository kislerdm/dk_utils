import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='dk_utils',
    version='0.1',
    description='Utils function for private project of Dmitry Kisler',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='utils modules python',
    url='https://www.dkisler.de',
    author='Dmitry Kisler',
    author_email='admin@dkisler.de',
    license='MIT',
    packages=['dk_utils'],
    install_requires=[
        'pandas',
        'numpy',
        'kafka',
        'psycopg2',
        'requests',
        'logging',
        'shapely',
        'Geohash'
    ],
    include_package_data=True,
    zip_safe=False)
