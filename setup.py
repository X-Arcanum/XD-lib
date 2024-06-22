from setuptools import setup, find_packages

setup(
    name='XD-lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'XD=XD:main',
        ],
    },
    url='https://github.com/X-Arcanum/XD-lib',
    author='@Darkee0_0',
    author_email='youremail@example.com',  # Replace with your email address
    description='A lightweight Telegram bot client library.',
)
