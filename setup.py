from setuptools import setup, find_packages

setup(
    name='abtestoo',
    version='0.1',
    description='A/B testing and multi-armed bandit made easy',
    author='Charin Polpanumas',
    author_email='cebril@gmail.com',
    packages=find_packages(),  # same as name
    install_requires=['plotnine', 'numpy', 'pandas'],  # external packages as dependencies
)
