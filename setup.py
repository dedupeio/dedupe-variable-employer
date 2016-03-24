try:
    from setuptools import setup, Extension
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    name='dedupe-variable-employer',
    url='https://github.com/datamade/dedupe-variables-employer',
    version='0.0.4',
    description='Employer variable type for dedupe',
    packages=['dedupe.variables'],
    install_requires=['companyparser==0.2',
                      'parseratorvariable >= 0.0.14',
                      'simplecosine'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php'
    )
