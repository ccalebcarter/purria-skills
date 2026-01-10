#!/usr/bin/env python3
"""
Purria Starter - Asset Pipeline Tester
Tests the full Gemini → Recraft → SVG pipeline.
"""
import os
import sys
import tempfile
import subprocess
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def check_mark():
    return f"{GREEN}✓{RESET}"


def x_mark():
    return f"{RED}✗{RESET}"


def header(text):
    print(f"\n{BOLD}{BLUE}{text}{RESET}")
    print("-" * 40)


def get_skills_dir():
    """Get the Claude skills directory."""
    return Path.home() / ".claude" / "skills"


def get_python_exe():
    """Get the Python executable in the gemini venv."""
    skills_dir = get_skills_dir()
    venv_python = skills_dir / "gemini-image-generator" / "scripts" / "venv"

    if sys.platform == "win32":
        return venv_python / "Scripts" / "python.exe"
    else:
        return venv_python / "bin" / "python"


def run_script(script_path, args, description):
    """Run a Python script and return success status."""
    python_exe = get_python_exe()

    if not python_exe.exists():
        print(f"  {x_mark()} Python venv not found: {python_exe}")
        return False

    cmd = [str(python_exe), str(script_path)] + args

    print(f"  Running: {description}...")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ}
        )

        if result.returncode == 0:
            print(f"  {check_mark()} {description}")
            return True
        else:
            print(f"  {x_mark()} {description}")
            print(f"    Error: {result.stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  {x_mark()} {description} (timeout)")
        return False
    except Exception as e:
        print(f"  {x_mark()} {description} ({e})")
        return False


def main():
    print(f"\n{BOLD}Purria Starter - Asset Pipeline Test{RESET}")
    print("=" * 40)

    # Check API keys
    header("Checking API Keys")

    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    recraft_key = os.environ.get("RECRAFT_API_KEY", "")

    if not gemini_key:
        print(f"  {x_mark()} GEMINI_API_KEY not set")
        print("    Set with: export GEMINI_API_KEY='your-key'")
        return 1
    print(f"  {check_mark()} GEMINI_API_KEY ({len(gemini_key)} chars)")

    if not recraft_key:
        print(f"  {x_mark()} RECRAFT_API_KEY not set")
        print("    Set with: export RECRAFT_API_KEY='your-key'")
        return 1
    print(f"  {check_mark()} RECRAFT_API_KEY ({len(recraft_key)} chars)")

    # Setup paths
    skills_dir = get_skills_dir()
    generate_script = skills_dir / "gemini-image-generator" / "scripts" / "generate.py"
    recraft_script = skills_dir / "gemini-image-generator" / "scripts" / "recraft_process.py"

    # Check scripts exist
    header("Checking Scripts")

    if not generate_script.exists():
        print(f"  {x_mark()} generate.py not found")
        return 1
    print(f"  {check_mark()} generate.py")

    if not recraft_script.exists():
        print(f"  {x_mark()} recraft_process.py not found")
        return 1
    print(f"  {check_mark()} recraft_process.py")

    # Create temp directory for test outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        header("Running Pipeline")

        # Step 1: Generate image
        output_png = tmpdir / "test-asset.png"
        success = run_script(
            generate_script,
            [
                "--prompt", "A simple cute robot icon, minimal style, solid background",
                "--output", str(output_png)
            ],
            "Step 1: Gemini Generate"
        )

        if not success:
            print(f"\n{RED}Pipeline failed at Step 1{RESET}")
            return 1

        if not output_png.exists():
            print(f"  {x_mark()} Output file not created")
            return 1

        size_kb = output_png.stat().st_size / 1024
        print(f"    Output: {size_kb:.0f} KB")

        # Step 2: Remove background
        output_nobg = tmpdir / "test-asset-nobg.png"
        success = run_script(
            recraft_script,
            [
                "--action", "remove-bg",
                "--input", str(output_png),
                "--output", str(output_nobg)
            ],
            "Step 2: Recraft Remove BG"
        )

        if not success:
            print(f"\n{RED}Pipeline failed at Step 2{RESET}")
            return 1

        if not output_nobg.exists():
            print(f"  {x_mark()} Output file not created")
            return 1

        size_kb = output_nobg.stat().st_size / 1024
        print(f"    Output: {size_kb:.0f} KB")

        # Step 3: Vectorize
        output_svg = tmpdir / "test-asset.svg"
        success = run_script(
            recraft_script,
            [
                "--action", "vectorize",
                "--input", str(output_nobg),
                "--output", str(output_svg)
            ],
            "Step 3: Recraft Vectorize"
        )

        if not success:
            print(f"\n{RED}Pipeline failed at Step 3{RESET}")
            return 1

        if not output_svg.exists():
            print(f"  {x_mark()} Output file not created")
            return 1

        size_kb = output_svg.stat().st_size / 1024
        print(f"    Output: {size_kb:.0f} KB")

    # Summary
    header("Results")
    print(f"  {GREEN}{BOLD}Asset pipeline test passed!{RESET}")
    print(f"\n  Pipeline: Gemini → Recraft BG → Recraft SVG")
    print(f"  All three steps completed successfully.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
