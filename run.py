"""
ProductGuard AI - Unified CLI Runner.
Launch FastAPI backend or Streamlit Auditor Dashboard with a single command.
"""
import sys
import os
import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="ProductGuard AI Runner")
    parser.add_argument(
        "service",
        choices=["dashboard", "api", "test"],
        default="dashboard",
        nargs="?",
        help="Service to launch: 'dashboard' (Streamlit UI), 'api' (FastAPI server), or 'test' (Run test suite)"
    )
    args = parser.parse_args()

    python_exe = sys.executable

    # Dynamic port configuration (essential for Render / Cloud hosting)
    default_port = 8501 if args.service == "dashboard" else 8000
    port = int(os.environ.get("PORT", default_port))

    if args.service == "dashboard":
        print(f"Starting ProductGuard AI Streamlit Auditor Dashboard on port {port} ...")
        cmd = [
            python_exe, "-m", "streamlit", "run", "dashboard/app.py",
            f"--server.port={port}",
            "--server.address=0.0.0.0",
            "--server.headless=true"
        ]
        subprocess.run(cmd)

    elif args.service == "api":
        print(f"Starting ProductGuard AI FastAPI backend on port {port} (Docs at /docs) ...")
        cmd = [
            python_exe, "-m", "uvicorn", "api.main:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ]
        subprocess.run(cmd)

    elif args.service == "test":
        print("Running ProductGuard AI test suite with pytest...")
        cmd = [python_exe, "-m", "pytest", "tests/", "-v"]
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
