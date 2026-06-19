#!/usr/bin/env python3
"""
Benchmark Runner — 2-System LLM Benchmarking
Lena (Controller) triggert Tests auf Ava (Executor) via SSH.
Ergebnisse werden lokal gesammelt und in DB geschrieben.

Usage:
    python run_benchmark.py --target ava --suite inference
    python run_benchmark.py --target local --suite quality
"""

import argparse
import json
import os
import subprocess
import sqlite3
from datetime import datetime
from pathlib import Path

# Config
SYSTEMS = {
    "lena": {
        "host": "localhost",
        "user": "bobadmin",
        "ssh_key": "~/.ssh/id_ed25519",
        "lmstudio_url": "http://localhost:1234/v1",
        "gpu": "4x NVIDIA (RTX 3090 + 3x Device 2803)",
    },
    "ava": {
        "host": "192.168.178.121",
        "user": "bobadmin",
        "ssh_key": "~/.ssh/id_ed25519",
        "lmstudio_url": "http://localhost:1234/v1",
        "gpu": "RTX 4060 Ti + RTX 2070",
    },
}

RESULTS_DIR = Path(__file__).parent.parent / "benchmarks" / "results"
DB_PATH = Path(__file__).parent.parent / "benchmarks" / "db" / "benchmarks.db"


def init_db():
    """SQLite DB erstellen wenn nicht existiert."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            system TEXT,
            model TEXT,
            test_suite TEXT,
            test_name TEXT,
            tokens_per_sec REAL,
            latency_ms REAL,
            score REAL,
            details TEXT
        )
    """)
    conn.commit()
    return conn


def run_remote_command(host, user, command):
    """Command via SSH auf entferntem System ausfuehren."""
    ssh_cmd = f"ssh -o ConnectTimeout=10 {user}@{host} '{command}'"
    result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=300)
    return result.stdout, result.stderr, result.returncode


def test_lmstudio_availability(system_name):
    """Check ob LM Studio auf System verfuegbar ist."""
    sys_config = SYSTEMS[system_name]
    
    if system_name == "lena":
        # Local check
        try:
            import urllib.request
            resp = urllib.request.urlopen(f"{sys_config['lmstudio_url']}/models", timeout=5)
            return json.loads(resp.read())
        except Exception as e:
            print(f"  [WARN] LM Studio nicht erreichbar: {e}")
            return None
    else:
        # Remote check via SSH
        cmd = f'curl -s --max-time 5 {sys_config["lmstudio_url"]}/models || echo "NOT_AVAILABLE"'
        stdout, stderr, rc = run_remote_command(sys_config["host"], sys_config["user"], cmd)
        if "NOT_AVAILABLE" in stdout:
            print(f"  [WARN] LM Studio auf {system_name} nicht erreichbar")
            return None
        try:
            return json.loads(stdout)
        except:
            return None


def run_inference_test(system_name, model_id, prompt="Erzaehle eine kurze Geschichte ueber einen Hund."):
    """Einen einfachen Inference-Test ausfuehren."""
    sys_config = SYSTEMS[system_name]
    
    if system_name == "lena":
        # Local test via curl to LM Studio
        cmd = f'''curl -s {sys_config["lmstudio_url"]}/chat/completions \\
            -H "Content-Type: application/json" \\
            -d '{{"model":"{model_id}","messages":[{{"role":"user","content":"{prompt}"}}],"max_tokens":100}}' '''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    else:
        # Remote test via SSH
        remote_cmd = f'''curl -s --max-time 120 {sys_config["lmstudio_url"]}/chat/completions \\
            -H "Content-Type: application/json" \\
            -d '{{"model":"{model_id}","messages":[{{"role":"user","content":"{prompt}"}}],"max_tokens":100}}' '''
        stdout, stderr, rc = run_remote_command(sys_config["host"], sys_config["user"], remote_cmd)
        result = subprocess.run("", shell=False, capture_output=True, text=True)
        result.stdout = stdout
        result.stderr = stderr
        result.returncode = rc  # type: ignore
    
    try:
        response_json = result.stdout.strip()
        if not response_json:
            raise ValueError("Empty response")
        response = json.loads(response_json)
        return {
            "success": True,
            "output_tokens": response.get("usage", {}).get("completion_tokens", 0),
            "response_preview": response["choices"][0]["message"]["content"][:200],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="LLM Benchmark Runner")
    parser.add_argument("--target", choices=["lena", "ava"], required=True, help="Ziel-System")
    parser.add_argument("--suite", choices=["inference", "quality", "realworld"], default="inference")
    parser.add_argument("--model", type=str, help="Model ID (optional)")
    args = parser.parse_args()

    print(f"\n=== Benchmark Runner ===")
    print(f"Target: {args.target} | Suite: {args.suite}")
    
    # Init DB
    conn = init_db()
    c = conn.cursor()
    
    # Check system availability
    print(f"\n[1/3] System-Check fuer {args.target}...")
    models = test_lmstudio_availability(args.target)
    
    if not models:
        print("  [ERROR] Kein LM Studio verfuegbar. Abbruch.")
        return
    
    model_list = models.get("data", [])
    print(f"  Gefundene Modelle: {len(model_list)}")
    for m in model_list[:5]:
        print(f"    - {m.get('id', 'unknown')}")
    
    # Select model
    target_model = args.model or (model_list[0]["id"] if model_list else None)
    if not target_model:
        print("  [ERROR] Kein Model zum Testen verfuegbar.")
        return
    
    print(f"\n[2/3] Inference-Test mit Model: {target_model}")
    test_result = run_inference_test(args.target, target_model)
    
    if test_result["success"]:
        print(f"  Tokens: {test_result['output_tokens']}")
        print(f"  Preview: {test_result['response_preview'][:100]}...")
        
        # Save to DB
        timestamp = datetime.now().isoformat()
        c.execute("""
            INSERT INTO results (timestamp, system, model, test_suite, test_name, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, args.target, target_model, args.suite, "inference_basic", 
              json.dumps(test_result)))
        conn.commit()
        print(f"\n[3/3] Ergebnis in DB gespeichert.")
    else:
        print(f"  [ERROR] Test fehlgeschlagen: {test_result.get('error')}")
    
    conn.close()


if __name__ == "__main__":
    main()
