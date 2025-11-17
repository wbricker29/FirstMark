#!/usr/bin/env python3
"""
Airtable Candidate Loader

Loads executive candidates from CSV files into Airtable People table.
Supports flexible CSV schemas, intelligent column mapping, duplicate detection,
and optional bio file loading.

Usage:
    python load_candidates.py <csv_path> [--dry-run] [--verbose]

Examples:
    python load_candidates.py reference/guildmember_scrape.csv
    python load_candidates.py data/executives.csv --dry-run
    python load_candidates.py ../Exec_Network.csv --verbose
"""

import argparse
import csv
import re
import sys
from datetime import date
from difflib import get_close_matches
from pathlib import Path
from typing import Dict, List, Tuple

# Airtable configuration
BASE_ID = "appeY64iIwU5CEna7"
PEOPLE_TABLE_ID = "tblHqYymo3Av9hLeC"

# Field mapping: Airtable field → possible CSV column names
FIELD_MAPPINGS = {
    "name": ["full_name", "name", "executive_name", "candidate_name", "exec_name"],
    "title": ["title_raw", "current_title", "title", "role_title", "position", "role"],
    "company": ["company", "current_company", "organization", "employer"],
    "linkedin_headline": [
        "misc_liheadline",
        "linkedin_headline",
        "headline",
        "description",
    ],
    "linkedin_url": ["linkedin_url", "linkedin", "profile_url", "url"],
    "location": ["location", "city", "region", "geo"],
    "function": [
        "function",
        "role_type",
        "seniority",
        "exec_function",
        "normalized_function",
    ],
    "source": ["source", "data_source", "origin"],
    "bio": ["bio", "biography", "background", "summary"],
}


def detect_csv_schema(csv_path: Path) -> Dict[str, str]:
    """Detect CSV schema and map columns to Airtable fields."""
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        csv_columns = [col.strip().lower() for col in reader.fieldnames]

    schema_map = {}
    for airtable_field, possible_columns in FIELD_MAPPINGS.items():
        for col_option in possible_columns:
            if col_option in csv_columns:
                # Find original case-sensitive column name
                original_col = next(
                    c for c in reader.fieldnames if c.strip().lower() == col_option
                )
                schema_map[airtable_field] = original_col
                break

    return schema_map


def read_csv_flexible(csv_path: Path, schema_map: Dict[str, str]) -> List[Dict]:
    """Read CSV using detected schema mapping."""
    candidates = []

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
            candidate = {"_row_num": row_num}

            # Map CSV columns to standard fields
            for airtable_field, csv_column in schema_map.items():
                value = row.get(csv_column, "").strip()
                candidate[airtable_field] = value

            # Only add if we have at least name
            if candidate.get("name"):
                candidates.append(candidate)

    return candidates


def normalize_name(name: str) -> str:
    """Normalize name for matching (lowercase, remove special chars, collapse spaces)."""
    # Remove common prefixes like "bio_", "exec_"
    name = re.sub(r"^(bio_|exec_|executive_)", "", name, flags=re.IGNORECASE)
    # Convert to lowercase, replace special chars with spaces
    name = re.sub(r"[^a-z0-9\s]", " ", name.lower())
    # Collapse multiple spaces
    name = " ".join(name.split())
    return name


def load_executive_bios(
    csv_dir: Path, candidates: List[Dict], verbose: bool = False
) -> Dict[str, str]:
    """Load executive bios from .txt files, match to candidates by name."""
    bio_files = list(csv_dir.glob("*.txt"))
    bios = {}

    if not bio_files:
        return bios

    if verbose:
        print(f"\n📄 Looking for bio files in {csv_dir}...")
        print(f"   Found {len(bio_files)} .txt files")

    # Create lookup: normalized name → original name
    candidate_names = {normalize_name(c["name"]): c["name"] for c in candidates}

    for bio_file in bio_files:
        filename = bio_file.stem  # Remove .txt extension
        filename_normalized = normalize_name(filename)

        # Try exact match first
        if filename_normalized in candidate_names:
            original_name = candidate_names[filename_normalized]
            bio_content = bio_file.read_text(encoding="utf-8").strip()
            bios[original_name] = bio_content
            if verbose:
                print(f"   ✅ Matched: {bio_file.name} → {original_name}")
            continue

        # Try fuzzy match (for typos, slight variations)
        close_matches = get_close_matches(
            filename_normalized,
            candidate_names.keys(),
            n=1,
            cutoff=0.8,  # 80% similarity threshold
        )

        if close_matches:
            matched_normalized = close_matches[0]
            original_name = candidate_names[matched_normalized]
            bio_content = bio_file.read_text(encoding="utf-8").strip()
            bios[original_name] = bio_content
            if verbose:
                print(f"   ✅ Fuzzy matched: {bio_file.name} → {original_name}")
        else:
            if verbose:
                print(f"   ⏭️  No match: {bio_file.name}")

    return bios


