# Workforce, Credentialing, and Claims Semantics in CCASP

## Purpose

This document defines initial semantics for workforce participation, credentialing, licensing, scope of practice, billing eligibility, and claims processability within the Care Coordination and Support Personnel (CCASP) ontology.

The purpose is to separate personnel role semantics from operational billing, licensing, certification, and payer-specific requirements while allowing these concepts to be referenced by CCASP profiles, characteristics, and catalogs.

## Scope

This document applies to personnel and roles involved in care coordination and support services.

It may be used to support questions such as:

* Is this role billable?
* What license, certification, or credential is required?
* Who is the certifying or licensing authority?
* What activities are allowed under the role's scope of practice?
* What CPT, claims, or service-code attributes may be associated with the role?
* What payer types may process claims for this role or service?
* Under what conditions are claims processable?

## Relationship to the CCASP Profile Workbook

The CCASP profile workbook may contain characteristics and catalogs that reference this document.

Examples of workbook characteristics may include:

* billableRole
* requiresLicense
* licenseType
* requiresCertification
* certificationType
* certifyingAuthority
* scopeOfPractice
* supervisionRequired
* canSubmitClaims
* claimSubmissionAuthority
* payerEligibility
* reimbursementEligibility
* allowableProcedureCodes
* allowableClaimTypes
* claimsProcessable

Examples of workbook catalogs may include:

* License Type Catalog
* Certification Type Catalog
* Certifying Authority Catalog
* Payer Type Catalog
* Procedure Code Catalog
* Claim Type Catalog
* Billing Method Catalog
* Scope of Practice Catalog
* Supervision Requirement Catalog

The workbook should capture structured values. This document provides the semantic meaning and modeling guidance behind those values.

## Core Concepts

### Workforce Role

A workforce role represents a care coordination or support personnel function performed by a person or organization.

Examples:

* Care coordinator
* Community health worker
* Peer support specialist
* Housing navigator
* Case manager
* Social worker
* Patient navigator

### Scope of Practice

Scope of practice describes the activities, services, interventions, or responsibilities that a workforce role is permitted or expected to perform.

Scope of practice may be constrained by:

* license
* certification
* jurisdiction
* employer policy
* payer rules
* supervision requirements
* program requirements

### Credential

A credential represents evidence that a person or organization has met defined requirements.

Credential types may include:

* license
* certification
* registration
* accreditation
* training completion
* authorization

Credential attributes may include:

* credential type
* issuing authority
* jurisdiction
* effective date
* expiration date
* status
* renewal requirements

### Certifying or Licensing Authority

A certifying or licensing authority is the organization or body that grants, recognizes, or maintains a credential.

Examples may include:

* state licensing boards
* certification bodies
* professional associations
* government agencies
* accredited training organizations

### Billing Eligibility

Billing eligibility describes whether a role, credential, service, or participant can be associated with reimbursable services or claim submission.

Billing eligibility may depend on:

* workforce role
* credential status
* service type
* payer type
* jurisdiction
* supervision arrangement
* place of service
* program rules
* documentation requirements

### Claim Capability

Claim capability describes the ability to represent a service, intervention, or activity for reimbursement or claims processing.

Claim capability may include:

* allowable procedure codes
* allowable service codes
* claim type
* billing method
* required modifiers
* documentation requirements
* prior authorization requirements
* payer-specific constraints

### Payer Eligibility

Payer eligibility describes which payer or funding ecosystems may process or reimburse claims for a role, service, or intervention.

Examples:

* Medicaid
* Medicare
* commercial insurance
* managed care organization
* grant-funded program
* self-pay
* state or local program
* social-service funding source

## Conceptual Relationships

A workforce role may require a credential.

A credential may be issued by a certifying or licensing authority.

A workforce role may have a scope of practice.

A scope of practice may constrain allowable services, interventions, or responsibilities.

A workforce role may be billable only under specific conditions.

Billing eligibility may depend on payer type, credential status, supervision, jurisdiction, service type, and documentation.

Claim capability may define which procedure codes, claim types, service codes, or billing methods are available.

Payer eligibility may constrain whether a claim is processable.

## Modeling Considerations

CCASP should distinguish between:

* a role being clinically or operationally useful
* a role being authorized to perform a service
* a role being credentialed or licensed
* a role being billable
* a service being reimbursable
* a claim being processable by a payer

These are related but not equivalent.

For example, a role may participate in care coordination but not be independently billable. Another role may perform a service only under supervision. A service may be allowed under a scope of practice but not reimbursable by a specific payer.

## Open Questions

* Should billability attach to the workforce role, the service, the credential, or the participation context?
* How should supervision and delegated billing be represented?
* How should jurisdiction-specific licensure rules be modeled?
* Should payer-specific rules be modeled directly or referenced as external policy artifacts?
* How should CPT, HCPCS, revenue codes, and non-clinical service codes be represented?
* How should CCASP distinguish between service eligibility, claim eligibility, and claim processability?
* Which characteristics should live in the profile workbook, and which should become ontology concepts?
