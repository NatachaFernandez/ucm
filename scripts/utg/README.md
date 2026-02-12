# Scripts for working with the HL7 Unified Terminology Governance (UTG) repository

The scripts in this folder are intended to be used with the [HL7 Unified Terminology Governance (UTG) repository].

## Generate HL7 Terminology IRI Stem Table

[generate-hl7-terminology-iri-stem-table.py](./generate-hl7-terminology-iri-stem-table.py) generates
a table of all the IRI stems present in a given version of the HL7 UTG, which needs to be downloaded
or cloned from the [HL7 Unified Terminology Governance (UTG) repository].

### Usage

To generate the IRI stem table, install [uv](https://docs.astral.sh/uv/) and run the following command:

```bash
uv run generate-hl7-terminology-iri-stem-table.py /path/to/UTG
```

This will write out a CSV table of IRI stems to standard output.

This script uses the `/// script` header so that [`uv` will automatically install dependencies](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies)
before running this script.

### Purpose

This script was specifically written to be used in a [GitHub Action workflow](../../.github/workflows/regenerate-hl7-terminology-iri-stem-table.yml)
that runs on a schedule and triggers a PR to update the [HL7 IRI stem table](../../data/utg/iri-stems-in-hl7.md)
when the IRI stems in the UTG repository changes. Several features have been implemented to provide
this functionality:

* `--id-type iri-stem` to only write out IRI stems that have a uniqueId of type `iri-stem`.
* `-f [csv|markdown]` to choose the output format

### Workflow

The [GitHub Action workflow](../../.github/workflows/regenerate-hl7-terminology-iri-stem-table.yml) works as follows:
1. Download the UTG GitHub repo -- ideally we'd use the GitLab original instead of the GitHub mirror, but this doesn't seem to be accessible from the GitHub Action.
2. Use a Python script (replacing the older Scala script) to extract the IRI Stems from UTG GitHub repo.
    * This script can be run with `uv run` -- it includes a `/// script` header that specified dependencies and minimum Python version.
    * The Scala script is deleted in this PR.
    * The script uses command-line arguments to specify that only CodeSystems/NamingSystems containing IRI Stems should be written out, but that can be taken out if you want all the unique IDs.
    * The script produces a Markdown table.
3. The Markdown table produced by the Python script is then combined with a header and footer table to produce the final Markdown file.
4. If the Markdown file differs from the previous file (as judged with a `git commit`), then the `auto/update-iri-stems-in-hl7` branch will be updated with this change, and a PR will be generated with this change.
    * An example PR is available at https://github.com/gaurav/hcls-fhir-rdf/pull/3
    * Reusing the same branch name means that if the script runs again before the PR is merged, it will be updated rather than a new PR created.
5. It will then be up to a human to review the change and merge it if it makes sense.

[HL7 Unified Terminology Governance (UTG) repository]: https://github.com/HL7/UTG
