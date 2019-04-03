import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='scavenger',
    version='0.0.1',
    author='gults',
    author_email='bh.gulats@gmail.com',
    description='a google play store scavenger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiodns',
        'aiohttp',
        'beautifulsoup4',
        'cchardet',
        'dataclasses-json',
        'motor',
        'play-scraper',
        'pydash'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=[
        'faker',
        'nose'
    ],
)