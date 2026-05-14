#!/usr/bin/env python3
"""Phase 5 QA + dedup + merge prep for DFP 2018-2026 toplines."""

import argparse
import csv
import hashlib
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def to_float(v: str):
    try:
        return float((v or "").strip())
    except Exception:
        return None


def valid_iso_date(v: str) -> bool:
    if not DATE_RE.match(v or ""):
        return False
    try:
        datetime.strptime(v, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def load_csv(path: Path) -> Tuple[List[dict], List[str]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), (r.fieldnames or [])


def compute_quality(row: dict) -> str:
    qtxt = norm(row.get("question_or_message_text", ""))
    pct = to_float(row.get("value_pct", ""))
    metric = norm(row.get("metric_type", "")).lower()
    if qtxt and pct is not None and metric in {"support", "oppose", "favorability_pos", "favorability_neg", "agreement", "concern", "salience"}:
        return "structured_poll"
    return "narrative_finding"


def dedupe_pick(rows: List[dict]) -> Tuple[List[dict], List[dict]]:
    grouped: Dict[Tuple[str, str, str, str], List[dict]] = defaultdict(list)
    for r in rows:
        key = (
            norm(r.get("source_url", "")).lower(),
            norm(r.get("question_text_norm", "")).lower(),
            norm(r.get("metric_type", "")).lower(),
            norm(r.get("value_pct", "")),
        )
        grouped[key].append(r)

    kept, dropped = [], []
    for _, g in grouped.items():
        g_sorted = sorted(
            g,
            key=lambda r: (
                float(r.get("confidence_score", "0") or 0),
                r.get("needs_review", "true") == "false",
                len(norm(r.get("question_or_message_text", ""))),
            ),
            reverse=True,
        )
        winner = g_sorted[0]
        winner["dedupe_status"] = "kept"
        kept.append(winner)
        for d in g_sorted[1:]:
            d["dedupe_status"] = "dropped_duplicate"
            dropped.append(d)
    return kept, dropped


def stable_row_id(r: dict) -> str:
    return hashlib.sha1(
        f"{r.get('source_url','')}|{r.get('question_text_norm','')}|{r.get('metric_type','')}|{r.get('value_pct','')}".encode()
    ).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--issues", required=True)
    ap.add_argument("--dfp-new-issues", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duplicates-out", required=True)
    ap.add_argument("--review-out", required=True)
    ap.add_argument("--merge-candidates-out", required=True)
    ap.add_argument("--report-out", required=True)
    args = ap.parse_args()

    rows, fields = load_csv(Path(args.input))
    issues_rows, _ = load_csv(Path(args.issues))
    dfp_rows, _ = load_csv(Path(args.dfp_new_issues))

    for r in rows:
        r.setdefault("review_reason", "")
        r["data_quality"] = compute_quality(r)
        pct = to_float(r.get("value_pct", ""))
        if pct is None or pct < 0 or pct > 100:
            r["needs_review"] = "true"
            r["review_reason"] = "invalid_value_range"
        if not valid_iso_date(r.get("publish_date", "")):
            r["needs_review"] = "true"
            r["review_reason"] = "invalid_publish_date"
        if not norm(r.get("question_or_message_text", "")):
            r["needs_review"] = "true"
            r["review_reason"] = r.get("review_reason") or "missing_question_text"
        r["row_id"] = stable_row_id(r)

    deduped, duplicates = dedupe_pick(rows)

    existing_keys = set()
    for src in (issues_rows, dfp_rows):
        for r in src:
            existing_keys.add((norm(r.get("source", r.get("source_url", ""))).lower(), norm(r.get("wording", r.get("question_or_message_text", ""))).lower()))

    merge_candidates = []
    review_rows = []
    for r in deduped:
        key = (norm(r.get("source_url", "")).lower(), norm(r.get("question_or_message_text", "")).lower())
        r["existing_overlap"] = "true" if key in existing_keys else "false"
        if r.get("needs_review", "false").lower() == "true":
            review_rows.append(r)
        if r["existing_overlap"] == "false":
            merge_candidates.append(r)

    out_fields = sorted(set(fields + ["data_quality", "dedupe_status", "existing_overlap"]))
    for p, data in [
        (args.out, deduped),
        (args.duplicates_out, duplicates),
        (args.review_out, review_rows),
        (args.merge_candidates_out, merge_candidates),
    ]:
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=out_fields)
            w.writeheader()
            w.writerows(data)

    total = len(rows)
    dedup_n = len(deduped)
    review_n = len(review_rows)
    structured_n = sum(1 for r in deduped if r.get("data_quality") == "structured_poll")
    valid_pct_n = sum(1 for r in deduped if (to_float(r.get("value_pct", "")) is not None and 0 <= to_float(r.get("value_pct", "")) <= 100))
    valid_date_n = sum(1 for r in deduped if valid_iso_date(r.get("publish_date", "")))

    with open(args.report_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["input_rows", total])
        w.writerow(["deduped_rows", dedup_n])
        w.writerow(["duplicate_rows", len(duplicates)])
        w.writerow(["review_queue_rows", review_n])
        w.writerow(["structured_poll_rows", structured_n])
        w.writerow(["valid_value_pct_rows", valid_pct_n])
        w.writerow(["valid_publish_date_rows", valid_date_n])
        w.writerow(["merge_candidates_rows", len(merge_candidates)])


if __name__ == "__main__":
    main()
