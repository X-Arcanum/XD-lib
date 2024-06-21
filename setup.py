from setuptools import setup, find_packages

setup(
    name='XD-lib',
    version='0.01',
    packages=find_packages(),
    install_requires=[
        'asyncio',
        'aiohttp',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'XD-lib=Xd-lib.bot:main',
        ],
    },
    url='https://github.com/X-Arcanum/XD-lib',
    author='@Darkee0_0',
    author_email='',
    description='A lightweight Telegram bot client library.',
)
