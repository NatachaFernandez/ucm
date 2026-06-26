# Care Plan Components

## Purpose

This document defines the conceptual components that collectively form a Care Plan within the Unified Care Model (UCM).

A Care Plan is modeled as a living coordination construct composed of reusable components that support planning, coordination, execution, measurement, evaluation, and adaptation over time.

This document defines the major building blocks and their intended meaning independent of implementation technology.

---

# Principles

Care Plan components are:

* modular
* composable
* extensible
* interoperable
* reusable
* measurable
* person-centered
* implementation independent

Components may evolve independently while maintaining continuity of the overall Care Plan.

---

# Conceptual Structure

```text
Care Plan
├── Participant
├── Current State
├── Goal
├── Assessment
├── Need / Problem
├── Intervention
├── Activity
├── Service
├── Eligibility
├── Enrollment
├── Coordination
├── Outcome
├── Progress
├── Measurement
├── Risk
├── Evidence
├── Review
├── Decision
├── Transition
├── Version
└── Governance
```

---

# Components

## Participant

Represents individuals, organizations, teams, programs, systems, or other actors participating in planning, coordination, execution, contribution, or oversight.

Examples:

* individual
* caregiver
* provider
* care coordinator
* community organization
* payer
* digital participant

---

## Current State

Represents the present understanding of an individual’s status.

Examples:

* health state
* social conditions
* strengths
* barriers
* preferences
* environment
* readiness

Current State changes over time.

---

## Goal

Represents intended future outcomes.

Goals may be:

* preventive
* restorative
* maintenance-oriented
* recovery-oriented
* access-oriented
* wellbeing-oriented

Goals may be revised.

---

## Assessment

Represents observations, evaluations, screenings, and structured assessment outputs used to inform planning.

Examples:

* needs assessment
* structured instruments
* eligibility determination
* reassessment
* risk assessment

Assessments may trigger updates.

---

## Need / Problem

Represents conditions, gaps, barriers, opportunities, concerns, priorities, or issues requiring attention.

Examples:

* clinical needs
* social needs
* access barriers
* unmet goals

---

## Intervention

Represents actions intended to influence outcomes.

Examples:

* evidence-based interventions
* referrals
* education
* care management
* treatment
* prevention activities

Interventions may be coordinated across participants.

---

## Activity

Represents planned, ongoing, completed, or scheduled actions.

Examples:

* appointments
* outreach
* follow-up
* communication
* coordination

---

## Service

Represents organized support delivered through programs, providers, or systems.

Examples:

* healthcare service
* behavioral service
* social support
* enrollment assistance

---

## Eligibility

Represents rules, determinations, requirements, or evaluations governing access.

Examples:

* benefit eligibility
* service eligibility
* program qualification

Eligibility status may change.

---

## Enrollment

Represents activation, onboarding, or entry into a service, pathway, or program.

Examples:

* insurance enrollment
* care management enrollment
* community program enrollment

---

## Coordination

Represents collaborative activities required to align participants and actions.

Examples:

* communication
* workflow orchestration
* transitions
* interdisciplinary planning

Coordination is iterative.

---

## Outcome

Represents observed or measured effects.

Examples:

* achieved goals
* reduced barriers
* improved wellbeing
* engagement

---

## Progress

Represents change over time.

Progress may include:

* milestones
* status updates
* completion indicators
* trajectory

Progress informs adaptation.

---

## Measurement

Represents indicators used to evaluate status, outcomes, or effectiveness.

Examples:

* measures
* indicators
* benchmarks
* quality metrics

---

## Risk

Represents uncertainty, complexity, threats, or probability of undesirable outcomes.

Examples:

* clinical risk
* social risk
* enrollment risk
* transition risk

Risk may drive prioritization.

---

## Evidence

Represents supporting information used for decisions.

Examples:

* evidence-based guidance
* assessments
* observations
* evaluations
* measures

Evidence informs planning.

---

## Review

Represents reassessment and evaluation cycles.

Examples:

* periodic review
* milestone review
* triggered review

Reviews may initiate revision.

---

## Decision

Represents explicit planning decisions.

Examples:

* continue
* revise
* escalate
* transition
* complete

---

## Transition

Represents movement across states, settings, services, programs, or care episodes.

Examples:

* admission
* discharge
* referral completion
* handoff

---

## Version

Represents evolution of the Care Plan over time.

Examples:

* revision history
* snapshots
* effective periods

Care Plans are expected to evolve.

---

## Governance

Represents authority, stewardship, ownership, contribution, and policy.

Examples:

* approval
* accountability
* contribution rights
* access control

Governance may be distributed.

---

# Component Relationships

Components are expected to interact dynamically.

Examples:

```text
Assessment
→ Goal

Goal
→ Intervention

Intervention
→ Activity

Activity
→ Outcome

Outcome
→ Progress

Progress
→ Review

Review
→ Care Plan Revision
```

---

# Status

Draft — evolving.

Components are conceptual and implementation independent and may be represented differently across systems and interoperability models.