def infer_function(title: str) -> str:
    """Infer Normalized Function from title."""
    title_upper = title.upper()

    # Order matters - check most specific first
    if "CFO" in title_upper or "CHIEF FINANCIAL OFFICER" in title_upper:
        return "CFO"
    elif (
        "CTO" in title_upper
        or "CHIEF TECHNOLOGY OFFICER" in title_upper
        or "CHIEF TECHNICAL OFFICER" in title_upper
    ):
        return "CTO"
    elif "CPO" in title_upper or "CHIEF PRODUCT OFFICER" in title_upper:
        return "CPO"
    elif "CRO" in title_upper or "CHIEF REVENUE OFFICER" in title_upper:
        return "CRO"
    elif "COO" in title_upper or "CHIEF OPERATING OFFICER" in title_upper:
        return "COO"
    elif "CMO" in title_upper or "CHIEF MARKETING OFFICER" in title_upper:
        return "CMO"
    elif "CEO" in title_upper or "CHIEF EXECUTIVE OFFICER" in title_upper:
        return "CEO"
    elif re.search(r"\bFOUNDER\b|\bCO-FOUNDER\b|\bCOFOUNDER\b", title_upper):
        return "CEO"
    else:
        return "Other"


def normalize_source(source: str) -> str:
    """Fix source typos."""
    if source == "FMGUildPage":
        return "FMGuildPage"
    return source


def normalize_candidates(candidates: List[Dict]) -> None:
    """Apply normalization rules to all candidates (in-place)."""
    today = date.today().isoformat()

    for candidate in candidates:
        # Infer function from title if not already set
        if not candidate.get("function"):
            candidate["function"] = infer_function(candidate.get("title", ""))

        # Normalize source
        if candidate.get("source"):
            candidate["source"] = normalize_source(candidate["source"])

        # Set added date
        candidate["added_date"] = today


def check_duplicates(
    candidates: List[Dict], verbose: bool = False
) -> Tuple[List[Dict], List[str]]:
    """
    Check for duplicates against existing Airtable records.
    Returns (new_candidates, duplicate_names).

    Note: This requires Airtable MCP to be available.
    For testing without MCP, this will return all candidates as new.
    """
    try:
        # Import here to avoid hard dependency
        from mcp__airtable__list_records import mcp__airtable__list_records

        existing_people = mcp__airtable__list_records(
            baseId=BASE_ID,
            tableId=PEOPLE_TABLE_ID,
            maxRecords=200,  # Adjust if more than 200 people expected
        )

        existing_names = {
            record["fields"].get("Name", "").lower()
            for record in existing_people
            if "Name" in record["fields"]
        }

        if verbose:
            print(f"\n🔍 Found {len(existing_names)} existing candidates in Airtable")

    except (ImportError, Exception) as e:
        if verbose:
            print(f"\n⚠️  Could not check duplicates: {e}")
            print("   Proceeding without duplicate detection...")
        existing_names = set()

    new_candidates = []
    duplicates = []

    for candidate in candidates:
        name_lower = candidate["name"].lower()
        if name_lower in existing_names:
            duplicates.append(candidate["name"])
        else:
            new_candidates.append(candidate)

    return new_candidates, duplicates


def create_airtable_records(
    candidates: List[Dict], dry_run: bool = False, verbose: bool = False
) -> Tuple[int, int, List[str]]:
    """
    Create Airtable records for candidates.
    Returns (created_count, error_count, error_messages).
    """
    if dry_run:
        print("\n🔍 DRY RUN MODE - No records will be created")
        return 0, 0, []

    try:
        # Import here to avoid hard dependency
        from mcp__airtable__create_record import mcp__airtable__create_record
    except ImportError:
        print("\n❌ ERROR: Airtable MCP not available")
        print("   Install Airtable MCP server to create records")
        return 0, len(candidates), ["Airtable MCP not available"]

    created_count = 0
    error_count = 0
    errors = []

    # Known valid options (from demo schema)
    VALID_FUNCTIONS = {"CFO", "CTO"}
    VALID_SOURCES = {"FMGuildPage", "FMLinkedIN"}

    for idx, candidate in enumerate(candidates, start=1):
        try:
            # Build fields dict - only required fields
            fields = {"Name": candidate["name"], "Added Date": candidate["added_date"]}

            # Add optional fields if present
            if candidate.get("title"):
                fields["Current Title"] = candidate["title"]

            if candidate.get("company"):
                fields["Current Company"] = candidate["company"]

            if candidate.get("linkedin_headline"):
                fields["LinkedIn Headline"] = candidate["linkedin_headline"]

            if candidate.get("linkedin_url"):
                fields["LinkedIn URL"] = candidate["linkedin_url"]

            if candidate.get("location"):
                fields["Location"] = candidate["location"]

            if candidate.get("bio"):
                fields["Bio"] = candidate["bio"]

            # Only set single-select fields if value is in valid set
            if candidate.get("function") in VALID_FUNCTIONS:
                fields["Normalized Function"] = candidate["function"]
            elif verbose and candidate.get("function"):
                print(
                    f"   ⚠️  Skipping Normalized Function '{candidate['function']}' for {candidate['name']} (not in schema)"
                )

            if candidate.get("source") in VALID_SOURCES:
                fields["Source"] = candidate["source"]
            elif verbose and candidate.get("source"):
                print(
                    f"   ⚠️  Skipping Source '{candidate['source']}' for {candidate['name']} (not in schema)"
                )

            # Create record
            result = mcp__airtable__create_record(
                baseId=BASE_ID, tableId=PEOPLE_TABLE_ID, fields=fields
            )

            created_count += 1
            print(f"  ✅ {idx}/{len(candidates)}: {candidate['name']}")

        except Exception as e:
            error_count += 1
            error_msg = f"{candidate['name']}: {str(e)}"
            errors.append(error_msg)
            print(f"  ❌ Error: {error_msg}")

    return created_count, error_count, errors


