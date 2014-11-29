from setuptools import setup, find_packages


setup(
    name='Flask-httpretty',
    version='1.1',
    url='http://github.com/admire93/flask-httpretty',
    license='BSD',
    author='Hyojun Kang',
    author_email='hyojun@admire.kr',
    description='my description',
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
