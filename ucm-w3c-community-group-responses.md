# **W3C Community Group Responses**

## **What problem(s) do you want to solve?**
[italics represent open questions/tasks]
Organizations across healthcare, behavioral health, social care, housing, justice, education, and related human-service domains increasingly need to coordiante around the same individuals, households, and care goals.  Although these domains often serve the same people, they have evolved independently and use different standards, information models, terminologies, workflows, and ontologies that often reflect different perspectives, assumptions, and semantic structures. 

This need is increasingly operationally and clinically necessary rather than optional, as outcomes often depend on coordinated actions across multiple disciplines and service ecosystems.

Existing domain standards and data models (including USCDI and future versions where applicable) provide important foundations; however; relationships between these artifacts and longitudinal care planning concepts are not consistently represented or computable across domains. 

Although information can often be exchanged between systems, shared meaning, intent, context, and relationships between care activities are frequently not preserved consistently across domains. As a result, organizations face significant challenges in achieving semantic interoperability, interdisciplinary coordination, integrated analytics, AI-enabled reasoning, and the development of applications that require semantically consistent information across domains.  These challenges create barriers to interdisciplinary collaboration and limit the ability of organizations to coordinate services while allowing domains to preserve their distinct responsibilities, expertise, and workflows.

The group seeks to address the lack of a shared semantic framework that can bridge these heterogeneous domain models while preserving their meaning. The goal is to enable semantic alignment, integration, reasoning, and reuse across care domains in support of coordinated, person-centered service delivery and longitudinal care planning.

Addressing this problem enables whole-person and person-centered approaches to care by creating the semantic foundation needed for interdisciplinary coordination across domains.  UCM itself is not a care model; it is the semantic framework intended to support existing and emerging models of care.

## **What is the mission of this Group?**

The mission of the group is to develop an open, computable semantic framework that enables semantic interoperability across care domains including healthcare, behavioral health, social care, housing, justice, education, and related human-service ecosystems.

The group will develop the Unified Care Model (UCM), a high-level ontology and semantic reference model that can be used to align and bridge domain-specific information models, ontologies, and standards. UCM is intended to provide a shared semantic foundation that supports coordinated, interdisciplianry, and person-centered service delivery while preservig domain-specific meaning and autonomy.

It is not a goal to replace existing standards, information models, or domain artifacts, but rather to enable interoperability and semantic consistency accross them.

## **Design Principles**

The current version of the project Design Principles document can be found at: https://github.com/hserv/ucm/blob/main/ucm-design-principles.md

Key design principles include *such as*:

• **Care Plan as the coordination construct** | UCM treats the Care Plan as the central cross-domain structure for alignig goals, coordinating actions, assigning responsibilities, and executing interventions across participating disciplins.  Care Plans evelve over time as outcomes and needs change.
• **Computable semantics** | UCM developed as an OWL ontology supporting Description Logic reasoning.  
• **Ontology grounding** | Uses BFO as the ontological foundation.  
• **Semantic classification and abstraction** | Leverages SULO as a semantic classification framework.  
• Alignment without replacement | Goal is to align model with HL7, HUD, NIEM and other domain artifacts.  
• **Layered semantic seperation** | Layered architecture of Core Concepts, Participation Concepts, and Domain Concepts.  
• **Independent domain evolution** | Enable independent extension by different subject matter experts while maintaining semantic consistency through a shared core.  
• **Participation over identity classification** | Emphasizes reuse, extensibility, semantic clarity, and cross-domain interoperability.

## **Will the Group Publish Specifications?**

Yes. The long-term goal of the group is to publish one or more open specifications describing the Unified Care Model and its associated semantic framework.

The group anticipates producing a W3C Community Group Report.

*Spec as a starting point?*

*FHIR semantic gaps*

*Care plan is the most critical component.*
