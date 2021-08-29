from distutils.core import setup

setup(
    name='PassDecoder',
    version='',
    packages=[''],
    url='',
    license='',
    author='TwoDotSlashPass',
    author_email='',
    description='',
    python_requires='>=3.7, <4',
    install_requires=['base45', 'cbor2', 'pillow', 'pyzbar', 'cose', 'cryptojwt', 'pyasn1'],
    scripts=['PassDecoder'],
)