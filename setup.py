from pathlib import Path
from setuptools import setup, find_packages

if __name__ == '__main__':
    base_dir = Path(__file__).parent

    about = {}
    with (base_dir / '__about__.py').open() as f:
        exec(f.read(), about)

    install_requirements = [
        'numpy',
        'pandas'
    ]

    setup(
        name=about['__title__'],
        version=about['__version__'],

        author=about["__author__"],
        author_email=about["__email__"],

        include_package_data=True,
        python_requires='>=3.7.0',
        install_requires=install_requirements,
        zip_safe=False,
        entry_points={
            'console_scripts': [
                'trackit=trackit:main',
                'summarize=summarize:main'
            ]
        }
    )
