import os
import shutil
import time
import subprocess
from typing import List, Optional, Dict
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_directory(path: str) -> None:
    """Ensure directory exists with proper error handling"""
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        raise

def backup_file(path: str) -> Optional[str]:
    """Backup file with error handling"""
    if not os.path.exists(path):
        return None
    try:
        ts = time.strftime('%Y%m%d-%H%M%S')
        backup_path = f"{path}.{ts}.bak"
        shutil.copy2(path, backup_path)
        return backup_path
    except (OSError, IOError) as e:
        logger.error(f"Failed to backup file {path}: {e}")
        return None

def generate_worktodo_lines(exponents: List[int], mode: str = "LL") -> List[str]:
    """Generate Prime95 WorkToDo.txt lines with validation"""
    if not exponents:
        return []
    
    lines: List[str] = []
    valid_modes = {"LL", "PRP", "PFACTOR"}
    mode = mode.upper()
    
    if mode not in valid_modes:
        logger.warning(f"Invalid mode {mode}, using LL")
        mode = "LL"
    
    for p in exponents:
        try:
            p = int(p)
            if p <= 1:
                logger.warning(f"Skipping invalid exponent: {p}")
                continue
                
            if mode == "LL":
                lines.append(f"Test={p}")
            elif mode == "PRP":
                lines.append(f"PRP={p},1")
            elif mode == "PFACTOR":
                lines.append(f"Pfactor={p}")
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid exponent {p}: {e}")
            continue
    
    return lines

def write_worktodo(worktodo_path: str, lines: List[str], append: bool = True) -> str:
    """Write worktodo with proper error handling"""
    if not lines:
        logger.warning("No lines to write")
        return worktodo_path
    
    try:
        ensure_directory(worktodo_path)
        if append and os.path.exists(worktodo_path):
            backup_file(worktodo_path)
        
        mode = 'a' if append else 'w'
        with open(worktodo_path, mode, encoding='utf-8') as f:
            for line in lines:
                f.write(line.rstrip('\n') + "\n")
        
        logger.info(f"Written {len(lines)} lines to {worktodo_path}")
        return worktodo_path
    except (OSError, IOError) as e:
        logger.error(f"Failed to write worktodo file {worktodo_path}: {e}")
        raise

def launch_prime95(prime95_dir: str) -> Optional[subprocess.Popen]:
    """Launch Prime95 with error handling"""
    if not prime95_dir or not os.path.isdir(prime95_dir):
        logger.error(f"Invalid Prime95 directory: {prime95_dir}")
        return None
    
    exe = os.path.join(prime95_dir, 'prime95.exe')
    if not os.path.isfile(exe):
        logger.error(f"Prime95 executable not found: {exe}")
        return None
    
    try:
        proc = subprocess.Popen(
            [exe], 
            cwd=prime95_dir, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        logger.info(f"Prime95 launched with PID: {proc.pid}")
        return proc
    except (OSError, subprocess.SubprocessError) as e:
        logger.error(f"Failed to launch Prime95: {e}")
        return None

def parse_results(results_path: str, since_bytes: int = 0) -> Dict[str, any]:
    """Parse Prime95 results with error handling"""
    if not os.path.exists(results_path):
        return {"lines": [], "new_offset": since_bytes}
    
    try:
        size = os.path.getsize(results_path)
        start = min(since_bytes, size)
        lines: List[str] = []
        
        with open(results_path, 'r', encoding='utf-8', errors='ignore') as f:
            if start:
                f.seek(start)
            lines = [line.rstrip('\n') for line in f]
        
        return {"lines": lines, "new_offset": size}
    except (OSError, IOError) as e:
        logger.error(f"Failed to parse results file {results_path}: {e}")
        return {"lines": [], "new_offset": since_bytes}

def extract_confirmed_mersenne_primes(lines: List[str]) -> List[int]:
    """Extract confirmed Mersenne primes with better error handling"""
    exps: List[int] = []
    pat_prime = re.compile(r"M\(\s*(\d+)\s*\)\s+is\s+prime", re.IGNORECASE)
    
    for ln in lines:
        try:
            m = pat_prime.search(ln)
            if m:
                exp = int(m.group(1))
                if exp > 0:  # Validate positive exponent
                    exps.append(exp)
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse line '{ln}': {e}")
            continue
    
    return exps

def integrate_with_prime95(exponents: List[int], config: Dict) -> Dict:
    """High-level integration with comprehensive error handling"""
    if not exponents:
        return {"enabled": False, "reason": "No exponents provided"}
    
    try:
        integration = (config or {}).get('prime95_integration', {})
        enabled = integration.get('enabled', False)
        
        if not enabled:
            return {"enabled": False, "reason": "Prime95 integration disabled"}

        prime95_dir = integration.get('prime95_dir', '')
        worktodo_path = integration.get('worktodo_path') or (
            os.path.join(prime95_dir, 'worktodo.txt') if prime95_dir else ''
        )
        mode = integration.get('mode', 'LL')
        append = integration.get('append', True)
        auto_launch = integration.get('auto_launch', False)

        if not worktodo_path:
            return {"enabled": True, "error": "Missing worktodo_path in configuration"}

        lines = generate_worktodo_lines(exponents, mode=mode)
        if not lines:
            return {"enabled": True, "error": "No valid work lines generated"}
        
        written_path = write_worktodo(worktodo_path, lines, append=append)

        proc = None
        if auto_launch and prime95_dir:
            proc = launch_prime95(prime95_dir)

        return {
            "enabled": True,
            "worktodo_path": written_path,
            "lines_written": len(lines),
            "launched": bool(proc),
            "prime95_dir": prime95_dir,
            "mode": mode
        }
    except Exception as e:
        logger.error(f"Prime95 integration failed: {e}")
        return {"enabled": True, "error": str(e)}