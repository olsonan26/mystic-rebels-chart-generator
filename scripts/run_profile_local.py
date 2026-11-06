"""Run the existing protected API locally using an installed astronomy runtime."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api.index:app', host='127.0.0.1', port=8000, access_log=False)
