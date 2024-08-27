# LDStaleFlags

LDStaleFlags is a Python tool for identifying and managing stale feature flags in LaunchDarkly.

## Prerequisites

- **Python 3.6+**
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

## License

Licensed under the MIT License.
