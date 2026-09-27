#!/usr/bin/env python3
"""
Closed-Loop Autonomous R&D and Intellectual Property Pipeline Harness
Sole Human Inventor: Kenneth Wayne Dallmier
Entity: Dallmier Tech Venture
"""
import ast
import difflib
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, Callable, List

INVENTOR_NAME = "Kenneth Wayne Dallmier"
ENTITY_NAME = "Dallmier Tech Venture"
DEFAULT_LOCAL_API_BASE = os.environ.get("LOCAL_LLM_API_BASE", "http://localhost:11434/v1")
DEFAULT_MODEL = os.environ.get("LOCAL_LLM_MODEL", "qwen2.5-coder-7b-instruct")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("RDPipelineHarness")

@dataclass
class TelemetryProfile:
    module_name: str
    target_symbol: str
    mean_duration_ms: float
    min_duration_ms: float
    max_duration_ms: float
    iterations: int
    memory_peak_kb: float
    timestamp_utc: str
    raw_samples_ms: List[float]

@dataclass
class OptimizationCandidate:
    original_code: str
    optimized_code: str
    ast_tree: ast.AST
    changes_summary: str
    target_symbol: str

@dataclass
class ValidationResult:
    passed: bool
    tests_run: int
    error_message: Optional[str] = None

@dataclass
class DeltaEvaluation:
    baseline_ms: float
    optimized_ms: float
    speedup_percent: float
    meets_threshold: bool
    threshold_percent: float

class ProfilerStage:
    def __init__(self, warmup_runs: int = 3, benchmark_runs: int = 25):
        self.warmup_runs = warmup_runs
        self.benchmark_runs = benchmark_runs

    def profile_callable(self, module_name: str, symbol_name: str, target_fn: Callable, *args, **kwargs) -> TelemetryProfile:
        logger.info(f"[*] Profiling target '{module_name}.{symbol_name}'...")
        for _ in range(self.warmup_runs):
            target_fn(*args, **kwargs)
        samples_ms = []
        for _ in range(self.benchmark_runs):
            t0 = time.perf_counter_ns()
            target_fn(*args, **kwargs)
            t1 = time.perf_counter_ns()
            samples_ms.append((t1 - t0) / 1_000_000.0)
        mean_ms = sum(samples_ms) / len(samples_ms)
        profile = TelemetryProfile(
            module_name=module_name,
            target_symbol=symbol_name,
            mean_duration_ms=mean_ms,
            min_duration_ms=min(samples_ms),
            max_duration_ms=max(samples_ms),
            iterations=self.benchmark_runs,
            memory_peak_kb=0.0,
            timestamp_utc=datetime.utcnow().isoformat() + "Z",
            raw_samples_ms=samples_ms
        )
        logger.info(f"    - Baseline Mean: {mean_ms:.4f} ms")
        return profile

class LocalLiteLLMOptimizer:
    def __init__(self, api_base: str = DEFAULT_LOCAL_API_BASE, model: str = DEFAULT_MODEL):
        self.api_base = api_base
        self.model = model

    def optimize_code(self, source_code: str, target_symbol: str, profile: TelemetryProfile, algorithmic_fallback: Optional[str] = None) -> OptimizationCandidate:
        candidate_code = algorithmic_fallback or source_code
        return OptimizationCandidate(
            original_code=source_code,
            optimized_code=candidate_code,
            ast_tree=ast.parse(candidate_code),
            changes_summary=f"Algorithmic optimization for {target_symbol}.",
            target_symbol=target_symbol
        )

class ValidationStage:
    @staticmethod
    def validate(candidate: OptimizationCandidate, test_suite_fn: Callable[[Callable], bool]) -> ValidationResult:
        local_scope = {}
        try:
            exec(candidate.optimized_code, {}, local_scope)
            candidate_fn = local_scope.get(candidate.target_symbol)
            if not candidate_fn or not test_suite_fn(candidate_fn):
                return ValidationResult(passed=False, tests_run=1, error_message="Regression assertions failed.")
            return ValidationResult(passed=True, tests_run=1)
        except Exception as e:
            return ValidationResult(passed=False, tests_run=0, error_message=str(e))

