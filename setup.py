"""

see https://docs.micropython.org/en/latest/reference/packages.html
"""
import sys
import setuptools
import sdist_upip

with open("README.md", "r") as fh:
    long_description = fh.read()

print("setuptools va inclure les paquets %s" % [ setuptools.find_packages() ], file=sys.stderr)


name = "micropython-ADCOverUDP"
version = "0.3"

setuptools.setup(
    name=name,
    version=version,
    author="la Fleur",
    author_email="lafleur@boum.org",
    license="GNUv3",
    #description=long_description[:long_description.find("\n")]
    description="Send signals read from ADC over UDP broadcast (and use them).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lafleurdeboum/ADCOverUDP",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        #"Platform :: ESP",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "ssd1306",
    ],
    #extras_require={
    #    "OLED printout": "ssd1306",
    #},
    cmdclass={'sdist': sdist_upip.sdist}
)

