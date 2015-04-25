from setuptools import setup, find_packages


def readme():
    with open('./README.md') as f:
        return f.read()


setup(
    name='Flask-httpretty',
    version='1.2.0',
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
