import setuptools

with open("README.md", "r", encoding="utf8") as readme:
    description = readme.read()

with open('requirements.txt', "r", encoding="utf8") as requirements:
    requires = requirements.read().splitlines()

setuptools.setup(
    name="CollectorGame",
    version="0.0.1",
    author="Baytekov Nikita",
    author_email="nvbaytekov@gmail.com",
    description="Simple 2D arcade game to help her creator pass the exams",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/bayten/collector-game",
    packages=setuptools.find_packages(),
    package_data={
        'CollectorGame': ['images/*',
                          'FortunataCYR.ttf']
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requires,
    python_requires='>=3.6',
)
