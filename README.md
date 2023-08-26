# PASA QR Code Generator

This project is the official QR code formatter app for the University of Calgary's Physics and Astronomy Student Association.

# Installation

Minimum Python version: 3.6 (detected by [vermin](https://github.com/netromdk/vermin))

To install, run the following command:

`pip install git+https://github.com/UCalgaryPASA/pasaqrcode.git`

All dependencies should be installed automatically.

This project is platform-independent.

# Usage

To launch the app, run the following command:

`python -m pasaqrcode`

To generate a QR code, enter a URL in the space provided and tweak the following settings as necessary:
- Additional Complexity: increases the size of the pattern
- Scale Factor: number of pixels per dot in the code
- Logo Vertical Padding: number of pixels to add around the logo as empty space

Click the 'Generate QR Code' button to display a preview of the code, then click 'Save Image' to save it to any desired location on your computer.
