#!/usr/bin/env python3
"""
FinAgent Pro - Setup Verification Script
Run this to verify your installation is ready for the hackathon demo
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_status(check, status, message=""):
    icon = "✅" if status else "❌"
    print(f"{icon} {check}: {message}")
    return status

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 11
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return print_status(
        "Python Version", 
        is_valid, 
        f"{version_str} {'(OK)' if is_valid else '(Need 3.11+)'}"
    )

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    return print_status(description, exists, filepath)

def check_backend_deps():
    """Check backend dependencies"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import loguru
        return print_status("Backend Dependencies", True, "FastAPI, Uvicorn, Pydantic installed")
    except ImportError as e:
        return print_status("Backend Dependencies", False, f"Missing: {e.name}")

def check_huggingface_deps():
    """Check Hugging Face dependencies (optional)"""
    try:
        import transformers
        import sentence_transformers
        return print_status("Hugging Face Dependencies", True, "transformers, sentence-transformers")
    except ImportError:
        return print_status("Hugging Face Dependencies (Optional)", True, "Not installed (will use API mode)")

def check_nodejs():
    """Check Node.js installation"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        return print_status("Node.js", True, f"{version}")
    except FileNotFoundError:
        return print_status("Node.js", False, "Not installed")

def check_npm_deps():
    """Check if frontend dependencies are installed"""
    node_modules = Path("frontend/node_modules")
    exists = node_modules.exists()
    return print_status("Frontend Dependencies", exists, "node_modules" if exists else "Run: cd frontend && npm install")

def check_env_file():
    """Check for .env.example"""
    has_example = Path(".env.example").exists()
    has_real = Path(".env").exists()
    
    if has_example:
        print_status(".env.example", True, "Template exists")
    else:
        print_status(".env.example", False, "Missing template")
    
    if has_real:
        print_status(".env", True, "Configuration exists (ensure no real API keys!)")
    else:
        print_status(".env (Optional)", True, "Not present (using defaults)")
    
    return has_example

def check_documentation():
    """Check key documentation files"""
    docs = [
        ("README.md", "Main documentation"),
        ("docs/AI_FEATURES.md", "AI features guide"),
        ("docs/COMPETITIVE_ADVANTAGES.md", "Competition strategy"),
        ("docs/DEMO_CHEAT_SHEET.md", "Demo reference"),
        ("pitch/PITCH_DECK.md", "Pitch deck"),
        ("SUBMISSION_CHECKLIST.md", "Submission guide")
    ]
    
    all_exist = True
    for filepath, description in docs:
        exists = Path(filepath).exists()
        all_exist = all_exist and exists
        print_status(description, exists, filepath)
    
    return all_exist

def check_backend_structure():
    """Check backend file structure"""
    files = [
        "backend/main.py",
        "backend/agents/expense_classifier.py",
        "backend/agents/invoice_agent.py",
        "backend/agents/fraud_analyzer.py",
        "backend/agents/cashflow_forecast.py",
        "backend/agents/orchestrator.py",
        "backend/agents/smart_assistant.py",
        "backend/services/huggingface_service.py",
        "backend/requirements-demo.txt",
        "backend/requirements-huggingface.txt"
    ]
    
    all_exist = True
    for filepath in files:
        exists = Path(filepath).exists()
        all_exist = all_exist and exists
        if not exists:
            print_status("Missing", False, filepath)
    
    if all_exist:
        print_status("Backend Structure", True, "All agent files present")
    
    return all_exist

def check_frontend_structure():
    """Check frontend file structure"""
    files = [
        "frontend/src/App.tsx",
        "frontend/src/pages/Dashboard.tsx",
        "frontend/src/pages/ExpenseUpload.tsx",
        "frontend/src/pages/InvoiceCreation.tsx",
        "frontend/src/pages/FraudAlerts.tsx",
        "frontend/src/pages/CashflowForecast.tsx",
        "frontend/src/pages/VoiceAssistant.tsx",
        "frontend/package.json"
    ]
    
    all_exist = True
    for filepath in files:
        exists = Path(filepath).exists()
        all_exist = all_exist and exists
        if not exists:
            print_status("Missing", False, filepath)
    
    if all_exist:
        print_status("Frontend Structure", True, "All pages present")
    
    return all_exist

def check_demo_scripts():
    """Check demo scripts"""
    scripts = [
        "demos/expense_processing_demo.py",
        "demos/invoice_creation_demo.py",
        "demos/fraud_detection_demo.py",
        "demos/cashflow_forecast_demo.py"
    ]
    
    all_exist = True
    for script in scripts:
        exists = Path(script).exists()
        all_exist = all_exist and exists
        if not exists:
            print_status("Missing", False, script)
    
    if all_exist:
        print_status("Demo Scripts", True, "All 4 demos present")
    
    return all_exist

def main():
    """Run all verification checks"""
    print_header("FinAgent Pro - Setup Verification")
    
    print("🔍 Checking system requirements...\n")
    
    checks = []
    
    # System checks
    print_header("System Requirements")
    checks.append(check_python_version())
    checks.append(check_nodejs())
    
    # Dependency checks
    print_header("Dependencies")
    checks.append(check_backend_deps())
    check_huggingface_deps()  # Optional, don't fail on this
    checks.append(check_npm_deps())
    
    # File structure checks
    print_header("Backend Structure")
    checks.append(check_backend_structure())
    
    print_header("Frontend Structure")
    checks.append(check_frontend_structure())
    
    # Documentation checks
    print_header("Documentation")
    checks.append(check_documentation())
    
    # Demo checks
    print_header("Demo Scripts")
    checks.append(check_demo_scripts())
    
    # Environment checks
    print_header("Configuration")
    check_env_file()
    
    # Final summary
    print_header("Summary")
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 Your FinAgent Pro installation is ready!")
        print("\nNext steps:")
        print("1. Start backend: cd backend && set DEMO_MODE=1 && python -m uvicorn main:app --reload")
        print("2. Start frontend: cd frontend && npm run dev")
        print("3. Open browser: http://localhost:3000")
        print("4. Test voice: http://localhost:3000/voice")
        return 0
    else:
        print(f"⚠️  {total - passed} checks failed")
        print("\nPlease fix the issues above before proceeding.")
        print("See SUBMISSION_CHECKLIST.md for detailed setup instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
