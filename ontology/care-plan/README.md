# RFCC Care Plan Ontology

Version: v0.1 (Draft)

## Purpose

The RFCC Care Plan Ontology defines the conceptual model for representing shared care planning across healthcare, behavioral health, social care, community services, and related support environments.

This ontology establishes a common structure for describing care plans as shared, longitudinal, person-centered artifacts used to coordinate goals, services, actions, and outcomes across participants and organizations.

The ontology is intended to support UCM, RFCC use cases, care coordination workflows, and future interoperability and terminology alignment activities.

---

## Scope

This ontology defines:

* Care plan concepts and definitions
* Care plan participants
* Shared characteristics of care plans
* Core care plan elements
* Participant interaction with care plan elements
* Terminology and interoperability bindings

This ontology does not define:

* Clinical treatment protocols
* Organizational policies
* Regulatory requirements
* Workflow execution rules
* Authorization or access control

---

## Repository Structure

```text
care-plan/
├── README.md
├── references.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── decisions.md
├── RFCC_CarePlan_Model.xlsx
├── exports/
└── diagrams/
```

---

## Workbook Structure

### 01_Definition

Canonical care plan concept and definition.

### 02_Participants

Individuals, roles, organizations, and contributors involved in care planning.

### 03_Shared_Characteristics

Common characteristics present across care plans.

Examples:

* Person-Centered
* Shared
* Longitudinal
* Dynamic
* Goal-Oriented

### 04_Elements

Core information components contained within care plans.

Examples:

* Goals
* Needs
* Problems
* Services
* Interventions
* Actions
* Referrals
* Outcomes

### 05_Participant_to_Element

Relationship model describing participant interaction with care plan elements.

### 06_Terminology_Bindings

Candidate mappings to external standards and implementation artifacts.

---

## Relationship to CCaSP

Care Coordination and Support Personnel (CCaSP) interact with care plans but are not care plans.

Relationship:

```text
CCaSP
→ contributes to
→ Care Plan

Care Plan
→ organizes
→ services, actions, goals, outcomes
```

---

## Exports

Machine-readable exports are maintained in `/exports`.

Planned exports:

* definitions.csv
* participants.csv
* characteristics.csv
* elements.csv
* participant_to_element.csv
* terminology_bindings.csv

---

## Diagrams

Conceptual diagrams are maintained in `/diagrams`.

Examples:

* participant_relationships.md
* care_plan_structure.md

These diagrams are conceptual artifacts and do not represent implementation constraints.

---

## Terminology Status

Terminology bindings are maintained as candidate mappings until reviewed and approved through governance processes.

Terminology mapping does not imply semantic equivalence or implementation readiness.

---

## Governance

Ontology changes should be documented through:

* CHANGELOG
* decisions
* terminology review
* validation activities

---

## Status

Current Status: Draft
Current Version: v0.1
