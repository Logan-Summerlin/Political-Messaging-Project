#!/usr/bin/env python3
import argparse, csv, hashlib, json, os, random, sys, time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

TERMINAL_OK = {"ok_cached", "ok_fetched", "ok_not_modified", "skip_irrelevant"}
RETRYABLE_HTTP = {429, 500, 502, 503, 504}


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_status(path: Path):
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {r["url"]: r for r in rows if r.get("url")}


def write_status(path: Path, rows_by_url: dict):
    fields = ["url", "last_attempt_ts_utc", "final_status", "http_status", "cache_path", "http_meta_path", "retry_count", "next_action", "notes"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for u in sorted(rows_by_url):
            row = {k: rows_by_url[u].get(k, "") for k in fields}
            w.writerow(row)


def append_request_log(path: Path, row: dict):
    fields = ["run_id","request_ts_utc","url","method","attempt_no","sleep_before_sec","status_code","bytes_received","etag_sent","etag_received","last_modified_sent","last_modified_received","cache_outcome","error_type","elapsed_ms"]
    exists = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in fields})


def sanitize_slug(url: str):
    seg = urlparse(url).path.rstrip("/").split("/")[-1] or "index"
    slug = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in seg).strip("-") or "page"
    return slug.lower()


def build_paths(out_root: Path, url: str, publish_date: str):
    dt = datetime.strptime(publish_date[:10], "%Y-%m-%d")
    slug = sanitize_slug(url)
    base = out_root / "html" / f"{dt:%Y}" / f"{dt:%m}" / f"{dt:%d}"
    html_path = base / f"{slug}.html"
    if html_path.exists() and html_path.stat().st_size > 0:
        digest = hashlib.sha1(url.encode()).hexdigest()[:8]
        html_path = base / f"{slug}-{digest}.html"
    return html_path, html_path.with_suffix(".http.json"), html_path.with_suffix(".txt")


def should_fetch_row(row):
    d = row.get("publish_date","")[:10]
    c = (row.get("content_class") or row.get("phase1_classification") or "unknown").lower()
    try:
        in_window = "2018-01-01" <= d <= "2026-12-31"
    except Exception:
        return False
    cls_ok = c in {"poll_messaging", "unknown", "polling_or_messaging", "polling_messaging_brief"}
    if "non_poll" in c or "commentary" in c or "horserace" in c:
        cls_ok = False
    return in_window and cls_ok


