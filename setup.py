from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gamefusion',  
    version='0.1',
    author='Laurin Fäller',
    author_email='laurin@faeller.me',
    description='A tool to recommend multiplayer games by blending Steam libraries',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/faeller/gamefusion',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'openai>=0.27.0',
        'requests>=2.25.1'
    ],
    entry_points={
        'console_scripts': [
            'gamefusion=gamefusion:main',
        ],
    },
)
