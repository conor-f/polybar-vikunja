from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = [
    'requests',
]

setup(
    name='polybar-vikunja',
    description='Vikunja plugin for Polybar',
    version='0.2.0',
    url='https://github.com/conor-f/polybar-vikunja',
    python_requires='>=3.6',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'polybar-vikunja = polybar_vikunja.client:main'
        ]
    }
)
