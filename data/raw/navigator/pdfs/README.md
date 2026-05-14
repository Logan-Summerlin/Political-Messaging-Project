# Navigator Research PDF Topline Files

## Summary

Downloaded and extracted text from **12 Navigator Research PDFs** (8 toplines + 4 graph decks) covering polls from April 2025 through April 2026.

## Files Downloaded

### Topline PDFs (raw crosstab data)

| File | Date | Pages | Source Article |
|------|------|-------|---------------|
| `Navigator-Topline-F04.07.25.pdf` | Apr 7, 2025 | ~39 | (general polling) |
| `Navigator-Topline-F07.21.25.pdf` | Jul 21, 2025 | (not downloaded) | |
| `Navigator-Update-Topline-F09.08.25.pdf` | Sep 8, 2025 | ~39 | |
| `Navigator-Topline-F10.20.25.pdf` | Oct 20, 2025 | (not downloaded) | |
| `Navigator-Topline-F10.27.25.pdf` | Oct 27, 2025 | 31 | Government shutdown week 4 |
| `Navigator-Topline-F12.08.25-1.pdf` | Dec 8, 2025 | ~51 | |
| `Navigator-January-1-Topline-F01.12.26.pdf` | Jan 12, 2026 | ~39 | |
| `Navigator-Topline-F02.02.26.pdf` | Feb 2, 2026 | 51 | All eyes are on ICE |
| `Navigator-Toplines-03.16.2026.pdf` | Mar 16, 2026 | ~39 | |
| `Navigator-April-1-Topline-F04.06.26.pdf` | Apr 6, 2026 | 39 | Tax policies / Iran war |

### Graph Decks (presentation-style summaries)

| File | Date | Pages | Topic |
|------|------|-------|-------|
| `Navigator-Update-10.30.2025.pdf` | Oct 30, 2025 | 11 | Government shutdown messaging |
| `Navigator-Update-02.05.2026.pdf` | Feb 5, 2026 | 29 | ICE / Immigration messaging |
| `Navigator-Update-04.14.2026.pdf` | Apr 14, 2026 | 9 | Tax policy messaging |
| `Navigator-Update-4.9.26.pdf` | Apr 9, 2026 | 17 | Iran war messaging |

## Text Extraction Results

**Method:** Raw PDF stream decompression + TJ operator parsing (no external libraries needed)
**Result:** All PDFs contain embedded text that can be extracted. The toplines have rich crosstab data with demographic breakdowns.

### Extraction File Sizes

| Extracted Text File | Lines | Size |
|---------------------|-------|------|
| Navigator-Topline-F02.02.26_extracted.txt | 15,853 | 200K |
| Navigator-Topline-F10.27.25_extracted.txt | 8,647 | 142K |
| Navigator-April-1-Topline-F04.06.26_extracted.txt | 14,155 | 205K |
| Navigator-January-1-Topline-F01.12.26_extracted.txt | 15,135 | 200K |
| Navigator-Toplines-03.16.2026_extracted.txt | 13,548 | 186K |
| Navigator-Topline-F12.08.25-1_extracted.txt | 15,161 | 200K |
| Navigator-Topline-F09.08.25_extracted.txt | 13,791 | 196K |
| Navigator-Topline-F04.07.25_extracted.txt | 14,057 | 198K |
| Navigator-Update-02.05.2026_extracted.txt | 1,810 | 35K |
| Navigator-Update-4.9.26_extracted.txt | 1,109 | 20K |
| Navigator-Update-10.30.2025_extracted.txt | 767 | 16K |
| Navigator-Update-04.14.2026_extracted.txt | 431 | 11K |

### Content Quality

**Toplines (excellent):** Rich crosstab data with demographic breakdowns (Dem, Ind, Rep, Afr Am, Hisp, White, AAPI). Questions include approval ratings, issue support/oppose, message testing, and policy preferences. Data includes percentage values alongside each response option. Minor formatting artifacts from PDF layout (dots for spacing, occasional split numbers).

**Graph decks (good):** Summary-level text with key takeaways, messaging recommendations, and some percentage data. Cleaner but less granular than toplines.

## Message Testing Data Found

Key message testing data successfully extracted includes:

### ICE / Immigration (Feb 2026)
- Trump immigration approval net -12
- 59% oppose ICE deployment
- 52% disapprove mass deportation plan
- Support for balanced approach: 66%
- CBP and ICE favorability ratings
- Support/oppose for impeachment of Noem, firing of Miller, abolishing ICE
- Full demographic crosstabs

### Government Shutdown (Oct 2025)
- Opposition to $170M private jets: 76%
- Opposition to $300M ballroom: 70%
- Opposition to $4.5T tax cuts: 72%
- Opposition to $40B Argentina bailout: 76%
- Pre/post-message shifts on "Republicans focused on wrong things"
- Republican opposition to specific items

### Tax Policies (Apr 2026)
- Republican tax law net -13 favorability
- 48% say law doesn't benefit middle class
- 44% agree costs outweigh benefits
- Trust on taxes: Dems 34% vs GOP 34%
- Filed vs unfiled taxpayer responses

### Iran War (Apr 2026)
- Oppose: 50% vs Support: 40% (net -10)
- 70% concerned about prolonged conflict
- 58% oppose $200B additional funding
- 64% oppose ground war
- Top descriptors: expensive (30%), war of choice (29%), dangerous (28%)

## Technical Notes

- All PDFs are PDF 1.7 format with FlateDecode-compressed streams
- Text is embedded in TJ operator arrays with kerning adjustments
- No OCR needed - all text is directly extractable from PDF streams
- The graph decks have less data but cleaner text
- pdftotext and pymupdf not available in this environment; extraction done via pure Python zlib + regex
