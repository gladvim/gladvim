from setuptools import setup, find_packages

setup(
    name='gladvim-plugin-manager',
    version='0.1.0',
    author='Viktor A. Rozenko Voitenko',
    author_email='sharp.vik@gmail.com',
    description='GladVim is a lightweight and simple plugin manager for Vim.',
    url='https://github.com/gladvim/gladvim',
    license='MPL-2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'colorama',
        'termcolor',
    ],
    entry_points="""
        [console_scripts]
        gladvim=gladvim.cli:cli
    """,
)
