#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.1",
#   "py-markdown-table>=1.3.0"
# ]
# ///

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import click
from py_markdown_table.markdown_table import markdown_table
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FHIR_NS = "http://hl7.org/fhir"

@dataclass(slots=True)
class Result:
    file: Path
    root_label: str
    id: str
    url: str
    unique_ids: dict[str, str]
    description: str
    publisher: str
    status: str

    @property
    def root_label_without_namespace(self):
        if self.root_label.startswith("{" + FHIR_NS + "}"):
            return self.root_label[len(FHIR_NS) + 2:]
        return self.root_label

    @property
    def description_field(self) -> str:
        """Collapse whitespace like the Scala regex."""
        return " ".join(self.description.split())

# ---------- XML helpers ----------

def attr(elem: ET.Element | None, name: str) -> str:
    return elem.attrib.get(name, "") if elem is not None else ""


def find_attr(root: ET.Element, path: str, name: str = "value", namespaces=None) -> str:
    if namespaces is None:
        namespaces = {"fhir": FHIR_NS}
    return attr(root.find(path, namespaces=namespaces), name)


# ---------- indexing ----------

def index_file(path: Path, namespaces=None) -> Result | None:
    if namespaces is None:
        namespaces = {"fhir": FHIR_NS}
    try:
        with open(path, "r") as file:
            tree = ET.parse(file)
            root = tree.getroot()

            unique_ids = {
                attr(uid.find("fhir:type", namespaces=namespaces), "value"): attr(uid.find("fhir:value", namespaces=namespaces), "value")
                for uid in root.findall("fhir:uniqueId", namespaces=namespaces)
            }

            identifiers = {
                attr(ident.find("fhir:type/fhir:coding/fhir:code", namespaces=namespaces), "value"): attr(
                    ident.find("fhir:value", namespaces=namespaces), "value"
                )
                for ident in root.findall("fhir:identifier", namespaces=namespaces)
            }

            return Result(
                file=path,
                root_label=root.tag,
                id=find_attr(root, "fhir:id", namespaces=namespaces),
                url=find_attr(root, "fhir:url", namespaces=namespaces),
                unique_ids=unique_ids | identifiers,
                description=find_attr(root, "fhir:description", namespaces=namespaces),
                publisher=find_attr(root, "fhir:publisher", namespaces=namespaces),
                status=find_attr(root, "fhir:status", namespaces=namespaces),
            )

    except Exception as exc:
        logger.error(f"Error parsing {path}: {exc}")
        return None

# ---------- Helpers ------

def get_unique_id_colname(unique_id_type: str) -> str:
    if not unique_id_type:
        return "Unique ID: (none)"
    return "Unique ID: " + unique_id_type

# ---------- CLI ----------

@click.command()
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        path_type=Path,
    ),
    required=True,
)
@click.option(
    "--output",
    "-o",
    type=click.File("w", encoding="utf-8"),
    default="-",
)
@click.option(
    '--id-type',
    'id_types',
    multiple=True,
    help='Only include identifiers of the given type. May be specified multiple times.'
)
@click.option(
    '--format', '-f',
    'output_format',
    type=click.Choice(['csv', 'markdown']),
    default='csv',
)
def generate_index(paths: tuple[Path, ...], id_types, output, output_format) -> None:
    """
    Generate an index of all the identifiers from one or more HL7 UTG directories.
    The primary HL7 UTG repository is at https://github.com/HL7/UTG

    PATHS may be files or directories. Directories are searched recursively.
    """
    results = []
    for dirpath in paths:
        for filepath in dirpath.rglob("*.xml", case_sensitive=False):
            result = index_file(filepath)
            if result is not None:
                results.append(result)

    unique_id_types = sorted(
        {key for r in results for key in r.unique_ids}
    )

    if id_types:
        unique_id_types = [t for t in unique_id_types if t in id_types]

    # Write output as a CSV file.
    field_names = ["source", "url", "status"]

    # Track which unique ID types we're producing.
    unique_id_types = set()

    # Prepare rows
    rows = []
    for result in sorted(results, key=lambda r: r.id):
        row = {
            "source": f"{result.id} ({result.publisher})",
            "url": result.url,
            # "description": result.description_field,
            "status": result.status,
        }
        for t in result.unique_ids:
            value = result.unique_ids.get(t, "")
            row[get_unique_id_colname(t)] = value
            if value:
                unique_id_types.add(t)

        # We're not interested unless there's at least one ID type.
        if unique_id_types:
            rows.append(row)

    # FILTERING
    # First, let's filter to id_types if we have any.
    filtered_rows = []
    non_empty_filtered_id_types = set()
    if id_types:
        for row in rows:
            for id_type in id_types:
                flag_select_row = False
                if get_unique_id_colname(id_type) in row and row[get_unique_id_colname(id_type)]:
                    flag_select_row = True
                    non_empty_filtered_id_types.add(id_type)

                if flag_select_row:
                    filtered_rows.append(row)
    else:
        filtered_rows = rows

    # Markdown requires every row to have every column, so we need to fit in the uniqueIds we're missing.
    # But this is also an opportunity to remove any ID types that would be completely empty in the new table
    # (i.e. that have values in rows but not in filtered_rows).
    empty_filtered_id_types = set(unique_id_types) - non_empty_filtered_id_types
    for row in rows:
        for t in unique_id_types:
            if get_unique_id_colname(t) not in row:
                row[get_unique_id_colname(t)] = ""
        for t in empty_filtered_id_types:
            del row[get_unique_id_colname(t)]

    # Add the final filtered ID types to the field names.
    for t in sorted(non_empty_filtered_id_types):
        field_names.append(get_unique_id_colname(t))

    # Filtering done!
    logging.debug(f"Rows filtered via {id_types} to {non_empty_filtered_id_types}: {json.dumps(rows, indent=2)}")

    # Write out output.
    if output_format == 'csv':
        writer = csv.DictWriter(output, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(filtered_rows)
    elif output_format == 'markdown':
        output.write(markdown_table(filtered_rows)
                        .set_params(row_sep='markdown', quote=False)
                        .get_markdown())
    else:
        raise ValueError(f"Unknown output format: {output_format}")

if __name__ == "__main__":
    generate_index()
