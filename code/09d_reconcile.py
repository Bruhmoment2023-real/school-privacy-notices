"""Reconcile pass 1 -> data/coding/pass1_reconciled.csv after the regex-discrepancy review and rule v1.1 (documented in coding-rules).
Every change is listed in data/coding/reconciliation_log.csv (unit, item, old, new, reason). pass1.csv is never modified."""
import os, sys, csv
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
c = pd.read_csv(os.path.join(DATA, "coding", "pass1.csv"), dtype=str).fillna("")
FIX = [("ED-043", "D3", "P", "marketing opt-out by link/contact = P under rule D3"),
       ("ED-058", "D3", "P", "states a right to opt out (no channel) = P under rule D3"),
       ("ED-018", "D7", "Y", "rule v1.1: dedicated privacy/grievance address counts as Y for D7"),
       ("ED-001", "D7", "Y", "rule v1.1: dedicated grievance address counts as Y for D7"),
       ("ED-035", "D7", "Y", "rule v1.1: section for data concerns with a privacy contact address")]
log = []
for u, it, new, why in FIX:
    i = c.index[c.unit_id == u][0]; old = c.at[i, it]
    if old != new: log.append((u, it, old, new, why)); c.at[i, it] = new
c.to_csv(os.path.join(DATA, "coding", "pass1_reconciled.csv"), index=False)
pd.DataFrame(log, columns=["unit_id", "item", "old", "new", "reason"]).to_csv(os.path.join(DATA, "coding", "reconciliation_log.csv"), index=False)
print(len(log), "changes")
