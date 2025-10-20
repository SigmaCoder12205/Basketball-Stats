import sys, time, json, traceback
from pathlib import Path
import os, psutil

process = psutil.Process(os.getpid())
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_ROOT / "Database" / "log"
BASE_DIR.mkdir(parents=True, exist_ok=True)

def write_json(file, data):
    Path(file).parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'a', encoding='utf-8') as f:
        json.dump(data, f)
        f.write("\n")

def global_trace(frame, event, arg):
    if event not in {"call", "return", "exception"}:
        return

    filename_full = Path(frame.f_code.co_filename).resolve()
    if not str(filename_full).startswith(str(PROJECT_ROOT)):
        return
    if "<frozen" in str(filename_full) or "site-packages" in str(filename_full):
        return

    perf = {
        "cpu_percent": process.cpu_percent(interval=None),
        "memory_mb": round(process.memory_info().rss / (1024 * 1024), 2),
        "depth": len(traceback.extract_stack(frame))
    }

    filename = Path(filename_full).name
    log_path = BASE_DIR / f"{filename}_requests.json"

    func = frame.f_code.co_name
    caller = frame.f_back.f_code.co_name if frame.f_back else "N/A"
    lineno = frame.f_lineno
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    args_info = {k: repr(v) for k, v in frame.f_locals.items() if k != "_trace_start"}
    code_val = frame.f_locals.get("code", 200)  # define code

    if event == "call":
        frame.f_locals["_trace_start"] = time.perf_counter()
        entry = {
            "timestamp": timestamp,
            "event": "call",
            "caller": caller,
            "function": func,
            "args": args_info,
            "file": filename,
            "path": str(filename_full),
            "line": lineno,
            "code": code_val
        }
        entry.update(perf)

    elif event == "return":
        start = frame.f_locals.get("_trace_start", time.perf_counter())
        entry = {
            "timestamp": timestamp,
            "event": "return",
            "function": func,
            "duration_ms": round((time.perf_counter() - start) * 1000, 2),
            "file": filename,
            "path": str(filename_full),
            "line": lineno,
            "code": code_val
        }
        entry.update(perf)

    elif event == "exception":
        exc_type, exc_value, exc_tb = arg
        tb_list = traceback.format_exception(exc_type, exc_value, exc_tb)
        entry = {
            "timestamp": timestamp,
            "event": "error",
            "function": func,
            "file": filename,
            "path": str(filename_full),
            "line": lineno,
            "error_type": exc_type.__name__,
            "error_message": "".join(tb_list).strip(),
            "args": args_info,
            "code": 500
        }
        entry.update(perf)

    write_json(log_path, entry)
    return global_trace


    write_json(log_path, entry)
    return global_trace
