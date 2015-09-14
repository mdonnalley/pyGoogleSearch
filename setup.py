from distutils.core import setup

setup(
    name='pyGoogleSearch',
    version='1.0.1',
    packages=['pyGoogleSearch'],
    url='https://github.com/mdonnalley/pyGoogleSearch',
    license='',
    author='donnalley',
    author_email='michael.donnalley@gmail.com',
    description='Package for collecting and aggregating data from various Google sources (Web, News, and Scholar)',
    install_requries=["requests", "bs4"]
)
