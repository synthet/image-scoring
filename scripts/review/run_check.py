"""Run a bounded review check and preserve its command, output and timing locally."""

import argparse
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if args.receipt.exists():
        parser.error("Receipt exists; use a new path")
    started = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    try:
        result = subprocess.run(command, cwd=args.cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=args.timeout)
        output, code = result.stdout, result.returncode
    except subprocess.TimeoutExpired as exc:
        output, code = (exc.stdout or b"") + b"\nREVIEW CHECK TIMED OUT\n", 124
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    log = args.receipt.with_suffix(".log")
    log.write_bytes(output)
    receipt = {"started_at": started, "elapsed_seconds": time.perf_counter() - start,
               "cwd": str(args.cwd.resolve()), "command": command, "timeout_seconds": args.timeout,
               "exit_code": code, "output_sha256": hashlib.sha256(output).hexdigest(),
               "output_file": log.name, "campaign_gpu_hours": 0}
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    print(output.decode("utf-8", errors="replace")[-3500:])
    raise SystemExit(code)


if __name__ == "__main__":
    main()
