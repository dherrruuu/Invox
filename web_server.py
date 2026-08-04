"""INVOX Web Server — entry point."""
from __future__ import annotations

import sys
from pathlib import Path

# Make src/invox importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
