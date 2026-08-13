from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.metrics import router as metrics_router
from app.routes.agent import router as agent_router
from app.routes.root_cause import router as root_cause_router
from app.routes.recommendations import router as recommendations_router
from app.routes.audit import router as audit_router
from app.routes.charts import router as charts_router
from app.routes.trends import router as trends_router


app = FastAPI(
    title="MetricMind API",
    description="Agentic Semantic BI Engine with Governed Metrics",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(metrics_router)
app.include_router(agent_router)
app.include_router(root_cause_router)
app.include_router(recommendations_router)
app.include_router(audit_router, prefix="/api", tags=["Governance Audit"])
app.include_router(charts_router)
app.include_router(trends_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MetricMind API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }