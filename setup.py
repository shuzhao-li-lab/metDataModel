from setuptools import setup, find_packages

with open("metDataModel/__init__.py") as f:
    exec([x for x in f.readlines() if '__version__' in x][0])

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    name='metDataModel',
    version=__version__,
    author="Shuzhao Li",
    author_email='shuzhao.li@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Data models for metabolomics",
    install_requires=requirements,
    license="BSD license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='metDataModel',
    
    packages=find_packages(
        include=['*', "metDataModel"],
    ),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shuzhao-li/metDataModel',

    zip_safe=False,
)
