"""
ProductGuard AI - Unified CLI Runner.
Launch FastAPI backend or Streamlit Auditor Dashboard with a single command.
"""
import sys
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

    if args.service == "dashboard":
        print("Starting ProductGuard AI Streamlit Auditor Dashboard on http://localhost:8501 ...")
        cmd = [python_exe, "-m", "streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.headless=true"]
        subprocess.run(cmd)

    elif args.service == "api":
        print("Starting ProductGuard AI FastAPI backend on http://localhost:8000 (Docs at /docs) ...")
        cmd = [python_exe, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        subprocess.run(cmd)

    elif args.service == "test":
        print("Running ProductGuard AI test suite with pytest...")
        cmd = [python_exe, "-m", "pytest", "tests/", "-v"]
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
