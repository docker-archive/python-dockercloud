import codecs
import os
import re

from setuptools import setup, find_packages

requirements =[
    "future >= 0.15.0, < 1",
    "requests >= 2.5.2, < 3",
    "six >= 1.3.0, < 2",
    "websocket-client >= 0.32.0, < 1"
]


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

with open('./test-requirements.txt') as test_reqs_txt:
    test_requirements = [line for line in test_reqs_txt]


setup(
        name="python-dockercloud",
        version=find_version('dockercloud', '__init__.py'),
        packages=find_packages(),
        install_requires=requirements,
        tests_require=test_requirements,
        provides=['docker'],
        include_package_data=True,
        author="Docker, Inc.",
        author_email="info@docker.com",
        description="Python Library for Dockercloud",
        license="Apache v2",
        keywords="docker cloud",
        url="http://cloud.docker.com/",
        test_suite="tests",
)
