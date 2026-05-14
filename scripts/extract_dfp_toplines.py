#!/usr/bin/env python3
import argparse, csv, hashlib, json, re
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

PARSER_VERSION_DEFAULT = "2.0.0"
WORD_NUMS = {"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,"hundred":100}
NUM_RE = re.compile(r"\b(\d{1,3}(?:\.\d+)?)\s?%")
WORD_PERCENT_RE = re.compile(r"\b([a-z\-\s]{2,40})\s+percent\b", re.I)

class DFPHTML(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=""; self.in_title=False; self.meta={}; self.jsonld=[]; self.text=[]; self.skip=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="title": self.in_title=True
        if tag in {"script","style","nav","footer"}: self.skip=True
        if tag=="meta":
            k=(a.get("property") or a.get("name") or "").lower(); v=a.get("content")
            if k and v: self.meta[k]=v
        if tag=="script" and a.get("type","").lower()=="application/ld+json": self._json_capture=True; self._json_buf=[]
    def handle_endtag(self, tag):
        if tag=="title": self.in_title=False
        if tag in {"script","style","nav","footer"}: self.skip=False
        if tag=="script" and hasattr(self,"_json_capture") and self._json_capture:
            self.jsonld.append("".join(self._json_buf)); self._json_capture=False
    def handle_data(self,data):
        d=data.strip()
        if not d: return
        if self.in_title: self.title += d
        if hasattr(self,"_json_capture") and self._json_capture: self._json_buf.append(d)
        if not self.skip: self.text.append(d)

def word_to_num(txt):
    txt = txt.lower().replace("-"," ")
    total=0
    for t in txt.split():
        if t not in WORD_NUMS: continue
        v=WORD_NUMS[t]
        if v==100 and total>0: total*=100
        else: total+=v
    return float(total) if total else None

def normalize_q(t):
    t=unescape(t.lower())
    t=re.sub(r"^[\W_]*(whether they|voters|respondents)\s+", "", t)
    t=re.sub(r"\s+", " ", t).strip(" .,:;\"'()[]")
    return t

def detect_metric(window):
    w=window.lower()
    if any(x in w for x in ["support","back","favor"]): return "support"
    if any(x in w for x in ["oppose","against","reject"]): return "oppose"
    if "concern" in w or "worried" in w: return "concern"
    if "agree" in w: return "agreement"
    return "other"

def parse_jsonld_date(objs):
    for raw in objs:
        try:
            obj=json.loads(raw)
            if isinstance(obj,list): items=obj
            else: items=[obj]
            for it in items:
                d=it.get("datePublished")
                if d: return d[:10]
        except Exception:
            pass
    return ""

def extract_from_text(source_url, title, publish_date, text, layer, parser_version):
    rows=[]; review=[]
    sentences=re.split(r"(?<=[\.!?])\s+", text)
    for s in sentences:
        for m in NUM_RE.finditer(s):
            pct=float(m.group(1)); raw=m.group(0)
            if pct<0 or pct>100: continue
            st=max(0,m.start()-120); en=min(len(s), m.end()+120)
            win=s[st:en]
            metric=detect_metric(win)
            q=s.strip()
            conf=0.45
            if metric!="other": conf += 0.25
            if '"' in s or "'" in s: conf += 0.15
            if layer!="article_body": conf -= 0.15
            needs=conf<0.70 or metric=="other"
            reason="low_confidence" if conf<0.70 else ("metric_other" if metric=="other" else "")
            qn=normalize_q(q)
            row_id=hashlib.sha1(f"{source_url}|{qn}|{metric}|{pct}".encode()).hexdigest()
            row={"row_id":row_id,"source_url":source_url,"publish_date":publish_date,"title":title,"question_or_message_text":q,"question_text_norm":qn,"metric_type":metric,"value_pct":f"{pct:.2f}","value_text_raw":raw,"population":"","sample_size_n":"","field_dates":"","mode":"","moe_pct":"","geography":"","party_breakout":"","extraction_source":layer,"evidence_snippet":win[:400],"evidence_char_start":str(st),"evidence_char_end":str(en),"confidence_score":f"{conf:.2f}","needs_review":str(needs).lower(),"review_reason":reason,"parser_version":parser_version,"extracted_at_utc":datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
            rows.append(row)
            if needs: review.append(row)
        for m in WORD_PERCENT_RE.finditer(s):
            n=word_to_num(m.group(1));
            if n is None or n>100: continue
    return rows, review

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--html-root", required=True)
    ap.add_argument("--asset-root")
    ap.add_argument("--out", required=True)
    ap.add_argument("--review-out", required=True)
    ap.add_argument("--parser-version", default=PARSER_VERSION_DEFAULT)
    ap.add_argument("--use-assets", action="store_true")
    ap.add_argument("--min-confidence", type=float, default=0.0)
    ap.add_argument("--max-articles", type=int)
    ap.add_argument("--write-audit-sidecar", action="store_true")
    args=ap.parse_args()

    fields=["row_id","source_url","publish_date","title","question_or_message_text","question_text_norm","metric_type","value_pct","value_text_raw","population","sample_size_n","field_dates","mode","moe_pct","geography","party_breakout","extraction_source","evidence_snippet","evidence_char_start","evidence_char_end","confidence_score","needs_review","review_reason","parser_version","extracted_at_utc"]
    all_rows=[]; review=[]
    html_files=sorted(Path(args.html_root).rglob("*.html"))
    if args.max_articles: html_files=html_files[:args.max_articles]
    for hp in html_files:
        raw=hp.read_text(encoding="utf-8", errors="replace")
        p=DFPHTML(); p.feed(raw)
        meta_path=hp.with_suffix(".http.json")
        source_url=""
        if meta_path.exists():
            try: source_url=json.loads(meta_path.read_text(encoding='utf-8')).get("url","")
            except Exception: pass
        source_url=source_url or p.meta.get("og:url","")
        pub=parse_jsonld_date(p.jsonld)
        if not pub: pub=""
        title=p.title or p.meta.get("og:title","")
        body=" ".join(p.text)
        rows1, rev1 = extract_from_text(source_url,title,pub,body,"article_body",args.parser_version)
        desc=p.meta.get("description") or p.meta.get("og:description") or ""
        rows2, rev2 = extract_from_text(source_url,title,pub,desc,"meta_description",args.parser_version)
        all_rows.extend(rows1+rows2); review.extend(rev1+rev2)

    dedup={}
    for r in all_rows:
        k=(r["source_url"],r["question_text_norm"],r["metric_type"],r["value_pct"])
        if float(r["confidence_score"]) < args.min_confidence: continue
        if k not in dedup or float(r["confidence_score"])>float(dedup[k]["confidence_score"]): dedup[k]=r
    final=list(dedup.values())

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(final)
    with open(args.review_out,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(review)

if __name__=="__main__": main()
