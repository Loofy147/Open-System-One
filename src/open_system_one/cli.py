from __future__ import annotations
import argparse, json
from .engine import DecisionEngine
from .schema import DecisionRequest
from .backends.mock import FixedBackend

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--demo",action="store_true"); args=parser.parse_args()
    if not args.demo: parser.error("v0.1 CLI supports --demo")
    req=DecisionRequest.model_validate({"state":"The customer was charged twice and wants a refund.","questions":{"billing":{"type":"noul","instructions":"Is this a billing issue?"},"team":{"type":"choice","instructions":"Which team should handle this?","criteria":{"billing":"charges, refunds","shipping":"delivery","account":"login/profile"}},"severity":{"type":"score","instructions":"How serious is the issue?","criteria":["routine","important","critical"]}}})
    print(json.dumps(DecisionEngine(FixedBackend()).evaluate(req).model_dump(),indent=2))
