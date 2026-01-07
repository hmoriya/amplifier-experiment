# TOGAF® Series Guide: Value Streams

**Prepared by The Open Group Architecture Forum Business Architecture Work Stream**

---

**Document Information**
- ISBN: 1-947754-02-7
- Document Number: G178
- Published by The Open Group, October 2017
- Updated in June 2018 to reference the TOGAF® Standard, Version 9.2 and the TOGAF® Series Guide: Business Capabilities (G189)

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 What is "Value"?
   - 1.2 Approaches to Value Analysis
   - 1.3 Value Streams in Business Architecture
   - 1.4 Relationship of Value Streams to Other Business Architecture Concepts
   - 1.5 Benefits of Value Streams and Value Stream Mapping
2. [Value Stream Description, Decomposition, and Mapping](#2-value-stream-description-decomposition-and-mapping)
   - 2.1 Describing a Value Stream
   - 2.2 Decomposing a Value Stream
   - 2.3 Mapping Capabilities to Value Stream Stages
3. [Approach to Creating Value Streams](#3-approach-to-creating-value-streams)
   - 3.1 Guiding Principles
4. [Value Stream Mapping Scenarios](#4-value-stream-mapping-scenarios)
   - 4.1 Baseline Example
   - 4.2 Mapping Value Streams to Business Capabilities
   - 4.3 Heat Mapping Scenario
5. [Conclusion](#5-conclusion)
- [Appendix A: Comparison of Alternative Value Analysis Techniques](#appendix-a-comparison-of-alternative-value-analysis-techniques)

---

## Preface

### The Open Group

The Open Group is a global consortium that enables the achievement of business objectives through technology standards. Our diverse membership of more than 600 organizations includes customers, systems and solutions suppliers, tools vendors, integrators, academics, and consultants across multiple industries.

The Open Group aims to:
- Capture, understand, and address current and emerging requirements, establish policies, and share best practices
- Facilitate interoperability, develop consensus, and evolve and integrate specifications and open source technologies
- Operate the industry's premier certification service

Further information on The Open Group is available at [www.opengroup.org](http://www.opengroup.org).

### The TOGAF® Standard

The TOGAF standard is a proven enterprise methodology and framework used by the world's leading organizations to improve business efficiency.

### This Document

This document is a TOGAF® Series Guide to Value Streams, addressing how to identify, define, model, and map a value stream to other key components of an enterprise's Business Architecture.

**Guide Structure:**
- **Chapter 1 (Introduction)** - Introduces the concept of value, how it relates to business in general, and how it can be used and applied within Business and Enterprise Architecture
- **Chapter 2 (Value Stream Description, Decomposition, and Mapping)** - Describes the structure and mechanics of the value stream, including its decomposition into value stream stages
- **Chapter 3 (Approach to Creating Value Streams)** - Sets out guiding principles for constructing a value stream map
- **Chapter 4 (Value Stream Mapping Scenarios)** - Describes a range of business scenarios and practical examples of value stream mapping
- **Chapter 5 (Conclusion)** - Summarizes the role and value that value streams and value stream mapping can bring to business
- **Appendix A (Comparison of Alternative Value Analysis Techniques)** - Compares and contrasts other common value analysis techniques

**Intended Audience:**
- Enterprise Architects
- Business Architects
- Process modelers
- Strategy planners

---

## 1 Introduction

### 1.1 What is "Value"?

The word "value" originates from the Old French *valoir*: 'be worth'. It is the regard that something is held to deserve; the importance, worth, or usefulness of something. Within the context of Business Architecture, it is important to think of value in the most general sense of usefulness, advantage, benefit, or desirability, rather than the relatively narrow accounting or financial perspective that defines value as being the material or monetary worth of something.

Non-monetary examples of value in the business world include such things as the successful delivery of a requested product or service, resolving a client's problem in a timely manner, or gaining access to up-to-date information in order to make better business decisions.

Value is fundamental to everything that an organization does. The primary reason that an organization exists is to provide value to one or more stakeholders. It is the foundation of a firm's business model, which describes the rationale for how a business creates, delivers, and captures value.

The Business or Enterprise Architect should be able to model, measure, and analyze the various ways that the enterprise achieves value for a given stakeholder. This includes the ability to decompose the creation, capture, and delivery of value into discrete stages of value-producing activities, each of which is enabled by the effective application of business capabilities (see the TOGAF® Series Guide to Business Capabilities).

### 1.2 Approaches to Value Analysis

Several approaches have been used in the past to model, measure, and analyze business value. Three well-known (but often misunderstood) techniques include value chains, value networks, and lean value streams. Each approach has a distinct purpose and area of focus:

| Technique | Primary Focus |
|-----------|---------------|
| Value Chain | Economic value perspective |
| Value Network | Identifying participants involved in creating and delivering value |
| Lean Value Stream | Optimizing business processes (primarily manufacturing context) |
| Business Architecture Value Stream | End-to-end perspective of value from the customer's/stakeholder's perspective |

Only the Business Architecture value stream is designed to create an end-to-end perspective of value from the customer's (or stakeholder's) perspective, and is more closely aligned to realizing an organization's business model rather than the financial, organizational, or operational models.

### 1.3 Value Streams in Business Architecture

The approach to value analysis used in Business Architecture is derived from James Martin's *The Great Transition*. The value stream is depicted as an end-to-end collection of value-adding activities that create an overall result for a customer, stakeholder, or end-user. In modeling terms, those value-adding activities are represented by value stream stages, each of which creates and adds incremental stakeholder value from one stage to the next.

**Example Value Stream: Acquire Retail Product**

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│  Advertise  │   Display   │   Enable    │   Process   │   Deliver   │
│  Channels   │ Merchandise │  Selection  │   Payment   │ Merchandise │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

**Key Characteristics:**
- Value streams may be **externally triggered** (e.g., retail customer acquiring merchandise)
- Value streams may be **internally triggered** (e.g., manager obtaining a new hire)
- Value streams may be defined at an **enterprise level** or at a **business unit level**

A key principle of value streams is that **value is always defined from the perspective of the stakeholder** – the customer, end-user, or recipient of the product, service, or deliverable produced by the work.

### 1.4 Relationship of Value Streams to Other Business Architecture Concepts

As part of the practice of Business Architecture, we separate concerns:

| Concern | Element |
|---------|---------|
| What we do | Business Capability |
| Who does it | Organization |
| How value is achieved | Value Stream |
| How it is implemented/performed | Process |
| What information is needed | Information |
| What systems are used | Systems |

**Value Stream Modeling Relationships:**

```
                    ┌───────────────┐
                    │  Stakeholder  │
                    └───────┬───────┘
                            │ triggers / receives
                            ▼
┌─────────┐  creates  ┌─────────────┐  consists of  ┌─────────────┐
│  Value  │◄──────────│Value Stream │───────────────►│ Value Stage │
└─────────┘           └─────────────┘               └──────┬──────┘
                                                          │ enables
                                                          ▼
                      ┌─────────────┐               ┌────────────┐
                      │   Process   │◄──────────────│ Capability │
                      └─────────────┘ operationalizes└────────────┘
```

The complete set of value streams depicts the various ways in which an organization orchestrates its capabilities to create stakeholder value. The value stream has a direct linkage to an organization's business model (specifically to the value proposition).

**Key Distinction:**
- **Value streams** take an outside-in perspective and show how value gets created and moved in relation to the stakeholder
- **Business processes** have an inward-looking, operational-level focus concerned with how work gets done

### 1.5 Benefits of Value Streams and Value Stream Mapping

Mapping value streams is a quick and easy way to obtain a snapshot of the entire business, since those value streams represent all the work that the business needs to perform from a value-delivery perspective.

**Benefits include:**
- Help business leaders envision and prioritize the impact of strategic plans, manage stakeholder engagement, and deploy new business solutions
- Provide a value-based, customer-centric context for business analysis and planning
- Provide a framework for more effective business requirements analysis, case management, and solution design
- Lead to more effective business and operating models through outside-in design approach

---

## 2 Value Stream Description, Decomposition, and Mapping

### 2.1 Describing a Value Stream

Value streams are defined using four standard elements:

| Element | Description |
|---------|-------------|
| **Name** | Must be clearly understandable from the stakeholder's perspective. Uses active tense (verb-noun construct). Example: "Acquire Retail Product", "Recruit Employee" |
| **Description** | Short, precise description providing clarity on scope of activities |
| **Stakeholder** | The person or role that initiates or triggers the value stream |
| **Value** | The value (in stakeholder terms) expected upon successful completion |

**Example:**

| Element | Content |
|---------|---------|
| Name | Acquire Retail Product |
| Description | The activities involved in looking for, selecting, and obtaining a desired retail product |
| Stakeholder | A retail shopper wishing to purchase a product |
| Value | Customers are able to locate desired products and obtain them in a timely manner |

### 2.2 Decomposing a Value Stream

Stakeholder value is rarely produced as the result of a single step. Value is achieved through a series of sequential and/or parallel actions, or **value stream stages**, that incrementally create and add stakeholder value from one stage to the next.

**Each value stream stage comprises:**

| Element | Description |
|---------|-------------|
| **Name** | Two to three words identifying what is achieved by this stage |
| **Description** | Few sentences explaining the purpose and activities performed |
| **Stakeholders** | Actors who receive measurable value or contribute to creating/delivering value |
| **Entrance Criteria** | Starting condition or state change that triggers the stage |
| **Exit Criteria** | End state condition denoting completion (becomes entry criteria for next stage) |
| **Value Item** | Incremental value created or delivered by the stage |

**Important:** A value stream does not necessarily flow continuously. Following each stage, there is an opportunity to stop if desired value has not been created or delivered.

### 2.3 Mapping Capabilities to Value Stream Stages

After defining the end-to-end value stream, identify which business capabilities are required to enable each value stream stage by:
1. Reviewing the business capability map
2. Linking (cross-mapping) relevant business capabilities to each value stream stage

**Purpose:**
- Identify which capabilities are critical to delivering stakeholder value
- Identify capabilities needing sufficient quality standards
- Identify capabilities that don't contribute to core value streams (potential elimination candidates)

---

## 3 Approach to Creating Value Streams

A common question: **Which should come first - the value stream map or the business capability model?**

**Answer:** It does not matter, because one should not exist without the other for very long. Value streams provide stakeholder context into *why* we need business capabilities, while capabilities demonstrate *what* we need for a value stream to be successful.

In practice, it is often faster and easier to draft value streams first, as you can demonstrate results sooner and inform the development of the business capability model.

### 3.1 Guiding Principles

1. **There must be a clearly defined triggering stakeholder** – For example, a customer initiating a discussion with a customer services agent

2. **Start with external (usually customer-based) value streams** – These help frame the range of possible internally focused value streams

3. **Value streams are not capabilities, nor components of capabilities** – They describe the sequence of activities to produce/realize value. Whether the business can perform those activities is a function of its business capabilities

4. **Keep it concise** – Creating value streams should not require going down to operational levels of detail. That is the domain of business process design

---

## 4 Value Stream Mapping Scenarios

### 4.1 Baseline Example

**Value Stream Definition:**

| Element | Content |
|---------|---------|
| Name | Acquire Retail Product |
| Description | The activities involved in looking for, selecting, and obtaining a desired retail product |
| Stakeholder | A retail shopper wishing to purchase a product |
| Value | Customers are able to locate desired products and obtain them in a timely manner |

**Value Stream Stages:**

| Stage | Description | Participating Stakeholders | Entrance Criteria | Exit Criteria | Value Items |
|-------|-------------|---------------------------|-------------------|---------------|-------------|
| Advertise Channels | Making customers aware of the company's products | Store/Website Owner, Marketing | Customer searches for product | Customer selects channel | Retail channel available to customer |
| Display Merchandise | Presenting products in physical or searchable digital form | Store Employees, Inventory Manager, Web Designer | Customer selects channel | Customer views products | Product options provided to customer |
| Enable Selection | Enabling filtering and assessments of best product(s) matched to customer's needs | Store Employees, Web Designer, Retail Shopper | Customer views products | Customer selects product | Desired product located |
| Process Payment | Taking and processing payment from the customer | Cashier, Financial Entities, Retail Shopper | Customer selects product | Charges paid | Delivery commitment |
| Deliver Merchandise | Getting the product into the customer's hands | Warehousing, Transportation, Retail Shopper | Charges paid | Product delivered | Product in user's possession |

### 4.2 Mapping Value Streams to Business Capabilities

**Example: Recruit Employee Value Stream**

| Element | Content |
|---------|---------|
| Name | Recruit Employee |
| Description | The activities involved in identifying and hiring suitably qualified employees |
| Stakeholder | A Hiring Manager looking to fill a specific position |
| Value | A new employee with good fit for the job, hired rapidly, and working productively |

**Value Stream Stages:**

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Define    │ Communicate │   Assess    │  Interview  │   Onboard   │
│  Position   │  Position   │  Responses  │ Candidates  │  Employee   │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

| Stage | Description | Participating Stakeholders | Entrance Criteria | Exit Criteria | Value Items |
|-------|-------------|---------------------------|-------------------|---------------|-------------|
| Define Position | Determining staffing need, identifying skills/qualifications, documenting | Hiring Manager, HR Recruitment Lead | Staffing changes identified | Recruitment needs identified | Time and expense saved on search |
| Communicate Position | Advertising, posting requisition to portals and recruitment events | Recruiter | Recruitment needs identified | Positions communicated | High likelihood of finding qualified candidates |
| Assess Responses | Receiving, logging, distributing, scoring candidate responses | Hiring Manager, Recruiter | Positions communicated | Qualified responses selected | Efficient use of interview time and costs |
| Interview Candidates | Communicating with candidates, scheduling and conducting interviews | Hiring Manager, Candidate Employee | Qualified responses selected | Hiring decision | Selection of the best employee |
| Onboard Employee | Making offer, integrating employee into work environment | Employee, HR, Security, Facilities, Finance, IT | Hiring decision | Employee onboarded | Productive workforce meeting commitments |

**Cross-Mapping to Business Capabilities:**

| Define Position | Communicate Position | Assess Responses | Interview Candidates | Onboard Employee |
|----------------|---------------------|------------------|---------------------|------------------|
| Finance Mgmt. | Asset Mgmt. | Agreement Mgmt. | HR Mgmt. | HR Mgmt. |
| HR Mgmt. | Asset Allocation | Security Mgmt. | Agreement Structuring | Benefits Management |
| Program Mgmt. | Position Advertising | HR Mgmt. | HR Mgmt. | Employee Background and ID |
| Employee Supply and Demand Mgmt. | | Competency Mgmt. | Employee Supply and Demand Mgmt. | Onboard Tracking |
| Program/Human Resource Matching | | Skills Assessment | | Facilities Mgmt. |
| | | | | Space Allocation |
| | | | | Information Mgmt. |
| | | | | Employee Information Mgmt. |
| | | | | Terms Management |
| | | | | Labor Funding |
| | | | | Compensation Mgmt. |

### 4.3 Heat Mapping Scenario

**Scenario:** A fictional company has been hiring in response to growing market demand. The acceptance rate has been trending down, and social media suggests poor treatment of new employees.

**Process:**
1. Recruitment Director assembles cross-functional team (Program Management, Finance, Asset Management, Business Architect)
2. Team refines the Recruit Employee value stream for their company
3. Map business capabilities to value stream stages
4. Create initial heat map showing gaps (reds = significant gaps, yellows = some shifts needed)
5. Gather more detailed information about gap areas
6. Reconvene and identify root causes

**Key Finding:** An IT employee who retired had been manually tracking the onboarding sequence. Since no one took over the role, new employees experienced longer delays to full productivity.

**Heat Map Legend:**
- Red: Significant gaps between needed and current state
- Yellow: Some shifts needed
- Green: Adequate performance

**Resolution:**
1. Added Policy Dissemination as key capability to first value stream stage
2. Recognized need for subordinate value stream covering employee onboarding
3. Identified need for value stream owner to improve company recruitment

---

## 5 Conclusion

The use of value streams is an important Business Architecture technique designed to understand what value needs to be created and delivered to each group of key stakeholders.

**Key Points:**
- Decomposing value streams into stages provides clearer understanding of how value is created/delivered
- Identifies what business capabilities are necessary to support critical value-adding activities
- Value streams are the counterpoint to business capabilities
- **Capabilities** deal with *what* a business does
- **Value streams** focus on *how* a business delivers value to stakeholders

Together, value streams and business capabilities form a powerful analytical device to:
- Unpick constituent parts of a business
- Understand inner workings
- Assess alignment between mission and activities
- Identify improvement opportunities

Value stream mapping provides a powerful way to obtain a snapshot of the entire business, helping business leaders assess organizational effectiveness at creating, capturing, and delivering value for stakeholders.

---

## Appendix A: Comparison of Alternative Value Analysis Techniques

### A.1 Value Chain

Value chains were introduced by Michael Porter in *Competitive Advantage*:

> "The value chain disaggregates a firm into its strategically-relevant activities in order to understand the behavior of costs and the existing potential sources of (competitive) differentiation."

**Porter's Value Chain Structure:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SUPPORT ACTIVITIES                               │
├─────────────────────────────────────────────────────────────────────┤
│ Firm Infrastructure                                                 │
│ Human Resource Management                                           │
│ Technology Development                                              │
│ Procurement                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                    PRIMARY ACTIVITIES                               │
├───────────┬───────────┬───────────┬───────────┬───────────┬────────┤
│ Inbound   │Operations │ Outbound  │ Marketing │  Service  │ MARGIN │
│ Logistics │           │ Logistics │ & Sales   │           │        │
└───────────┴───────────┴───────────┴───────────┴───────────┴────────┘
```

**Key Difference from Value Streams:**
- Value chains focus on activity costs and margins (economic value)
- Lack structure for modeling how business combines capabilities to produce outcomes
- Macro-level view of economic value production
- Value streams enable decomposition into sequences of core activities enabled by capabilities

### A.2 Value Network

Value networks describe social and technical resources within and between businesses.

**Characteristics:**
- Nodes represent people or roles
- Connections represent interactions/deliverables
- Deliverables may be tangible (products, cash) or intangible (knowledge)

**Primary Purpose:** Understand the complex web of relationships and value exchange areas within and between businesses.

### A.3 Lean Value Stream

Lean value streams originated from the Lean Thinking movement (Toyota's "material and information flow mapping").

**Core Premise:** Identify and eliminate waste from processes, retaining only activities that create or increase value for the end-user.

**Definition:** A diagrammatic representation of the sequence of activities required to design, produce, and deliver a good or service to a customer.

**Typical Metrics:**
- Processing Time
- Response Time
- Percent Complete & Accurate

**Key Difference from Business Architecture Value Streams:**
- Primary purpose: Document, analyze, improve flow of information/materials
- Not designed for broader architectural purposes
- Not suited for decomposing to critical value-creating stages
- Not designed for cross-mapping to enabling business capabilities

---

## Referenced Documents

**Primary References:**
- *Competitive Advantage: Creating and Sustaining Superior Performance*, Michael E. Porter, Free Press, 1985
- *The Future of Knowledge: Increasing Prosperity through Value Networks*, Verna Allee, Butterworth-Heinemann, 2003
- *The Great Transition: Using the Seven Disciplines of Enterprise Engineering to Align People, Technology, and Strategy*, James Martin, American Management Association, 1995
- *The Machine that Changed the World*, James Womack, Daniel Jones, and Daniel Roos, Free Press, 1990
- TOGAF® Series Guide: Business Capabilities (G189), June 2018, The Open Group

**Background References:**
- *A Guide to Business Architecture Body of Knowledge® (BIZBOK® Guide)*, Business Architecture Guild
- *Open Business Architecture (O-BA) – Part I* (P161), The Open Group, July 2016
- *The TOGAF® Standard, Version 9.2* (C182), The Open Group, April 2018

---

## Index

| Term | Description |
|------|-------------|
| Business activities | Work performed by the organization |
| Business capabilities | What a business does |
| Business capability map | Visual representation of all capabilities |
| Business capability model | Structured model of capabilities |
| Business model | How business creates, delivers, captures value |
| Gap analysis | Identifying differences between current and target states |
| Heat mapping | Visual technique showing performance levels |
| Lean value stream | Process optimization technique from Lean Thinking |
| Organization | Who does the work |
| Process | How work is implemented/performed |
| Stakeholder | Person/role receiving or triggering value |
| Stakeholder value | Value from stakeholder's perspective |
| Value | Usefulness, advantage, benefit, or desirability |
| Value analysis | Techniques for modeling, measuring business value |
| Value chain | Economic value analysis technique (Porter) |
| Value network | Relationship and value exchange analysis |
| Value stream | End-to-end value-adding activities |
| Value stream decomposition | Breaking down into value stream stages |
| Value stream description | Defining value stream elements |
| Value stream map | Visual representation of all value streams |
| Value stream mapping | Process of creating value stream visualizations |
| Value stream mapping scenario | Practical application examples |
| Value stream stage | Individual value-adding activity within stream |

---

*Copyright © 2017, The Open Group. All rights reserved.*
