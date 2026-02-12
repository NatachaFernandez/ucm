#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.1",
#   "py-markdown-table>=1.3.0"
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

FHIR_NS = "http://hl7.org/fhir"
FHIR_NAMESPACES = {"fhir": FHIR_NS}


@dataclass(frozen=True, slots=True)
class TerminologyMetadata:
    """Metadata extracted from a FHIR terminology resource (NamingSystem, CodeSystem, etc.)."""

    id: str
    title: str
    url: str
    publisher: str
    status: str
    unique_ids: dict[str, str]  # Maps ID type (e.g., "oid", "iri-stem") to value


def get_attr(elem: ET.Element | None, name: str) -> str:
    """Get an attribute value from an XML element, returning empty string if not found."""
    return elem.attrib.get(name, "") if elem is not None else ""


def find_value_attr(root: ET.Element, path: str) -> str:
    """
    Find an element by XPath and return its 'value' attribute.

    This is a convenience function for FHIR XML where most data is in value attributes.
    """
    elem = root.find(path, namespaces=FHIR_NAMESPACES)
    return get_attr(elem, "value")


def extract_metadata(path: Path) -> TerminologyMetadata | None:
    """
    Extract terminology metadata from a FHIR XML file.

    Parses uniqueId and identifier elements to build a map of identifier types to values.
    Returns None if the file cannot be parsed.
    """
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        # Extract uniqueId elements (older FHIR format)
        unique_ids = {
            get_attr(uid.find("fhir:type", namespaces=FHIR_NAMESPACES), "value"):
            get_attr(uid.find("fhir:value", namespaces=FHIR_NAMESPACES), "value")
            for uid in root.findall("fhir:uniqueId", namespaces=FHIR_NAMESPACES)
        }

        # Extract identifier elements (newer FHIR format)
        identifiers = {
            get_attr(ident.find("fhir:type/fhir:coding/fhir:code", namespaces=FHIR_NAMESPACES), "value"):
            get_attr(ident.find("fhir:value", namespaces=FHIR_NAMESPACES), "value")
            for ident in root.findall("fhir:identifier", namespaces=FHIR_NAMESPACES)
        }

        return TerminologyMetadata(
            id=find_value_attr(root, "fhir:id"),
            title=find_value_attr(root, "fhir:title"),
            url=find_value_attr(root, "fhir:url"),
            publisher=find_value_attr(root, "fhir:publisher"),
            status=find_value_attr(root, "fhir:status"),
            unique_ids=unique_ids | identifiers,
        )

    except Exception as exc:
        logger.error(f"Error parsing {path}: {exc}")
        return None


def format_id_type_column(id_type: str) -> str:
    """Format an identifier type as a column name."""
    return f"Unique ID: {id_type}" if id_type else "Unique ID: (none)"


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
            "Source": f"{metadata.id} ({metadata.publisher})",
            "Title": metadata.title,
            "URL": metadata.url,
            "Status": metadata.status,
        }

        # Add identifier columns for this row
        has_identifier = False
        for id_type, value in metadata.unique_ids.items():
            if value:  # Only add non-empty identifiers
                row[format_id_type_column(id_type)] = value
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
        if any(row.get(format_id_type_column(id_type)) for id_type in requested_id_types)
    ]

    # Determine which requested ID types actually appear in the filtered results
    id_types_in_output = {
        id_type for id_type in requested_id_types
        if any(row.get(format_id_type_column(id_type)) for row in filtered_rows)
    }

    return filtered_rows, id_types_in_output


def normalize_rows(rows: list[dict], field_names: list[str]) -> None:
    """
    Normalize rows to have exactly the columns in field_names.

    Removes extra columns and adds missing columns with empty string values.
    Modifies rows in place.
    """
    for row in rows:
        # Remove columns not in field_names
        for key in list(row.keys()):
            if key not in field_names:
                del row[key]

        # Add missing columns with empty values
        for field_name in field_names:
            row.setdefault(field_name, "")


def write_output(rows: list[dict], field_names: list[str], output_file, output_format: str) -> None:
    """Write rows to output file in the specified format."""
    if output_format == 'csv':
        writer = csv.DictWriter(output_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)
    elif output_format == 'markdown':
        output_file.write(
            markdown_table(rows)
            .set_params(row_sep='markdown', quote=False)
            .get_markdown()
        )
    else:
        raise ValueError(f"Unknown output format: {output_format}")


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

    # Convert to table rows
    rows, all_id_types = build_rows(metadata_list)

    # Filter by requested ID types if specified
    filtered_rows, id_types_in_output = filter_rows(rows, all_id_types, id_types)

    logger.info(
        f"Filtered {len(rows)} rows to {len(filtered_rows)} rows "
        f"with ID types: {sorted(id_types_in_output)}"
    )

    # Build field names: base fields + ID type columns
    field_names = ["Source", "Title", "URL", "Status"]
    field_names.extend(format_id_type_column(id_type) for id_type in sorted(id_types_in_output))

    # Normalize rows to have consistent columns
    normalize_rows(filtered_rows, field_names)

    # Write output
    write_output(filtered_rows, field_names, output, output_format)


if __name__ == "__main__":
    generate_index()
