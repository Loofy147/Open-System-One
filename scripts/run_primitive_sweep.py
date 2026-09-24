from __future__ import annotations

import argparse
from open_system_one.sweep import run_pair_sweep, run_single_sweep, save_results

p = argparse.ArgumentParser()
p.add_argument("--out", default="primitive_sweep.json")
p.add_argument("--pairs", action="store_true")
args = p.parse_args()

singles = run_single_sweep()
pairs = run_pair_sweep() if args.pairs else []
save_results(args.out, singles, pairs)
for row in singles:
    print(f"{row.status:26} {row.primitive:28} {row.elapsed_ms:8.3f} ms")
print(f"saved: {args.out}")
if pairs:
    print(f"pair probes: {len(pairs)}")
