#!/usr/bin/env python3
"""
Purria Starter - Setup Validator
Validates that all prerequisites and configuration are correct.
"""
import os
import subprocess
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def check_mark():
    return f"{GREEN}[OK]{RESET}"


def x_mark():
    return f"{RED}[FAIL]{RESET}"


def warn_mark():
    return f"{YELLOW}[WARN]{RESET}"


def header(text):
    print(f"\n{BOLD}{BLUE}{'='*50}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*50}{RESET}\n")


def check_command(name, cmd, min_version=None):
    """Check if a command exists and optionally verify version."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        version = result.stdout.strip() or result.stderr.strip()
        version = version.split('\n')[0]  # First line only
        print(f"  {check_mark()} {name}: {version}")
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"  {x_mark()} {name}: Not found or error")
        return False


def check_env_var(name, min_length=10):
    """Check if an environment variable is set."""
    value = os.environ.get(name, "")
    if value and len(value) >= min_length:
        print(f"  {check_mark()} {name}: Set ({len(value)} chars)")
        return True
    elif value:
        print(f"  {warn_mark()} {name}: Set but short ({len(value)} chars)")
        return False
    else:
        print(f"  {x_mark()} {name}: Not set")
        return False


def check_file(path, description):
    """Check if a file exists."""
    if Path(path).exists():
        print(f"  {check_mark()} {description}: {path}")
        return True
    else:
        print(f"  {x_mark()} {description}: Not found")
        return False


def check_dir(path, description):
    """Check if a directory exists."""
    if Path(path).is_dir():
        print(f"  {check_mark()} {description}: {path}")
        return True
    else:
        print(f"  {x_mark()} {description}: Not found")
        return False


def main():
    print(f"\n{BOLD}Purria Starter - Setup Validator{RESET}")
    print("=" * 40)

    results = {"passed": 0, "failed": 0, "warnings": 0}

    # Phase 1: Prerequisites
    header("Phase 1: Prerequisites")
    prereqs = [
        ("Bun", "bun --version"),
        ("Node.js", "node --version"),
        ("Python", "python --version"),
        ("Git", "git --version"),
    ]
    for name, cmd in prereqs:
        if check_command(name, cmd):
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Phase 2: API Keys
    header("Phase 2: API Keys")
    api_keys = [
        ("GEMINI_API_KEY", 30),
        ("RECRAFT_API_KEY", 30),
    ]
    for name, min_len in api_keys:
        if check_env_var(name, min_len):
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Phase 3: Project Files (if in project directory)
    header("Phase 3: Project Structure")
    cwd = Path.cwd()

    # Check if we're in a Purria project
    if (cwd / "CLAUDE.md").exists() or (cwd / "turbo.json").exists():
        project_files = [
            ("CLAUDE.md", "Project instructions"),
            ("turbo.json", "Turborepo config"),
            ("package.json", "Root package.json"),
            ("apps/web/package.json", "Web app"),
            ("apps/server/package.json", "Server app"),
            ("packages/db/package.json", "Database package"),
            ("packages/api/package.json", "API package"),
        ]
        for path, desc in project_files:
            if check_file(cwd / path, desc):
                results["passed"] += 1
            else:
                results["failed"] += 1

        # Check env files
        header("Phase 4: Environment Files")
        env_files = [
            ("apps/server/.env", "Server environment"),
            ("apps/web/.env", "Web environment"),
        ]
        for path, desc in env_files:
            if check_file(cwd / path, desc):
                results["passed"] += 1
            else:
                results["warnings"] += 1
                print(f"    Create with: cp {path}.example {path}")
    else:
        print(f"  {warn_mark()} Not in a Purria project directory")
        print(f"    Current: {cwd}")
        results["warnings"] += 1

    # Phase 5: Skills
    header("Phase 5: Skills Installation")
    skills_dir = Path.home() / ".claude" / "skills"
    skills = [
        ("gemini-image-generator", "AI image generation"),
        ("purria-starter", "Project setup (this skill)"),
    ]
    for skill, desc in skills:
        skill_path = skills_dir / skill / "SKILL.md"
        if check_file(skill_path, f"{skill} ({desc})"):
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Check gemini venv
    venv_path = skills_dir / "gemini-image-generator" / "scripts" / "venv"
    if check_dir(venv_path, "Gemini Python venv"):
        results["passed"] += 1
    else:
        results["warnings"] += 1
        print(f"    Setup with: python -m venv {venv_path}")

    # Summary
    header("Summary")
    total = results["passed"] + results["failed"] + results["warnings"]
    print(f"  {GREEN}Passed:{RESET}   {results['passed']}/{total}")
    print(f"  {RED}Failed:{RESET}   {results['failed']}/{total}")
    print(f"  {YELLOW}Warnings:{RESET} {results['warnings']}/{total}")

    if results["failed"] == 0:
        print(f"\n{GREEN}{BOLD}Setup validation passed!{RESET}")
        return 0
    else:
        print(f"\n{RED}{BOLD}Setup incomplete - fix failed checks above{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
