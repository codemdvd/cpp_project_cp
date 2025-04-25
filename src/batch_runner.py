#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import pathlib
import sys
import argparse
import shutil

SOLVER = pathlib.Path(__file__).with_name("dfa").resolve() 
CHECKER = pathlib.Path(__file__).with_name("checker.exe").resolve()
INST_DIR  = pathlib.Path("instances")
OUT_DIR   = pathlib.Path("out")
DIAG_DIR  = pathlib.Path("diagram")
TIME_LIM  = 60

def already_solved(out_file: pathlib.Path) -> bool:
    return out_file.exists() and out_file.stat().st_size > 0

def run_solver(inp: pathlib.Path, out: pathlib.Path) -> str:
    try:
        with inp.open("rb") as fin, out.open("wb") as fout:
            subprocess.run(
                [str(SOLVER)],
                stdin=fin, stdout=fout, stderr=subprocess.DEVNULL,
                timeout=TIME_LIM, check=True
            )
        return "DONE"
    except subprocess.TimeoutExpired:
        if out.exists(): out.unlink()
        return "TIMEOUT"
    except subprocess.CalledProcessError as e:
        if out.exists(): out.unlink()
        return f"ERROR(exit={e.returncode})"

def run_checker_and_move_diagram(out: pathlib.Path) -> str:
    try:
        p = subprocess.run(
            [str(CHECKER)],
            input=out.read_bytes(),
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            timeout=10
        )
        text = p.stdout.decode('utf-8', 'replace').splitlines()
        if not text:
            return "CHK_NO_OUTPUT"
        status = text[0].strip()
        if len(text) >= 2 and "Plotting solution to file" in text[1]:
            fname = text[1].split()[-1]
            src = pathlib.Path(fname)
            if src.exists():
                DIAG_DIR.mkdir(exist_ok=True)
                dst = DIAG_DIR / f"{out.stem}.png"
                shutil.move(str(src), str(dst))
        return status
    except subprocess.TimeoutExpired:
        return "CHK_TIMEOUT"
    except Exception as e:
        return f"CHK_ERROR({e})"

def main(argv=None):
    p = argparse.ArgumentParser(description="Batch run solver + checker + diagrams")
    p.add_argument("--force", action="store_true",
                   help="try again .out")
    args = p.parse_args(argv)

    if not SOLVER.exists():
        sys.exit(f"Solver not found: {SOLVER}")
    if not CHECKER.exists():
        sys.exit(f"Checker not found: {CHECKER}")

    OUT_DIR.mkdir(exist_ok=True)

    stats = {
        "total_inp":   0,
        "skipped":     0,
        "solved":      0,
        "timeout":     0,
        "error":       0,
        "checked_ok":  0,
        "checked_bad": 0,
        "checked_err": 0
    }

    print("=== Batch solving ===")
    for inp in sorted(INST_DIR.glob("*.inp")):
        stats["total_inp"] += 1
        out = OUT_DIR / (inp.stem + ".out")

        if not args.force and already_solved(out):
            print(f"[ ] {inp.name:30} SKIP")
            stats["skipped"] += 1
            continue

        print(f"[+] {inp.name:30}", end=" ", flush=True)
        res = run_solver(inp, out)
        print(res)
        if res == "DONE":
            stats["solved"] += 1
        elif res == "TIMEOUT":
            stats["timeout"] += 1
        else:
            stats["error"] += 1

    print("\n=== Batch checking & diagramming ===")
    for out in sorted(OUT_DIR.glob("*.out")):
        print(f"[?] {out.name:30}", end=" ", flush=True)
        chk = run_checker_and_move_diagram(out)
        print(chk)
        if chk.startswith("OK"):
            stats["checked_ok"]  += 1
        elif chk.startswith("NO"):
            stats["checked_bad"] += 1
        else:
            stats["checked_err"] += 1

    print("\n=== Summary ===")
    print(f"Instances total : {stats['total_inp']}")
    print(f"  Skipped        : {stats['skipped']}")
    print(f"  Solved         : {stats['solved']}")
    print(f"    Timeout      : {stats['timeout']}")
    print(f"    Error        : {stats['error']}")
    print(f"Checks total    : {stats['solved']}")
    print(f"  OK             : {stats['checked_ok']}")
    print(f"  Bad            : {stats['checked_bad']}")
    print(f"  Check errors   : {stats['checked_err']}")
    if stats['solved'] > 0:
        pct = stats['checked_ok'] / stats['solved'] * 100
        print(f"\n% OK of solved  : {pct:.2f}%")

if __name__ == "__main__":
    main()
