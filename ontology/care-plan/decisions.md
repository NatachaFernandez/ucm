# Decisions

This document records governance, modeling, terminology, and structural decisions made during development of the RFCC Care Plan Ontology.

Only approved decisions should be recorded.

---

## Decision Status Values

```text
Proposed
Accepted
Superseded
Rejected
Deferred
```

---

## DEC-001 — Care Plan Modeled as Shared Artifact

Status: Accepted

Date: YYYY-MM-DD

Decision

The Care Plan shall be modeled as a shared information artifact rather than as a workflow, service, organization, or actor.

Rationale

Care plans organize goals, services, actions, responsibilities, and outcomes across participants and settings.

Implications

* Participants interact with care plans
* Care plans are distinct from workforce roles
* Care plans support longitudinal coordination

Related Artifacts

* 01_Definition
* 02_Participants
* 04_Elements

---

## DEC-002 — Person-Centered Approach

Status: Accepted

Date: YYYY-MM-DD

Decision

Care Plan definitions and structures shall prioritize individual goals, preferences, needs, and outcomes.

Rationale

Care planning exists to support coordinated and individualized care rather than organizational processes.

Implications

* Goals are participant-oriented
* Outcomes remain traceable
* Participants may contribute jointly

Related Artifacts

* 03_Shared_Characteristics
* 04_Elements

---

## DEC-003 — Participant Separation from Authorization

Status: Accepted

Date: YYYY-MM-DD

Decision

Participants in care plans shall represent contributors and consumers and shall not imply authorization, access control, or permissions.

Rationale

Participation and access governance are separate concerns.

Implications

* Participants may create, update, view, or monitor
* Authorization remains external

Related Artifacts

* 02_Participants
* 05_Participant_to_Element

---

## DEC-004 — Terminology Deferred Until Validation

Status: Accepted

Date: YYYY-MM-DD

Decision

Terminology bindings shall remain candidate mappings until ontology validation is complete.

Rationale

Conceptual stability should precede terminology alignment.

Implications

* Candidate bindings only
* No semantic equivalence assumed

Related Artifacts

* 06_Terminology_Bindings

---

## Future Decisions

Reserve this section for:

* Care plan ownership
* Goal governance
* Care team relationships
* Service representation
* FHIR alignment
* SNOMED CT evaluation
* LOINC evaluation
