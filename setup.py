try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name = 'django-toplevel-files',
    version = '0.1',
    packages = find_packages(),
    install_requires = [],
    url = 'https://github.com/mikek/django-toplevel-files',
    author='Mikhail Kolesnik',
    author_email='mike@openbunker.org',
)
