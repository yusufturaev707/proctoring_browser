# SafeBrowser

**Online Test Proctoring System with Face ID**

SafeBrowser - bu online testlar uchun proctoring tizimi. Face ID texnologiyasi yordamida talabgorlarni aniqlash va test jarayonida monitoring qilish imkoniyatini beradi.

## Features

- **Face ID Authentication** - InsightFace asosida yuzni aniqlash va tasdiqlash
- **Real-time Monitoring** - Test vaqtida yuzni doimiy tekshirish
- **Anti-Cheating** - Qo'shimcha monitorlarni aniqlash
- **Screen Recording** - Ekranni yozib olish
- **Modern UI** - Material Design asosida zamonaviy interfeys
- **GPU Support** - NVIDIA CUDA, AMD DirectML, Intel OpenVINO

## Installation

### From PyPI

```bash
pip install safebrowser
```

### From Source

```bash
git clone https://github.com/safebrowser/safebrowser.git
cd safebrowser
pip install -e .
```

### Requirements

- Python 3.10+
- Windows 10/11
- Webcam

## Quick Start

```bash
# After installation
safebrowser

# Or run directly
python -m safebrowser

# Or from source
python run.py
```

## Configuration

Configuration file: `config/config.ini`

```ini
[AUTH]
admin_password = your_password

[API]
base_url = http://your-server/api/v1
timeout = 15

[FACE_RECOGNITION]
detection_size = 640
similarity_threshold = 40
check_interval = 10

[CAMERA]
width = 640
height = 480
fps = 30
```

## GPU Support

For NVIDIA GPU acceleration:

```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/
```

## Project Structure

```
safebrowser/
├── src/safebrowser/
│   ├── core/           # Face recognition logic
│   ├── ui/             # User interface
│   ├── services/       # API client
│   ├── workers/        # Background threads
│   └── utils/          # Utilities
├── config/             # Configuration
├── tests/              # Unit tests
└── pyproject.toml      # Project config
```

## License

MIT License

## Author

SafeBrowser Team
