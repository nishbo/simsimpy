from setuptools import setup, find_packages

readme = open('README.txt').read()
setup(name='simsimpy',
      version='0.2.5',
      description='Collection of functions for simple simulation.',
      long_description=readme,
      url='https://github.com/nishbo/simsimpy',
      author='nishbo',
      author_email='nishbo@yandex.ru',
      license='Apache 2.0',
      packages=find_packages(),
      zip_safe=True)
