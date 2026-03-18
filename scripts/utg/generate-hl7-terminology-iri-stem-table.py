#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click==8.3.1",
#   "py-markdown-table==1.3.0"
# ]
# ///
"""
Generate an index of HL7 terminology identifiers from UTG XML files.

This script parses FHIR XML files from the HL7 Unified Terminology Governance (UTG)
repository and extracts identifier information (OIDs, IRIs, URIs, etc.) into a
table format (CSV or Markdown).

Example usage:
    uv run generate-hl7-terminology-iri-stem-table.py utg/ -o output.csv
    uv run generate-hl7-terminology-iri-stem-table.py utg/ -o output.md -f markdown
    uv run generate-hl7-terminology-iri-stem-table.py utg/ -o iri-only.csv --id-type iri-stem
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path

import click
import xml.etree.ElementTree as ET
from py_markdown_table.markdown_table import markdown_table

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FHIR namespace information.
FHIR_NS = "http://hl7.org/fhir"
FHIR_NAMESPACES = {"fhir": FHIR_NS}

# Prefix used for uniqueId columns in the output table.
def get_uniqueId_col_name(id_type: str) -> str:
    """Return the column name for an identifier type."""
    return "Unique ID: " + (id_type or "(none)")


@dataclass(frozen=True, slots=True)
class TerminologyMetadata:
    """Metadata extracted from a FHIR terminology resource (NamingSystem, CodeSystem, etc.)."""
    id: str
    title: str
    url: str
    publisher: str
    status: str
    unique_ids: dict[str, list[str]]  # Maps ID type (e.g., "oid", "iri-stem") to list of values


def extract_metadata(path: Path) -> TerminologyMetadata | None:
    """
    Extract terminology metadata from a FHIR XML file.

    Parses uniqueId and identifier elements to build a map of identifier types to values.
    Returns None if the file cannot be parsed.
    """
    try:
        root = ET.parse(path).getroot()

        # Helpers for reading FHIR XML, where data lives in 'value' attributes.
        val = lambda elem: (elem.attrib.get("value", "") if elem is not None else "")
        find = lambda xpath: val(root.find(xpath, FHIR_NAMESPACES))

        # Extract uniqueId elements (older FHIR format).
        unique_ids = {}
        for uid in root.findall("fhir:uniqueId", namespaces=FHIR_NAMESPACES):
            id_type = val(uid.find("fhir:type", namespaces=FHIR_NAMESPACES))
            id_value = val(uid.find("fhir:value", namespaces=FHIR_NAMESPACES))
            unique_ids.setdefault(id_type, []).append(id_value)

        # Extract identifier elements (newer FHIR format), merging on top.
        for ident in root.findall("fhir:identifier", namespaces=FHIR_NAMESPACES):
            id_type = val(ident.find("fhir:type/fhir:coding/fhir:code", namespaces=FHIR_NAMESPACES))
            id_value = val(ident.find("fhir:value", namespaces=FHIR_NAMESPACES))
            unique_ids.setdefault(id_type, []).append(id_value)

        return TerminologyMetadata(
            id=find("fhir:id"),
            title=find("fhir:title"),
            url=find("fhir:url"),
            publisher=find("fhir:publisher"),
            status=find("fhir:status"),
            unique_ids=unique_ids,
        )

    except Exception as exc:
        logger.error(f"Error parsing {path}: {exc}")
        return None


def build_rows(metadata_list: list[TerminologyMetadata]) -> tuple[list[dict], set[str]]:
    """
    Convert metadata objects into table rows.

    Returns:
        A tuple of (rows, all_id_types) where:
        - rows: List of dictionaries suitable for CSV/markdown output
        - all_id_types: Set of all identifier types found across all metadata
    """
    rows = []
    all_id_types = set()

    for metadata in sorted(metadata_list, key=lambda m: m.id):
        # Build base row with standard fields
        row = {
            "Title": metadata.title,
            "Publisher": metadata.publisher,
            "URL": metadata.url,
            "Status": metadata.status,
        }

        # Add identifier columns for this row
        has_identifier = False
        for id_type, values in metadata.unique_ids.items():
            joined = "; ".join(v for v in values if v)
            if joined:
                row[get_uniqueId_col_name(id_type)] = joined
                all_id_types.add(id_type)
                has_identifier = True

        # Only include rows that have at least one non-empty identifier
        if has_identifier:
            rows.append(row)

    return rows, all_id_types


def filter_rows(
    rows: list[dict],
    all_id_types: set[str],
    requested_id_types: tuple[str, ...],
) -> tuple[list[dict], set[str]]:
    """
    Filter rows to only those with requested identifier types.

    Args:
        rows: All rows from build_rows()
        all_id_types: All identifier types found in the data
        requested_id_types: User-requested types to filter by (empty = no filter)

    Returns:
        A tuple of (filtered_rows, id_types_in_output) where:
        - filtered_rows: Rows that match the filter criteria
        - id_types_in_output: Set of ID types that appear in filtered results
    """
    if not requested_id_types:
        return rows, all_id_types

    # Keep rows that have at least one of the requested ID types
    filtered_rows = [
        row for row in rows
        if any(row.get(get_uniqueId_col_name(id_type)) for id_type in requested_id_types)
    ]

    # Determine which requested ID types actually appear in the filtered results
    id_types_in_output = {
        id_type for id_type in all_id_types
        if any(row.get(get_uniqueId_col_name(id_type)) for row in filtered_rows)
    }

    return filtered_rows, id_types_in_output


@click.command()
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option(
    "--output", "-o",
    type=click.File("w", encoding="utf-8"),
    default="-",
    help="Output file (default: stdout)",
)
@click.option(
    '--id-type',
    'id_types',
    multiple=True,
    help='Only include rows with the given identifier type. May be specified multiple times.',
)
@click.option(
    '--format', '-f',
    'output_format',
    type=click.Choice(['csv', 'markdown']),
    default='csv',
    help='Output format',
)
def generate_index(
    paths: tuple[Path, ...],
    id_types: tuple[str, ...],
    output,
    output_format: str,
) -> None:
    """
    Generate an index of identifiers from HL7 UTG directories.

    The HL7 Unified Terminology Governance (UTG) repository is at https://github.com/HL7/UTG

    PATHS may be files or directories. Directories are searched recursively for XML files.
    """
    # Parse all XML files
    metadata_list = []
    for path in paths:
        for filepath in path.rglob("*.xml"):
            metadata = extract_metadata(filepath)
            if metadata is not None:
                metadata_list.append(metadata)

    logger.info(f"Parsed {len(metadata_list)} XML files")

    # Convert to table rows, then filter by requested ID types if specified
    rows, all_id_types = build_rows(metadata_list)
    filtered_rows, id_types_in_output = filter_rows(rows, all_id_types, id_types)

    logger.info(
        f"Filtered {len(rows)} rows to {len(filtered_rows)} rows "
        f"with ID types: {sorted(id_types_in_output)}"
    )

    # Build field names: base fields + sorted ID type columns
    field_names = ["Title", "Publisher", "URL", "Status"]
    field_names.extend(get_uniqueId_col_name(id_type) for id_type in sorted(id_types_in_output))

    # Normalize rows to have exactly the columns in field_names
    for row in filtered_rows:
        for key in list(row.keys()):
            if key not in field_names:
                del row[key]
        for field_name in field_names:
            row.setdefault(field_name, "")

    # Write output
    if output_format == 'csv':
        writer = csv.DictWriter(output, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(filtered_rows)
    elif output_format == 'markdown':
        output.write(
            markdown_table(filtered_rows)
            .set_params(row_sep='markdown', quote=False)
            .get_markdown()
        )
    else:
        raise ValueError(f"Invalid output format: {output_format} (must be 'csv' or 'markdown')")


if __name__ == "__main__":
    generate_index()
