from __future__ import annotations
from .engine import DecisionEngine
from .schema import DecisionRequest, DecisionResponse

def create_app(engine: DecisionEngine):
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise RuntimeError("install open-system-one[server]") from exc
    app=FastAPI(title="Open System One",version="0.1.0")
    @app.post("/v1/systemone",response_model=DecisionResponse)
    def system_one(request:DecisionRequest): return engine.evaluate(request)
    @app.get("/v1/health")
    def health(): return {"ok":True,"model":engine.backend.name}
    return app
