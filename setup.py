from setuptools import setup

setup(
    name="GamePile API CLI Tool",
    version="1.0",
    description="The API Tool for GamePile, a University Major Project.",
    author="Kal Sandbrook (kas143)",
    author_email="kas143@aber.ac.uk",
    packages=['GamePile-API'],
    install_requires=['requests','thefuzz','pyinstaller']
)