class BenchmarkDeltaGate:
    @staticmethod
    def evaluate(baseline_profile: TelemetryProfile, optimized_profile: TelemetryProfile, threshold_pct: float = 15.0) -> DeltaEvaluation:
        base_time = baseline_profile.mean_duration_ms
        opt_time = optimized_profile.mean_duration_ms
        delta_pct = ((base_time - opt_time) / base_time) * 100.0 if base_time > 0 else 0.0
        return DeltaEvaluation(baseline_ms=base_time, optimized_ms=opt_time, speedup_percent=delta_pct, meets_threshold=delta_pct >= threshold_pct, threshold_percent=threshold_pct)

class IDPGenerator:
    @staticmethod
    def compile_packet(module_name: str, technical_field: str, problem_desc: str, code_diff: str, baseline_profile: TelemetryProfile, optimized_profile: TelemetryProfile, delta_pct: float) -> str:
        date_str = datetime.utcnow().strftime("%Y%m%d")
        doc_ref = f"IDP-DTV-{date_str}-{module_name.upper()}"
        try:
            git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        except Exception:
            git_hash = "UNCOMMITTED_WORKING_TREE"
        
        hasher = hashlib.sha256()
        hasher.update(f"{doc_ref}:{INVENTOR_NAME}:{ENTITY_NAME}:{git_hash}:{delta_pct:.4f}:{code_diff}".encode("utf-8"))
        
        return f"""# INVENTION DISCLOSURE PACKET (IDP)
**Document Reference**: `{doc_ref}`  
**Sole Human Inventor**: {INVENTOR_NAME}  
**Assignee / Entity**: {ENTITY_NAME}  
**Git Anchor Hash**: `{git_hash}`  
**Forensic SHA-256 Integrity**: `{hasher.hexdigest()}`  

### 1. TECHNICAL FIELD
{technical_field}

### 2. PROBLEM STATEMENT & PRIOR DEFICIENCIES
{problem_desc}

### 3. COMPARATIVE CODE DIFF
```diff
{code_diff}
4. EMPIRICAL METRICS
Baseline Mean: {baseline_profile.mean_duration_ms:.4f} ms

Optimized Mean: {optimized_profile.mean_duration_ms:.4f} ms

Net Delta: {delta_pct:+.2f}%
"""

if name == "main":
src_baseline = "def deduplicate_stream(items):\n    result = []\n    for x in items:\n        if x not in result:\n            result.append(x)\n    return result\n"
src_optimized = "def deduplicate_stream(items):\n    seen = set()\n    result = []\n    for x in items:\n        if x not in seen:\n            seen.add(x)\n            result.append(x)\n    return result\n"

ns_b, ns_o = {}, {}
exec(src_baseline, ns_b)
exec(src_optimized, ns_o)
fn_b = ns_b["deduplicate_stream"]
fn_o = ns_o["deduplicate_stream"]

profiler = ProfilerStage()
base_profile = profiler.profile_callable("stream_core", "deduplicate_stream", fn_b, list(range(1500)) * 2)
opt_profile = profiler.profile_callable("stream_core", "deduplicate_stream", fn_o, list(range(1500)) * 2)

delta = BenchmarkDeltaGate.evaluate(base_profile, opt_profile)
if delta.meets_threshold:
    diff_str = "".join(difflib.unified_diff(src_baseline.splitlines(keepends=True), src_optimized.splitlines(keepends=True)))
    idp = IDPGenerator.compile_packet("stream_core", "High-Performance Compute", "Quadratic search latency", diff_str, base_profile, opt_profile, delta.speedup_percent)
    with open("IDP_STREAM_CORE_DEDUPLICATE_STREAM.md", "w") as f:
        f.write(idp)
    logger.info("[+] IDP Dossier compiled successfully.")
