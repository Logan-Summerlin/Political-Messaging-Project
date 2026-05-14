#!/usr/bin/env python3
"""Phase 4 resolver for DFP topline extraction.

Maps percentage claims to the most likely tested question/prompt clause while
preserving alternate candidates for auditability.
"""

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

PERCENT_RE = re.compile(r"\b(\d{1,3}(?:\.\d+)?)\s?%\b")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
CLAUSE_SPLIT_RE = re.compile(r"[;:\u2014]|\s+-\s+")
SUPPORT_CUES = {"support", "back", "favor", "approve"}
OPPOSE_CUES = {"oppose", "against", "reject", "disapprove"}
TOPLINE_CUES = {"topline", "methodology", "crosstab", "memo", "poll found"}
PROMPT_PATTERNS = [
    re.compile(r'"([^"]{20,400})"'),
    re.compile(r"'([^']{20,400})'"),
    re.compile(r"whether\s+[^.?!]{15,280}", re.I),
    re.compile(r"(support(?:ing)?\s+[^.?!]{10,220})", re.I),
    re.compile(r"(oppose(?:d|s|ing)?\s+[^.?!]{10,220})", re.I),
]


@dataclass
class Candidate:
    text: str
    score: float
    reason: str


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def normalize_question(text: str) -> str:
    text = normalize_text(text).lower()
    text = re.sub(r"^[\W_]*(whether they|whether voters|voters|respondents)\s+", "", text)
    text = text.strip(" .,:;\"'()[]")
    return text


def metric_from_context(context: str) -> str:
    lc = context.lower()
    if any(c in lc for c in SUPPORT_CUES):
        return "support"
    if any(c in lc for c in OPPOSE_CUES):
        return "oppose"
    if "concern" in lc or "worried" in lc:
        return "concern"
    if "agree" in lc:
        return "agreement"
    return "other"


def sentence_candidates(sentence: str, prev_sentence: str, is_lead: bool) -> List[Candidate]:
    cands: List[Candidate] = []
    searchable = [sentence, prev_sentence] if prev_sentence else [sentence]
    for src_idx, src in enumerate(searchable):
        if not src:
            continue
        for patt in PROMPT_PATTERNS:
            for m in patt.finditer(src):
                txt = normalize_text(m.group(1) if m.groups() else m.group(0))
                if len(txt) < 18:
                    continue
                score = 0.25
                reasons = []
                if src_idx == 0:
                    score += 0.35
                    reasons.append("same_sentence")
                else:
                    score += 0.12
                    reasons.append("previous_sentence")
                if is_lead:
                    score += 0.10
                    reasons.append("lead_paragraph")
                if '"' in src or "'" in src:
                    score += 0.15
                    reasons.append("quoted_prompt")
                cands.append(Candidate(txt, score, "+".join(reasons)))

    for clause in CLAUSE_SPLIT_RE.split(sentence):
        clause = normalize_text(clause)
        if len(clause) < 20:
            continue
        if any(x in clause.lower() for x in ["support", "oppose", "whether", "should", "policy"]):
            bonus = 0.20 + (0.10 if is_lead else 0)
            cands.append(Candidate(clause, bonus, "policy_clause"))
    return cands


def resolve_row(row: dict, article_text: str) -> Tuple[dict, List[dict]]:
    val = row.get("value_text_raw", "")
    src = row.get("extraction_source", "")
    metric = row.get("metric_type", "other")
    sentences = SENTENCE_SPLIT_RE.split(article_text)

    evidence = row.get("evidence_snippet", "")
    best_idx = -1
    for i, s in enumerate(sentences):
        if evidence and evidence[:30] in s:
            best_idx = i
            break
        if val and val in s:
            best_idx = i
            break

    target_sentence = sentences[best_idx] if best_idx >= 0 else evidence
    prev_sentence = sentences[best_idx - 1] if best_idx > 0 else ""
    is_lead = best_idx in {0, 1, 2}

    candidates = sentence_candidates(target_sentence, prev_sentence, is_lead)
    ranked = []
    for c in candidates:
        score = c.score
        lc = c.text.lower()
        if metric == "support" and any(k in lc for k in SUPPORT_CUES):
            score += 0.25
        if metric == "oppose" and any(k in lc for k in OPPOSE_CUES):
            score += 0.25
        if metric == "other":
            score -= 0.10
        if any(k in lc for k in TOPLINE_CUES):
            score += 0.10
        if len(c.text) > 280:
            score -= 0.15
        ranked.append((score, c))

    ranked.sort(key=lambda x: x[0], reverse=True)

    selected_text = row.get("question_or_message_text", "")
    confidence = float(row.get("confidence_score", "0") or 0)
    review_reason = row.get("review_reason", "")
    needs_review = row.get("needs_review", "true").lower() == "true"

    audit_records = []
    for idx, (score, cand) in enumerate(ranked[:5], start=1):
        audit_records.append(
            {
                "row_id": row.get("row_id", ""),
                "candidate_rank": idx,
                "candidate_text": cand.text,
                "candidate_score": f"{score:.3f}",
                "candidate_reason": cand.reason,
            }
        )

    if ranked:
        top_score, top = ranked[0]
        selected_text = top.text
        confidence = max(confidence, min(1.0, top_score))
        if top_score < 0.60:
            needs_review = True
            review_reason = "phase4_low_binding_score"
    else:
        needs_review = True
        review_reason = review_reason or "phase4_no_candidates"

    row["question_or_message_text"] = selected_text
    row["question_text_norm"] = normalize_question(selected_text)
    row["confidence_score"] = f"{confidence:.2f}"
    row["needs_review"] = str(needs_review).lower()
    row["review_reason"] = review_reason
    row["resolver_phase4_applied"] = "true"
    row["resolver_source_layer"] = src
    row["row_id"] = hashlib.sha1(
        f"{row.get('source_url','')}|{row['question_text_norm']}|{row.get('metric_type','')}|{row.get('value_pct','')}".encode()
    ).hexdigest()

    return row, audit_records


def load_article_text_map(html_root: Path) -> dict:
    text_map = {}
    for hp in sorted(html_root.rglob("*.html")):
        body = hp.read_text(encoding="utf-8", errors="replace")
        body = re.sub(r"<script[\s\S]*?</script>", " ", body, flags=re.I)
        body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)
        body = re.sub(r"<[^>]+>", " ", body)
        body = normalize_text(body)
        meta = hp.with_suffix(".http.json")
        url = ""
        if meta.exists():
            try:
                data = json.loads(meta.read_text(encoding="utf-8"))
                url = data.get("url") or data.get("final_url") or ""
            except Exception:
                pass
        if url:
            text_map[url] = body
    return text_map


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Phase 3 CSV input")
    ap.add_argument("--html-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audit-out", required=True)
    args = ap.parse_args()

    text_map = load_article_text_map(Path(args.html_root))

    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []

    extra = ["resolver_phase4_applied", "resolver_source_layer"]
    out_fields = fields + [x for x in extra if x not in fields]
    audit_fields = ["row_id", "candidate_rank", "candidate_text", "candidate_score", "candidate_reason"]

    resolved_rows = []
    audits = []
    for row in rows:
        article_text = text_map.get(row.get("source_url", ""), row.get("evidence_snippet", ""))
        resolved, candidates = resolve_row(row, article_text)
        resolved_rows.append(resolved)
        audits.extend(candidates)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        w.writerows(resolved_rows)

    with open(args.audit_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=audit_fields)
        w.writeheader()
        w.writerows(audits)


if __name__ == "__main__":
    main()