def fetch_url(opener, url, timeout, headers):
    req = Request(url, headers=headers)
    t0 = time.time()
    try:
        resp = opener.open(req, timeout=timeout)
        body = resp.read()
        elapsed = int((time.time()-t0)*1000)
        return resp.getcode(), dict(resp.headers.items()), body, resp.geturl(), elapsed, None
    except HTTPError as e:
        elapsed = int((time.time()-t0)*1000)
        return e.code, dict(e.headers.items()) if e.headers else {}, e.read() if hasattr(e, "read") else b"", url, elapsed, "http"
    except URLError:
        elapsed = int((time.time()-t0)*1000)
        return None, {}, b"", url, elapsed, "timeout"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--min-delay", type=float, default=10)
    ap.add_argument("--max-delay", type=float, default=20)
    ap.add_argument("--pause-every", type=int, default=25)
    ap.add_argument("--pause-min", type=float, default=60)
    ap.add_argument("--pause-max", type=float, default=120)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--refresh-stale", type=int, default=None)
    ap.add_argument("--max-urls", type=int, default=None)
    args = ap.parse_args()

    out_root = Path(args.out_root)
    req_log = out_root / "request_log.csv"
    status_path = out_root / "fetch_status.csv"
    status = load_status(status_path)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    rows=[]
    with open(args.inventory, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            url = r.get("source_url") or r.get("url")
            if not url: continue
            if should_fetch_row(r):
                rows.append({**r, "url":url})
    if args.max_urls: rows = rows[:args.max_urls]
    if args.dry_run:
        print(f"planned_urls={len(rows)}")
        return

    opener = build_opener(HTTPRedirectHandler())
    consecutive_429=0
    request_count=0
    for row in rows:
        url=row["url"]
        publish_date = (row.get("publish_date") or "2018-01-01")[:10]
        s = status.get(url, {})
        if s.get("final_status") == "ok_cached" and args.refresh_stale is None:
            continue
        if args.resume and s.get("final_status") in TERMINAL_OK and args.refresh_stale is None:
            continue
        html_path, meta_path, txt_path = build_paths(out_root, url, publish_date)
        if html_path.exists() and args.refresh_stale is None:
            status[url] = {"url":url,"last_attempt_ts_utc":now_utc(),"final_status":"ok_cached","http_status":"200","cache_path":str(html_path),"http_meta_path":str(meta_path),"retry_count":"0","next_action":"none","notes":"cache hit skip"}
            continue

        etag_sent = s.get("etag_received","")
        lmod_sent = s.get("last_modified_received","")
        headers = {"User-Agent":"PoliticalMessagingDataset/1.0 (research; contact: maintainer@example.com)"}
        if etag_sent: headers["If-None-Match"] = etag_sent
        if lmod_sent: headers["If-Modified-Since"] = lmod_sent

        final_status="error_retryable"; http_status=""; notes=""; retry_count=0
        for attempt in range(1, args.retries+1):
            sleep_before = random.uniform(args.min_delay, args.max_delay)
            time.sleep(sleep_before)
            request_count += 1
            code, resp_headers, body, final_url, elapsed_ms, err = fetch_url(opener, url, args.timeout, headers)
            log = {"run_id":run_id,"request_ts_utc":now_utc(),"url":url,"method":"GET","attempt_no":attempt,"sleep_before_sec":f"{sleep_before:.2f}","status_code":code or "","bytes_received":len(body),"etag_sent":headers.get("If-None-Match",""),"etag_received":resp_headers.get("ETag",""),"last_modified_sent":headers.get("If-Modified-Since",""),"last_modified_received":resp_headers.get("Last-Modified",""),"elapsed_ms":elapsed_ms}

            if code == 304:
                final_status="ok_not_modified"; http_status="304"; notes="not modified"
                log["cache_outcome"] = "304_not_modified"
                append_request_log(req_log, log)
                consecutive_429=0
                break
            if code == 200 and body:
                html_path.parent.mkdir(parents=True, exist_ok=True)
                html_path.write_bytes(body)
                txt_path.write_text(body.decode("utf-8", errors="replace"), encoding="utf-8")
                meta = {"url":url,"final_url":final_url,"status_code":200,"request_headers":headers,"response_headers":resp_headers,"fetched_at_utc":now_utc()}
                meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
                final_status="ok_fetched"; http_status="200"; notes="fetched"
                log["cache_outcome"] = "fetched_200"
                append_request_log(req_log, log)
                consecutive_429=0
                break

            log["cache_outcome"] = "error"
            if code == 429:
                log["error_type"] = "http_429"; consecutive_429 += 1
            elif code in RETRYABLE_HTTP:
                log["error_type"] = "http_5xx"; consecutive_429=0
            else:
                log["error_type"] = err or "http_other"; consecutive_429=0
            append_request_log(req_log, log)
            retry_count = attempt
            if consecutive_429 >= 3:
                status[url] = {"url":url,"last_attempt_ts_utc":now_utc(),"final_status":"halt_rate_limit","http_status":str(code),"cache_path":str(html_path),"http_meta_path":str(meta_path),"retry_count":str(retry_count),"next_action":"manual_wait","notes":"halt_reason=rate_limited"}
                write_status(status_path, status)
                print("Circuit breaker: 3 consecutive 429; halting.")
                return
            if attempt < args.retries and (code in RETRYABLE_HTTP or err):
                backoff = [20,45,90][attempt-1] + random.uniform(-5,5)
                time.sleep(max(1, backoff))
                continue
            if code and code not in RETRYABLE_HTTP:
                final_status="error_terminal"; http_status=str(code); notes="terminal http"
            else:
                final_status="error_retryable"; http_status=str(code or ""); notes="retryable failure"

        status[url] = {"url":url,"last_attempt_ts_utc":now_utc(),"final_status":final_status,"http_status":http_status,"cache_path":str(html_path),"http_meta_path":str(meta_path),"retry_count":str(retry_count),"next_action":"none" if final_status in TERMINAL_OK else "retry","notes":notes}
        if request_count % max(1,args.pause_every) == 0:
            time.sleep(random.uniform(args.pause_min,args.pause_max))
        write_status(status_path, status)


if __name__ == "__main__":
    main()