def main():
    parser = argparse.ArgumentParser(
        description="Load executive candidates from CSV into Airtable People table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s reference/guildmember_scrape.csv
  %(prog)s data/executives.csv --dry-run
  %(prog)s ../Exec_Network.csv --verbose
        """,
    )
    parser.add_argument("csv_path", type=str, help="Path to CSV file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without creating records",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed progress"
    )

    args = parser.parse_args()

    csv_path = Path(args.csv_path)

    # Validate CSV exists
    if not csv_path.exists():
        print(f"❌ ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    print("🚀 Airtable Candidate Loader")
    print("=" * 60)
    print(f"CSV: {csv_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)

    # Step 1: Detect schema
    print("\n📋 Step 1: Detecting CSV schema...")
    schema_map = detect_csv_schema(csv_path)

    if args.verbose:
        print("   Schema mapping:")
        for at_field, csv_col in schema_map.items():
            print(f"     {at_field} ← {csv_col}")

    missing_fields = [f for f in ["name", "title", "company"] if f not in schema_map]
    if missing_fields:
        print(f"   ⚠️  Missing required fields: {', '.join(missing_fields)}")
        print("   CSV may not be compatible")

    # Step 2: Read CSV
    print("\n📖 Step 2: Reading CSV...")
    candidates = read_csv_flexible(csv_path, schema_map)
    print(f"   Read {len(candidates)} candidates")

    # Step 3: Load bios
    print("\n📄 Step 3: Loading bio files...")
    bios = load_executive_bios(csv_path.parent, candidates, args.verbose)

    # Attach bios to candidates
    for candidate in candidates:
        if candidate["name"] in bios:
            candidate["bio"] = bios[candidate["name"]]

    print(f"   Loaded {len(bios)} bios")

    # Step 4: Normalize data
    print("\n🔄 Step 4: Normalizing data...")
    normalize_candidates(candidates)
    print("   ✅ Normalized all candidates")

    # Step 5: Check duplicates
    print("\n🔍 Step 5: Checking for duplicates...")
    new_candidates, duplicates = check_duplicates(candidates, args.verbose)
    print(f"   🆕 {len(new_candidates)} new candidates")
    print(f"   ⏭️  {len(duplicates)} duplicates")

    if args.dry_run and duplicates and args.verbose:
        print("\n   Duplicates to skip:")
        for dup in duplicates[:5]:
            print(f"     - {dup}")
        if len(duplicates) > 5:
            print(f"     ... and {len(duplicates) - 5} more")

    # Step 6: Create records
    if new_candidates:
        print(f"\n💾 Step 6: {'Previewing' if args.dry_run else 'Creating'} records...")

        if args.dry_run:
            print(f"   Would create {len(new_candidates)} records:")
            for candidate in new_candidates[:10]:
                print(
                    f"     - {candidate['name']} ({candidate.get('title', 'No title')})"
                )
            if len(new_candidates) > 10:
                print(f"     ... and {len(new_candidates) - 10} more")

            created_count = 0
            error_count = 0
            errors = []
        else:
            created_count, error_count, errors = create_airtable_records(
                new_candidates, dry_run=args.dry_run, verbose=args.verbose
            )
    else:
        print("\n✅ No new candidates to import")
        created_count = error_count = 0
        errors = []

    # Final summary
    print(f"\n{'=' * 60}")
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Created: {created_count} records")
    print(f"⏭️  Skipped (duplicates): {len(duplicates)}")
    print(f"❌ Errors: {error_count}")
    print("=" * 60)

    if errors and args.verbose:
        print("\n❌ Errors:")
        for err in errors[:5]:
            print(f"  - {err}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")

    if not args.dry_run and created_count > 0:
        print("\n✅ Import complete! Check Airtable People table.")
    elif args.dry_run:
        print("\n🔍 Dry run complete. Re-run without --dry-run to create records.")

    # Exit with error code if there were errors
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
