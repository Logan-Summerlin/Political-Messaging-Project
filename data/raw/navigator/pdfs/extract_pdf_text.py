#!/usr/bin/env python3
"""Extract text from Navigator Research PDF toplines using raw PDF parsing."""
import zlib
import re
import sys
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF by decompressing streams and parsing TJ operators."""
    with open(pdf_path, 'rb') as f:
        content = f.read()
    
    # Find all stream...endstream pairs
    pattern = re.compile(rb'stream\r?\n(.+?)\r?\nendstream', re.DOTALL)
    matches = pattern.findall(content)
    
    all_pages_text = []
    page_text = []
    
    for stream_data in matches:
        try:
            decompressed = zlib.decompress(stream_data)
            decoded = decompressed.decode('latin-1')
        except:
            continue
        
        # Skip non-content streams (images, etc.)
        if 'BT' not in decoded and 'TJ' not in decoded:
            continue
        
        # Check for page boundary markers
        if '/Type /Page' in decoded or 'q\n0.00000912 0 612 792 re\nW* n' in decoded:
            if page_text:
                all_pages_text.append('\n'.join(page_text))
                page_text = []
        
        # Extract text from TJ arrays: [(text)] TJ or [(t)5(e)5(xt)] TJ
        # Pattern matches TJ arrays with parenthesized strings
        tj_pattern = re.findall(r'\[(.*?)\]\s*TJ', decoded)
        
        for tj_array in tj_pattern:
            # Extract text from each parenthesized group within the array
            parts = re.findall(r'\(([^)]*)\)', tj_array)
            if parts:
                line = ''.join(parts)
                line = line.strip()
                if line and len(line) > 1:  # Skip single chars
                    page_text.append(line)
        
        # Also extract from Tj operator: (text) Tj
        tj_single = re.findall(r'\(([^)]{2,})\)\s*Tj', decoded)
        for text in tj_single:
            text = text.strip()
            if text:
                page_text.append(text)
    
    if page_text:
        all_pages_text.append('\n'.join(page_text))
    
    return all_pages_text


def extract_all_text_simple(pdf_path):
    """Simpler extraction - just get all text strings from TJ operators."""
    with open(pdf_path, 'rb') as f:
        content = f.read()
    
    pattern = re.compile(rb'stream\r?\n(.+?)\r?\nendstream', re.DOTALL)
    matches = pattern.findall(content)
    
    all_text_lines = []
    
    for stream_data in matches:
        try:
            decompressed = zlib.decompress(stream_data)
            decoded = decompressed.decode('latin-1')
        except:
            continue
        
        # Extract text from TJ operators
        tj_arrays = re.findall(r'\[([^\]]*?)\]\s*TJ', decoded)
        for arr in tj_arrays:
            parts = re.findall(r'\(([^)]*)\)', arr)
            if parts:
                line = ''.join(parts)
                line = line.strip()
                if line and len(line) >= 2:
                    all_text_lines.append(line)
        
        # Tj operators
        tj_single = re.findall(r'\(([^)]{3,})\)\s*Tj', decoded)
        for text in tj_single:
            text = text.strip()
            if text:
                all_text_lines.append(text)
    
    return all_text_lines


if __name__ == '__main__':
    pdf_dir = os.path.dirname(os.path.abspath(__file__))
    
    pdf_files = [
        'Navigator-Topline-F02.02.26.pdf',
        'Navigator-Topline-F10.27.25.pdf',
        'Navigator-April-1-Topline-F04.06.26.pdf',
        'Navigator-Update-02.05.2026.pdf',
        'Navigator-Update-10.30.2025.pdf',
        'Navigator-Update-04.14.2026.pdf',
        'Navigator-Update-4.9.26.pdf',
    ]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if not os.path.exists(pdf_path):
            print(f"SKIPPING: {pdf_file} not found")
            continue
        
        print(f"\n{'='*80}")
        print(f"FILE: {pdf_file}")
        print(f"{'='*80}")
        
        lines = extract_all_text_simple(pdf_path)
        
        output_file = pdf_file.replace('.pdf', '_extracted.txt')
        output_path = os.path.join(pdf_dir, output_file)
        
        with open(output_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
        
        print(f"Extracted {len(lines)} text lines")
        print(f"Saved to: {output_file}")
        
        # Show preview
        print(f"\nPreview (first 30 lines):")
        for line in lines[:30]:
            print(f"  {line}")
        if len(lines) > 30:
            print(f"  ... and {len(lines) - 30} more lines")
