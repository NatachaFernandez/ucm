# CONTRIBUTING

## Purpose

This document defines how changes to the RFCC Care Plan Ontology are proposed, reviewed, approved, and maintained.

The Care Plan Ontology is intended to provide a stable conceptual model for shared care planning across healthcare, behavioral health, social care, community services, and related support environments.

---

## Contribution Principles

### Person-Centered

Definitions and structures should prioritize individual goals, preferences, needs, and outcomes.

### Shared Participation

Care plans should support contribution and use across participants, organizations, and care settings.

### Longitudinal Coordination

Changes should support continuity over time rather than isolated encounters.

### Implementation Neutral

Definitions should remain independent of specific products, workflows, vendors, or jurisdictions.

### Artifact-Oriented Modeling

Care plan concepts describe information structures and relationships rather than workforce roles.

---

## Modeling Rules

### Definitions

* Definitions should describe concepts rather than implementation.
* Avoid workflow-specific language unless universally applicable.
* Prefer reusable and jurisdiction-neutral terminology.

### Participants

* Participants describe contributors or consumers of care plans.
* Participants may include people, roles, organizations, and services.
* Participants should not define permissions or authorization.

### Characteristics

* Characteristics describe what care plans are.
* Characteristics should remain stable across implementations.

### Elements

* Elements describe components contained within care plans.
* Elements should represent information artifacts rather than activities.

### Terminology Bindings

* Candidate mappings must not be treated as approved.
* External terminology should not replace RFCC definitions.
* Local concepts should only be created when external concepts are insufficient.

---

## Change Process

```text
Draft
→ Review
→ Validation
→ Approval
→ Publication
```

Changes should be documented in:

* CHANGELOG
* decisions
* validation artifacts
* terminology review

---

## Naming Conventions

Participant IDs:

```text
PART-###
```

Characteristic IDs:

```text
CHAR-###
```

Element IDs:

```text
ELM-###
```

Terminology IDs:

```text
RFCC-###
```

---

## Validation Expectations

Before approval:

* Concept definition reviewed
* Participant relationships reviewed
* Element relationships reviewed
* Terminology evaluated
* Documentation updated

---

## Versioning

Version updates should be recorded in:

* CHANGELOG
* README

Version numbers should not be embedded in filenames.

---

## Status

Current Status: Draft
