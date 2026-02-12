# IRI Stems in the HL7 Terminology Server

This table shows all the IRI stems in the [HL7 Terminology Server](https://terminology.hl7.org/), along
with the identifiers they contain. Look at the `Unique ID: iri-stem` column to see the IRI stem for each
identifier.
|                                 Source                                |                       URL                      |Status|     Unique ID: oid    |              Unique ID: uri             |    Unique ID: iri-stem    |
|-----------------------------------------------------------------------|------------------------------------------------|------|-----------------------|-----------------------------------------|---------------------------|
|                  MeSH (National Library of Medicine)                  |  http://terminology.hl7.org/NamingSystem/MeSH  |active|2.16.840.1.113883.6.177|http://terminology.hl7.org/CodeSystem/MSH|http://id.nlm.nih.gov/mesh/|
|v3-loinc (LOINC and Health Data Standards, Regenstrief Institute, Inc.)|http://terminology.hl7.org/NamingSystem/v3-loinc|active| 2.16.840.1.113883.6.1 |             http://loinc.org            |   http://loinc.org/rdf/   |
<!-- The script doesn't put a final newline on the Markdown table, so we need to leave a blank line here. -->

## How is this generated?

This table is automatically updated by the
[Regenerate IRI Stems in HL7 GitHub Action](../../.github/workflows/regenerate-hl7-terminology-iri-stem-table.yml) on
a regular schedule, using the [extract-utg-identifiers.py](../../scripts/utg/extract-utg-identifiers.py) script.
