from setuptools import setup, find_packages

readme = open('README.txt').read()
setup(name='simsimpy',
      version='0.1.1.2',
      description='Simple simulator of biological neural networks.',
      long_description=readme,
      url='https://github.com/nishbo/simsimpy',
      author='nishbo',
      author_email='nishbo@yandex.ru',
      license='GNU GPL',
      packages=find_packages(),
      zip_safe=False)
