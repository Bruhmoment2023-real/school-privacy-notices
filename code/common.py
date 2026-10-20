import os, hashlib, time, json, datetime
ROOT = r"D:\Research-Publishing\11-school-privacy-notices"
DATA = os.path.join(ROOT, "data")
UA = "SchoolPrivacyNoticeAudit/0.1 (academic research on public privacy notices; no-contact; read-only)"
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def now_iso(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
NOTICES = r"E:\Research-Staging\11-school-privacy-notices\notices"
