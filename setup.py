from setuptools import setup, find_packages

setup(
    name="Meet N' Eat",
    version="1.0",
    description="REST API backend for a social application "
                "for meeting people based on their food interests",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.12.2',
        "Flask-Restful>=0.3.6"
    ]
)

