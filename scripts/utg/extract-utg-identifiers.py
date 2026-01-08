#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["click>=8.1"]
# ///

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import click
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    def description_field(self) -> str:
        """Collapse whitespace like the Scala regex."""
        return " ".join(self.description.split())

# ---------- XML helpers ----------

def attr(elem: ET.Element | None, name: str) -> str:
    return elem.attrib.get(name, "") if elem is not None else ""


def find_attr(root: ET.Element, path: str, name: str = "value") -> str:
    return attr(root.find(path), name)


# ---------- indexing ----------

def index_file(path: Path) -> Result | None:
    try:
        with open(path, "r", encoding="utf-8") as file:
            tree = ET.parse(file)
            root = tree.getroot()

            unique_ids = {
                attr(uid.find("type"), "value"): attr(uid.find("value"), "value")
                for uid in root.findall("uniqueId")
            }

            identifiers = {
                attr(ident.find("type/coding/code"), "value"): attr(
                    ident.find("value"), "value"
                )
                for ident in root.findall("identifier")
            }

            return Result(
                file=path,
                root_label=root.tag,
                id=find_attr(root, "id"),
                url=find_attr(root, "url"),
                unique_ids=unique_ids | identifiers,
                description=find_attr(root, "description"),
                publisher=find_attr(root, "publisher"),
                status=find_attr(root, "status"),
            )

    except Exception as exc:
        logger.error(f"Error parsing {path}: {exc}")
        return None


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
def generate_index(paths: tuple[Path, ...], output) -> None:
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

    # Write output as a CSV file.
    field_names = ["file", "root_label", "id", "url", "description", "publisher", "status"]
    for t in unique_id_types:
        field_names.append(f"uniqueIdType={t}")
    writer = csv.DictWriter(output, fieldnames=field_names)
    writer.writeheader()

    # rows
    for result in sorted(results, key=lambda r: r.id):
        row = {
            "file": result.file,
            "root_label": result.root_label,
            "id": result.id,
            "url": result.url,
            "description": result.description_field,
            "publisher": result.publisher,
            "status": result.status,
        }
        for t in result.unique_ids:
            row[f"uniqueIdType={t}"] = result.unique_ids.get(t, "")
        writer.writerow(row)


if __name__ == "__main__":
    generate_index()
