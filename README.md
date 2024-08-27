# LDStaleFlags

LDStaleFlags is a Python tool for identifying and managing stale feature flags in LaunchDarkly.

## Prerequisites

- **Python**
- **Git**
- **LaunchDarkly API token**

## Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/LDStaleFlags.git
   cd LDStaleFlags
   ```

2. **Set up the environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On macOS/Linux
   # .\venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Create a `.env` file:
    ```plaintext
    LD_API_TOKEN=your-api-token
    LD_PROJECT_KEY=your-project-key
    LD_ENVIRONMENT_KEY=production
    ```

## Usage

Run the script to identify stale flags:

```bash
python get_stale_flags.py
```

## Disclaimer

This code is provided on an as-is basis and is not officially supported by LaunchDarkly. Use at your own discretion.

## License

This project is licensed under the Apache License, Version 2.0. See the LICENSE.txt file for details.