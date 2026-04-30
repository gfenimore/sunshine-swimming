#!/usr/bin/env python3
"""
Sunshine Swimming — Client Data Scrub
Converts Amanda's Google Form export (xlsx) to a HoneyBook-ready CSV.

Usage:
    python3 scrub-client-data.py [input.xlsx] [output.csv]

Defaults:
    input:  ../../data/raw/Swimmer_Questionnaire___Sunshine_Swimming_Responses.xlsx
    output: ../../data/processed/honeybook-import.csv
"""

import csv
import re
import sys
import os
from datetime import datetime

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl required. Run: pip install openpyxl")
    sys.exit(1)


# ── Config ──────────────────────────────────────────────────────
DEFAULT_INPUT = os.path.join(os.path.dirname(__file__), 
    "../../data/raw/Swimmer_Questionnaire___Sunshine_Swimming_Responses.xlsx")
DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__),
    "../../data/processed/honeybook-import.csv")

# HoneyBook CSV columns
HB_COLUMNS = ["name", "email", "phone", "address", "notes"]


# ── Helpers ─────────────────────────────────────────────────────
def clean_phone(raw):
    """Normalize phone numbers to (XXX) XXX-XXXX format."""
    if not raw:
        return ""
    
    # Convert floats (Google Sheets exports numbers as floats)
    if isinstance(raw, float):
        raw = str(int(raw))
    
    raw = str(raw).strip()
    
    # Handle multiple numbers separated by / or ;
    # Keep the first one, note the rest
    parts = re.split(r'[/;]', raw)
    primary = parts[0].strip()
    
    # Extract digits only
    digits = re.sub(r'\D', '', primary)
    
    # Handle 10-digit US numbers
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    elif len(digits) >= 7:
        return primary  # Return as-is if we can't parse it
    
    return raw


def clean_text(val):
    """Clean a cell value to a string, handling None/NaN/float."""
    if val is None:
        return ""
    if isinstance(val, float):
        if val != val:  # NaN check
            return ""
        if val == int(val):
            return str(int(val))
        return str(val)
    return str(val).strip()


def format_birthday(val):
    """Format birthday as a readable string."""
    if not val:
        return ""
    if isinstance(val, datetime):
        return val.strftime("%m/%d/%Y")
    return clean_text(val)


def build_notes(row_data):
    """Combine swimmer details into a structured notes block."""
    lines = []
    
    if row_data.get("swimmer_name"):
        lines.append(f"Swimmer: {row_data['swimmer_name']}")
    if row_data.get("birthday"):
        lines.append(f"Birthday: {row_data['birthday']}")
    if row_data.get("comfort_level"):
        lines.append(f"Comfort level: {row_data['comfort_level']}")
    if row_data.get("previous_lessons"):
        lines.append(f"Previous lessons: {row_data['previous_lessons']}")
    if row_data.get("medical"):
        lines.append(f"Medical/allergies: {row_data['medical']}")
    if row_data.get("injuries"):
        lines.append(f"Prior injuries: {row_data['injuries']}")
    if row_data.get("additional_swimmers"):
        lines.append(f"Additional swimmers: {row_data['additional_swimmers']}")
    if row_data.get("lesson_location"):
        lines.append(f"Lesson location: {row_data['lesson_location']}")
    if row_data.get("contact_method"):
        lines.append(f"Preferred contact: {row_data['contact_method']}")
    if row_data.get("text_reminders"):
        lines.append(f"Text reminders: {row_data['text_reminders']}")
    if row_data.get("preferred_times"):
        lines.append(f"Schedule notes: {row_data['preferred_times']}")
    if row_data.get("anything_else"):
        lines.append(f"Other: {row_data['anything_else']}")
    if row_data.get("referral_source"):
        lines.append(f"Heard about us: {row_data['referral_source']}")
    if row_data.get("submitted_at"):
        lines.append(f"Form submitted: {row_data['submitted_at']}")
    
    return " | ".join(lines) if lines else ""


# ── Column Mapping ──────────────────────────────────────────────
# Maps xlsx column letters to our internal field names
# Based on actual spreadsheet analysis
COLUMN_MAP = {
    'A': 'submitted_at',      # Timestamp
    'B': 'swimmer_name',       # Swimmer Name
    'C': 'additional_swimmers',# Additional Swimmers
    'D': 'birthday',           # Birthday
    'E': '_skip',              # Column 19 (empty)
    'F': 'parent_name',        # Parent/Guardian Name(s)
    'G': 'phone',              # Phone Number
    'H': 'email',              # Email
    'I': 'address',            # Home Address
    'J': 'lesson_location',    # Lesson location if different
    'K': 'contact_method',     # Best Contact Method
    'L': 'text_reminders',     # Text reminders preference
    'M': 'previous_lessons',   # Previous swim lessons
    'N': 'comfort_level',      # Comfort level 1-5
    'O': 'medical',            # Medical conditions
    'P': 'injuries',           # Prior injuries
    'Q': 'preferred_times',    # Preferred days/times
    'R': 'anything_else',      # Anything else
    'S': 'referral_source',    # How did you hear about us
}


# ── Main ────────────────────────────────────────────────────────
def scrub(input_path, output_path):
    print(f"📂 Reading: {input_path}")
    
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    
    rows_processed = 0
    rows_skipped = 0
    records = []
    seen_emails = set()
    
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
        # Build row data dict
        row_data = {}
        for cell in row:
            col_letter = cell.column_letter
            field = COLUMN_MAP.get(col_letter)
            if field and field != '_skip':
                if field == 'birthday':
                    row_data[field] = format_birthday(cell.value)
                elif field == 'comfort_level' and isinstance(cell.value, float):
                    row_data[field] = str(int(cell.value))
                elif field == 'submitted_at' and isinstance(cell.value, datetime):
                    row_data[field] = cell.value.strftime("%Y-%m-%d")
                else:
                    row_data[field] = clean_text(cell.value)
        
        # Skip rows without email (HB import requirement)
        email = row_data.get('email', '').strip()
        if not email or '@' not in email:
            rows_skipped += 1
            continue
        
        # Deduplicate by email (keep first occurrence)
        email_lower = email.lower()
        if email_lower in seen_emails:
            rows_skipped += 1
            continue
        seen_emails.add(email_lower)
        
        # Build the HB record
        parent_name = row_data.get('parent_name', '')
        if not parent_name:
            # Fallback: use part before @ in email
            parent_name = email.split('@')[0].replace('.', ' ').title()
        
        record = {
            'name': parent_name,
            'email': email,
            'phone': clean_phone(row_data.get('phone', '')),
            'address': row_data.get('address', ''),
            'notes': build_notes(row_data),
        }
        
        records.append(record)
        rows_processed += 1
    
    # Write CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HB_COLUMNS)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"✅ Processed: {rows_processed} contacts")
    print(f"⏭️  Skipped: {rows_skipped} (no email or duplicate)")
    print(f"📄 Output: {output_path}")
    
    # Summary stats
    phones_formatted = sum(1 for r in records if r['phone'])
    addresses_present = sum(1 for r in records if r['address'])
    print(f"\n📊 Data quality:")
    print(f"   Phone numbers: {phones_formatted}/{rows_processed}")
    print(f"   Addresses: {addresses_present}/{rows_processed}")
    
    return records


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    output_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        print(f"   Place Amanda's xlsx in data/raw/ or pass the path as an argument.")
        sys.exit(1)
    
    scrub(input_file, output_file)
