#!/usr/bin/python

from setuptools import setup

setup(name="pasaqrcode",
      version="1.0",
      package_dir={"pasaqrcode": "."},
      packages=["pasaqrcode"],
      include_package_data=True,
      package_data={"pasaqrcode": ["pasa_logo.png"]},
      install_requires=[
          "PyQt5",
          "pyqrcode",
          "Pillow"
      ],
      author="UCalgary PASA",
      author_email="physastr@ucalgary.ca",
      url="https://pasa.website"
     )