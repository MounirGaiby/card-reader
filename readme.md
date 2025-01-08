# Badge Reader Application

A simple GUI application for reading RFID/NFC card UIDs with support for both big-endian and little-endian formats.

## Features
- Real-time card detection
- Display of card UID in both big-endian and little-endian formats
- One-click copying of UIDs
- Auto-reconnection to reader
- Clean and simple user interface

## Requirements
- Windows OS
- PC/SC-compatible card reader
- Python 3.12+ (for development)

## Installation

### Using the Executable
1. Download the latest release from the `dist/BadgeReader` folder
2. Run `BadgeReader.exe`
3. Ensure your card reader is connected

### For Development
1. Clone the repository
```bash
git clone https://github.com/yourusername/card-reader.git
cd card-reader