# Scripts for working with the HL7 Unified Terminology Governance (UTG) repository

The scripts in this folder are intended to be used with the [HL7 Unified Terminology Governance (UTG) repository].

* GenerateIndex.scala: A [Scala CLI] script for generating an index for the UTG repository.

## GenerateIndex.scala

This [Scala CLI] script generates an index for the UTG repository. It was intended to
help with [finding IRI stems] that needed to be added to the UTG repository.

An example of the generated index is [available in this repository](./examples/index-as-of-2025jan23.tsv).

Instructions:
1. [Install Scala CLI] (if you have macOS and Homebrew, you can run `brew install scala-cli`).
2. Download or clone the [HL7 Unified Terminology Governance (UTG) repository].
3. Run `scala-cli GenerateIndex.scala -- [path to the root of the UTG]`. The script writes out the index to
   STDOUT, so you will need to redirect that to a TSV file.
  * For example, you might run `scala-cli GenerateIndex.scala -- /Users/username/github/UTG > index.tsv`

[HL7 Unified Terminology Governance (UTG) repository]: https://github.com/HL7/UTG
[Scala CLI]: https://scala-cli.virtuslab.org/
[finding IRI stems]: https://github.com/w3c/hcls-fhir-rdf/issues/123
[Install Scala CLI]: https://scala-cli.virtuslab.org/install
