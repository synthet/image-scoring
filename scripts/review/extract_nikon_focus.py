"""Read only the user-named Nikon sequence; write derived focus metadata and identity receipts."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

TAGS = ("Model", "LensModel", "AFInfo2Version", "FocusMode", "AFDetectionMethod", "AFAreaMode",
        "AFCoordinatesAvailable", "AFImageWidth", "AFImageHeight", "AFAreaXPosition", "AFAreaYPosition",
        "AFAreaWidth", "AFAreaHeight", "AFPointsUsed", "FocusResult", "FocusDistance",
        "Orientation", "ImageWidth", "ImageHeight", "ExifImageWidth", "ExifImageHeight", "CropArea",
        "CropHiSpeed", "DateTimeOriginal", "SubSecTimeOriginal", "ExposureTime", "FNumber", "ISO", "FocalLength")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--directory", required=True, type=Path)
    ap.add_argument("--exiftool", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    assert not args.output.exists(), "Preserve prior extraction"
    files = [args.directory / f"DSC_{n:04d}.NEF" for n in range(56, 67)]
    assert all(p.is_file() for p in files), "Named range must be complete"
    before = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in files}
    env = dict(os.environ, LC_ALL="C", LC_CTYPE="C", LANG="C")
    version = subprocess.check_output([str(args.exiftool), "-ver"], env=env, text=True).strip()
    results = {}
    for numeric in (True, False):
        cmd = [str(args.exiftool), "-j", "-G1", "-a", "-s"] + (["-n"] if numeric else [])
        cmd += ["-" + tag for tag in TAGS] + [str(p) for p in files]
        result = subprocess.run(cmd, capture_output=True, env=env, timeout=90)
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        rows = json.loads(result.stdout)
        assert len(rows) == len(files)
        for row in rows:
            row["SourceFile"] = Path(row["SourceFile"]).name
        results["numeric" if numeric else "formatted"] = rows
    assert before == {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in files}, "Source changed during extraction"
    args.output.mkdir(parents=True)
    receipt = {"status": "read-only extraction; no scoring or culling decisions", "exiftool_version": version,
               "exiftool_sha256": sha(args.exiftool), "tags": TAGS, "files": before, "results": results,
               "runner_sha256": sha(Path(__file__))}
    (args.output / "nikon-focus-extraction.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    for row in results["numeric"]:
        print(row["SourceFile"], {k: v for k, v in row.items() if k.split(":")[-1] in (
            "AFInfo2Version", "AFImageWidth", "AFImageHeight", "AFAreaXPosition", "AFAreaYPosition", "AFAreaWidth",
            "AFAreaHeight", "FocusResult", "ISO", "FNumber", "ExposureTime", "FocusDistance", "Orientation")})


if __name__ == "__main__":
    main()
