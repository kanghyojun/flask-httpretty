from setuptools import setup, find_packages


def readme():
    with open('./README.rst') as f:
        return f.read()


tests_require = [
    'pytest',
    'flake8',
]

setup(
    name='Flask-httpretty',
    version='1.3.0',
    url='http://github.com/admire93/flask-httpretty',
    license='BSD',
    author='Hyojun Kang',
    author_email='hyojun@admire.kr',
    description='flask-httpretty help you to mock http requests via flask.',
    long_description=readme(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'httpretty',
    ],
    extras_require={
        'tests': tests_require,
    },
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
