import os
import shutil
import time
import subprocess
from typing import List, Optional, Dict
import re


def ensure_directory(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)


def backup_file(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    ts = time.strftime('%Y%m%d-%H%M%S')
    backup_path = f"{path}.{ts}.bak"
    shutil.copy2(path, backup_path)
    return backup_path


def generate_worktodo_lines(exponents: List[int], mode: str = "LL") -> List[str]:
    """
    Generate Prime95 WorkToDo.txt lines for given Mersenne exponents.

    Notes:
    - Classic Lucas-Lehmer assignment lines are accepted as "Test=p" by many p95 builds.
    - Newer formats may use PRP/LL variants; keep it simple and configurable.
    - mode options: "LL" (Lucas-Lehmer for Mersenne), "PRP" (probable prime test), "PFACTOR" (trial factoring).
    """
    lines: List[str] = []
    for p in sorted(set(int(x) for x in exponents if x and x > 1)):
        if mode.upper() == "LL":
            # LL test for Mersenne number 2^p-1
            lines.append(f"Test={p}")
        elif mode.upper() == "PRP":
            # PRP test for Mersenne number 2^p-1 (Gerbicz, etc.)
            # Many builds accept: PRP=p,1
            lines.append(f"PRP={p},1")
        elif mode.upper() == "PFACTOR":
            # Trial factoring assignment up to default bounds
            lines.append(f"Pfactor={p}")
        else:
            lines.append(f"Test={p}")
    return lines


def write_worktodo(worktodo_path: str, lines: List[str], append: bool = True) -> str:
    ensure_directory(worktodo_path)
    if append:
        backup_file(worktodo_path)
    mode = 'a' if append else 'w'
    with open(worktodo_path, mode, encoding='utf-8') as f:
        for line in lines:
            f.write(line.rstrip('\n') + "\n")
    return worktodo_path


def launch_prime95(prime95_dir: str) -> Optional[subprocess.Popen]:
    """Attempt to launch Prime95 on Windows by starting prime95.exe in given directory."""
    exe = os.path.join(prime95_dir, 'prime95.exe')
    if not os.path.isfile(exe):
        return None
    # Start minimized without blocking
    try:
        proc = subprocess.Popen([exe], cwd=prime95_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return proc
    except Exception:
        return None


def parse_results(results_path: str, since_bytes: int = 0) -> Dict[str, List[str]]:
    """
    Parse Prime95 results.txt for new lines since a byte offset.
    Returns dict with keys: 'lines', 'new_offset'.
    """
    if not os.path.exists(results_path):
        return {"lines": [], "new_offset": since_bytes}
    size = os.path.getsize(results_path)
    start = min(since_bytes, size)
    lines: List[str] = []
    with open(results_path, 'r', encoding='utf-8', errors='ignore') as f:
        if start:
            f.seek(start)
        for line in f:
            lines.append(line.rstrip('\n'))
    return {"lines": lines, "new_offset": size}


def extract_confirmed_mersenne_primes(lines: List[str]) -> List[int]:
    """
    Parse Prime95 results lines to extract confirmed Mersenne prime exponents p.
    Looks for patterns like:
      - "M( p ) is prime!"
      - "M(p) is prime!"
      - "M( p ) is a probable prime" (treat separately if needed)
    Returns list of integer exponents found.
    """
    exps: List[int] = []
    # Regex for M( 82589933 ) is prime!
    pat_prime = re.compile(r"M\(\s*(\d+)\s*\)\s+is\s+prime", re.IGNORECASE)
    for ln in lines:
        m = pat_prime.search(ln)
        if m:
            try:
                exps.append(int(m.group(1)))
            except:
                continue
    return exps


def parse_mersenne_findings(results_path: str, since_bytes: int = 0) -> Dict:
    """
    Convenience parser that reads Prime95 results.txt since an offset and
    returns any confirmed Mersenne prime exponents and the new offset.
    """
    parsed = parse_results(results_path, since_bytes=since_bytes)
    lines = parsed.get("lines", [])
    new_offset = parsed.get("new_offset", since_bytes)
    confirmed = extract_confirmed_mersenne_primes(lines)
    return {
        "confirmed_exponents": confirmed,
        "new_offset": new_offset,
        "lines": lines,
    }


def integrate_with_prime95(exponents: List[int], config: Dict) -> Dict:
    """
    High-level integration:
    - Generate WorkToDo entries for exponents
    - Write/append to WorkToDo.txt
    - Optionally launch Prime95 process
    - Return summary info
    """
    integration = (config or {}).get('prime95_integration') or (config or {}).get('integration') or {}

    enabled = integration.get('enabled', False)
    if not enabled:
        return {"enabled": False, "reason": "Prime95 integration disabled"}

    prime95_dir = integration.get('prime95_dir') or ''
    worktodo_path = integration.get('worktodo_path') or (os.path.join(prime95_dir, 'worktodo.txt') if prime95_dir else '')
    mode = integration.get('mode', 'LL')
    append = integration.get('append', True)
    auto_launch = integration.get('auto_launch', False)

    if not worktodo_path:
        return {"enabled": True, "error": "Missing worktodo_path in configuration"}

    lines = generate_worktodo_lines(exponents, mode=mode)
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


