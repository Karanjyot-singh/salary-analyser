import numpy as np

def summary(salaries):
    if len(salaries) == 0:
        return None
    arr = np.array(salaries, dtype=float)
    return {
        "count": int(arr.size),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "std": float(np.std(arr)),
        "p25": float(np.percentile(arr, 25)),
        "p75": float(np.percentile(arr, 75)),
    }
def by_department(employees):
    groups = {}
    for e in employees:
        groups.setdefault(e["department"], []).append(e["salary"])
    return {dept: float(np.mean(vals)) for dept, vals in groups.items()}
