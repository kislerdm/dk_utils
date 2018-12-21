from setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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
        'inspect',
        'requests',
        'inspect'
    ],
    include_package_data=True,
    zip_safe=False)
