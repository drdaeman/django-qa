from setuptools import setup, find_packages

import datetime

d = datetime.datetime.now()
version = '0.0-r{0:0d}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}'.format(\
        d.year, d.month, d.day, d.hour, d.minute, d.second)
# version = "0.0.0"

long_description=""
try:
    long_description=file('README.md').read()
except Exception:
    pass

license=""
try:
    license=file('License.txt').read()
except Exception:
    pass

setup(
    name = 'qa',
    version = version,
    description = 'Simple Q&A',
    author = 'Pablo Saavedra',
    author_email = 'saavedra.pablo@gmail.com',
    url = 'http://github.com/psaavedra/liver',
    download_url= 'https://github.com/psaavedra/Simple-Q-A-App-using-Python-Django/archive/master.zip',
    packages = find_packages(),
    include_package_data=True,
    scripts=[
    ],
    zip_safe=False,
    install_requires=[
        "django-bootstrap3",
        "django-markdown",
        "djangorestframework",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
    license=license,
    keywords = "forum qa django",
)
