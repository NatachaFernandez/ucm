# CCaSP Actor Relationship Diagram

```mermaid
flowchart TD

CCASP["Care Coordination and Support Personnel (CCaSP)"]

CCASP --> Roles["Normalized Actor Roles"]

Roles --> CareCoordinator["Care Coordinator"]
Roles --> CareNavigator["Care Navigator"]
Roles --> CaseManager["Case Manager"]
Roles --> PatientNavigator["Patient Navigator"]
Roles --> CHW["Community Health Worker"]
Roles --> SocialCareCoordinator["Social Care Coordinator"]
Roles --> CaseWorker["Case Worker"]
Roles --> ResourceNavigator["Community Resource Navigator / RNAV"]
Roles --> OutreachWorker["Community Outreach Worker"]
Roles --> ReferralCoordinator["Referral Coordinator"]
Roles --> ResourceSpecialist["Resource Specialist"]
Roles --> PeerSupport["Peer Support Specialist"]

CCASP --> Characteristics["Shared Characteristics"]

Characteristics --> HumanActor["Human Actor"]
Characteristics --> CarePlanParticipation["Care Plan Participation"]
Characteristics --> ReferralParticipation["Referral Participation"]
Characteristics --> ContinuityFocus["Continuity Focus"]
Characteristics --> PersonCentered["Person-Centered Orientation"]

CCASP --> Capabilities["Shared Capabilities"]

Capabilities --> Coordinate
Capabilities --> Navigate
Capabilities --> Assess
Capabilities --> Refer
Capabilities --> Monitor
Capabilities --> Document
Capabilities --> FollowUp["Follow Up"]
Capabilities --> Advocate
Capabilities --> ReduceBarriers["Reduce Barriers"]

CCASP --> WorksWith["Works With"]

WorksWith --> CarePlan["Care Plan"]
WorksWith --> Referral["Referral"]
WorksWith --> Assessment["Assessment"]
WorksWith --> SupportiveServices["Supportive Services"]
WorksWith --> CareTeam["Care Team"]
```

## Interpretation

Care Coordination and Support Personnel (CCaSP) is the canonical actor category.

Specific workforce titles are normalized as actor roles under CCaSP. These roles share common characteristics, perform shared capabilities, and work with artifacts such as care plans, referrals, assessments, supportive services, and care teams.

This diagram separates:

* Actor category — CCaSP
* Actor roles — specific workforce titles
* Shared characteristics — what these roles have in common
* Shared capabilities — what these roles do
* Artifacts / work objects — what these roles interact with
