import json, sys
from pathlib import Path
from decision_arch_sweep_v2 import train_one

name=sys.argv[1]
interaction=float(sys.argv[2])
task=sys.argv[3]
k=int(sys.argv[4])
steps=int(sys.argv[5]) if len(sys.argv)>5 else 50
rows=[]
for seed in (1,2):
    rows.append(train_one(name, task, k, interaction, seed, steps))
out=Path(f'/mnt/data/open-system-one/batch_{task}_{interaction}_{k}_{name}.json')
out.write_text(json.dumps(rows, indent=2))
print(out)
