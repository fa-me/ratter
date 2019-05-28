from setuptools import setup
import ratter


with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name=ratter.__name__,
    version=ratter.__version__,
    author=ratter.__author__,
    author_email=ratter.__email__,
    description=ratter.__summary__,
    url=ratter.__url__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only'
    ],
    long_description=readme,
    long_description_content_type='text/markdown'
)
