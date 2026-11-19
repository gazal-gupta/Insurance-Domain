# Module 25 – Lloyd's IT Landscape by Stage: Swimlane Process Views

| | |
|---|---|
| **Level** | Advanced – functional and technical |
| **Use it for** | Explaining the IT landscape to executives; current-state walkthroughs; requirements; integration design; target architecture |
| **Prerequisites** | [Module 23](23-Lloyds-Process-Catalogue.md) (process steps) and [Module 24](24-Lloyds-Systems-Documents-Data-Flow.md) (applications, documents, data) |

**How to read the swimlanes.** Each diagram is a swimlane: every vertical lane is **a party and the system it works in** (for example "Lloyd's broker – placing system"). Arrows are hand-offs, labelled with the document or data that moves. Notes show controls. Below each diagram, a table explains how each system is used at that stage, with its data in and data out.

**Tags.** Lloyd's systems CMR, MDC and ATLAS are confirmed on Lloyd's pages **[certain]**. Bureau component names (IMR, ECF, CLASS), Crystal, BEEDS and RegData are **[likely]**. Product names for firm-level systems are examples of the type only **[likely]**.

---

## 1. The landscape in seven layers

| Layer | Applications | Owner | Stages where used |
|---|---|---|---|
| **1. Client and distribution** | Client files; retail broker systems; Lloyd's broker placing and accounting systems; broker document management | Clients, brokers | 2, 4, 5, 8 |
| **2. Placement platforms** | PPL Next Gen, Whitespace **[likely]** | Market / vendors | 2, 4, 6, 10 |
| **3. Core insurance (managing agent)** | Submission ingestion; underwriting workbench; pricing; exposure and cat models; policy administration (PAS); claims; outwards reinsurance; sanctions screening; document management | Managing agent | 2–5, 8–10 |
| **4. Delegated authority** | Coverholder rating and policy systems; DCA claims systems; MA DA and bordereaux platform (e.g., Velonetic DA services such as DCOM **[likely]**) | Coverholders, DCAs, MA | 6, 7, 9 |
| **5. Market utilities** | Velonetic premium processing and signing; Insurers' Market Repository; central accounting and settlement; ECF and CLASS claims **[likely]** | Velonetic (via LIMOSS) | 5, 8, 9 |
| **6. Finance, risk and actuarial** | Technical accounting; general ledger; IFRS 17 / UK GAAP; reserving tools; capital model | Managing agent | 1, 5, 11 |
| **7. Data, AI and reporting** | Data platform; MI; AI services; Lloyd's CMR, MDC, SecureShare; ATLAS; Crystal; BoE BEEDS; FCA RegData | MA, Lloyd's, regulators | All |

### Lloyd's insurance stages used in this module

```mermaid
flowchart LR
  S1[1 Plan and capital] --> S2[2 Onboard and place]
  S2 --> S3[3 Underwrite]
  S3 --> S4[4 Bind and document]
  S4 --> S5[5 Premium and settlement]
  S2 --> S6[6 Coverholder set-up]
  S6 --> S7[7 Bordereaux and oversight]
  S5 --> S8[8 Open market claims]
  S7 --> S9[9 Delegated and cat claims]
  S8 --> S10[10 Reinsurance]
  S9 --> S10
  S10 --> S11[11 Reserve, close, report]
  S11 --> S1
```

---

## Stage 1 – Plan and capital

```mermaid
sequenceDiagram
  participant BRD as MA board<br/>Board papers
  participant CUO as CUO and class UW<br/>Planning models
  participant ACT as Actuarial<br/>Capital model and reserving tools
  participant FIN as Finance<br/>Ledger and data platform
  participant LLY as Lloyd's<br/>CMR and MDC
  participant MEM as Members<br/>Members' agent systems
  CUO->>FIN: Class plans - premium, rate, loss ratio
  FIN->>ACT: Draft plan data for capital modelling
  ACT->>ACT: Run model - SCR and uSCR
  FIN->>BRD: Plan and capital papers
  BRD-->>FIN: Approval
  FIN->>LLY: SBF and Lloyd's Capital Return
  Note over LLY: Lloyd's reviews plan and capital, may cap growth or add loadings
  LLY-->>FIN: Plan approval and capacity
  LLY->>MEM: Member capital requirement - ECA = uSCR x 1.35
  MEM->>LLY: Funds at Lloyd's - Coming into Line
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| CUO / class UW | Planning models (spreadsheets or planning tools) | Build class plans | Prior results, rate trends, market guidance | Class plans |
| Actuarial | Capital model; reserving tools | Calculate SCR/uSCR | Plan, exposures, reserves, RI | Capital results |
| Finance | Ledger; data platform | Consolidate plan; prepare returns | Actuals, plans | SBF, LCR |
| Lloyd's | CMR, MDC | Collect plans, capital, quarterly data | Returns | Approvals, feedback |
| Members | Members' agent systems | Track participations and FAL | Capital statements | FAL deposits |

**Watch points:** plan data built in spreadsheets with weak lineage; plan and capital data inconsistent; late Lloyd's challenges.

---

## Stage 2 – Onboard client and place the risk

```mermaid
sequenceDiagram
  participant CL as Client and retail broker<br/>Client files
  participant LB as Lloyd's broker<br/>Placing system and DMS
  participant SAN as Broker compliance<br/>Sanctions and KYC screening
  participant PLT as Placing platform<br/>PPL Next Gen or Whitespace
  participant ING as MA operations<br/>Submission ingestion
  participant WB as Lead underwriter<br/>Underwriting workbench
  CL->>LB: Instructions, SOV, loss runs
  LB->>SAN: Screen client and owners
  SAN-->>LB: KYC and sanctions cleared
  LB->>LB: Create UMR and draft MRC
  LB->>ING: Submission pack by email or platform
  ING->>WB: Structured risk data
  LB->>PLT: Electronic MRC for presentation
  PLT->>WB: Risk presented to lead
  Note over WB: Underwriting decision - see Stage 3
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Client / retail broker | Client files; retail broker system | Provide risk information | Client data | Instructions, SOV, loss runs |
| Lloyd's broker | Placing system; document management | Build submission and MRC; create UMR | Client documents | UMR, draft MRC, submission |
| Broker compliance | Screening service | KYC and sanctions | Party names, owners | Clearance record |
| Placing platform | PPL Next Gen / Whitespace | Share the MRC with underwriters | Draft MRC | Platform record |
| MA operations | Submission ingestion (AI-assisted) | Turn documents into data | Emails, PDFs, spreadsheets | Structured submission |
| Lead underwriter | Workbench | Receive and prioritise | Structured data | Work queue |

**Watch points:** the same risk data is keyed by broker and by each insurer; SOV quality decides cat model quality.

---

## Stage 3 – Underwrite

```mermaid
sequenceDiagram
  participant WB as Lead underwriter<br/>Workbench
  participant CMP as Compliance<br/>Sanctions screening and Crystal
  participant EXP as Exposure team<br/>Cat models
  participant PRC as Pricing<br/>Pricing models
  participant CUO as CUO<br/>Referral workflow
  participant PLT as Placing platform
  WB->>CMP: Parties, territory, class
  CMP-->>WB: Sanctions result and licensing and tax rules
  WB->>EXP: Locations and values
  EXP-->>WB: Modelled losses and aggregate headroom
  WB->>PRC: Rating factors and exposure
  PRC-->>WB: Technical price and rate adequacy
  WB->>CUO: Referral if outside authority
  CUO-->>WB: Approval with conditions
  WB->>PLT: Quote - terms, rate, line, subjectivities
  Note over WB: Decision and rationale saved as file note
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Lead underwriter | Workbench | Orchestrates checks; records decision | Submission data | Quote; file note |
| Compliance | Sanctions screening; Crystal **[likely]** | Screen parties; check licences and tax | Party, territory, class | Clear / refer; rules |
| Exposure | Cat models (e.g., Moody's RMS, Verisk) **[likely]** | Model event losses and aggregates | Geocoded locations, values | AAL, PML, aggregate use |
| Pricing | Pricing models | Technical price; RARC | Exposure, experience | Technical price; adequacy |
| CUO | Referral workflow | Approve outside-authority risks | Referral | Decision |
| Platform | PPL / Whitespace | Communicate quote | Terms | Quote record |

**Watch points:** checks done in separate tools without a single decision record; exposure checks monthly rather than at bind.

---

## Stage 4 – Bind, document and change

```mermaid
sequenceDiagram
  participant CL as Client
  participant LB as Lloyd's broker<br/>Placing system
  participant PLT as Placing platform
  participant LUW as Lead underwriter<br/>Workbench
  participant FUW as Follow underwriters<br/>Own workbenches
  participant PAS as MA operations<br/>Policy administration
  CL->>LB: Firm order
  LB->>PLT: Request lead line
  LUW->>PLT: Write and stamp lead line
  LB->>PLT: Show led MRC to followers
  FUW->>PLT: Write follow lines
  LB->>PLT: Sign down to 100 percent
  PLT->>PAS: Final MRC, signed lines, UMR
  PLT->>FUW: Final MRC, signed lines
  LB->>CL: Evidence of cover and contract documents
  Note over PAS: Mid-term change - MRC endorsement agreed under GUA, AP or RP processed
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Lloyd's broker | Placing system | Firm order; signing down; documentation | Lines | Final MRC; policy documents |
| Platform | PPL / Whitespace | Record lines, stamps and audit trail | Quotes, lines | Final electronic MRC |
| Lead / follow underwriters | Workbenches | Accept lines | Final terms | Written lines |
| MA operations | PAS (e.g., Sequel Eclipse, DXC Genius/Assure, Guidewire) **[likely]** | Book contract, lines, endorsements | Final MRC | Policy record; postings |

**Watch points:** PAS updated by re-keying rather than from the platform; written line booked and never corrected to signed line.

---

## Stage 5 – Premium accounting and central settlement

```mermaid
sequenceDiagram
  participant CL as Client
  participant LB as Lloyd's broker<br/>Broker accounting
  participant IMR as Velonetic<br/>Insurers' Market Repository
  participant PREM as Velonetic<br/>Premium processing and signing
  participant SET as Velonetic<br/>Central settlement
  participant TA as MA technical accounting<br/>Accounting and reconciliation
  participant GL as MA finance<br/>General ledger
  CL->>LB: Pays gross premium
  LB->>IMR: Upload MRC and supporting documents
  LB->>PREM: Premium advice - premium, tax, brokerage, lines
  PREM->>PREM: Validate against MRC
  PREM-->>LB: Query if data error
  PREM->>TA: Signed entries with SND
  LB->>SET: Net premium in settlement cycle
  SET->>TA: Settlement statement by syndicate
  TA->>TA: Three-way reconciliation - PAS, bureau, cash
  TA->>GL: Postings
  Note over TA: Aged debt chased - premium payment clause enforced
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Lloyd's broker | Broker accounting | Collect premium; submit to bureau; settle | Debit notes, MRC | Premium advice; payments |
| Velonetic IMR **[likely]** | Document repository | Store MRC and supporting documents | Documents | Linked documents |
| Velonetic premium processing | Bureau processing | Validate and sign | Premium advice | SND, signed entries |
| Velonetic settlement | Central settlement | Net cash between brokers and syndicates | Signed entries | Settlement statements |
| MA technical accounting | Accounting and reconciliation tools | Match bureau, PAS and cash | Signings, settlements, cash | Reconciled items; aged debt |
| MA finance | General ledger | Post premium | Reconciled entries | Accounts |

**Watch points:** bureau queries from data errors; written vs signed line breaks; FX differences; non-bureau insurers on the same contract processed separately.

---

## Stage 6 – Coverholder approval and binding authority set-up

```mermaid
sequenceDiagram
  participant CH as Coverholder<br/>Own systems
  participant LB as Lloyd's broker<br/>Placing system
  participant DA as MA DA team<br/>DA platform
  participant ATL as Lloyd's<br/>ATLAS
  participant PLT as Placing platform
  participant LUW as Lead underwriter<br/>Workbench
  LB->>DA: Introduce prospective coverholder
  DA->>CH: Due diligence request
  CH-->>DA: Financials, systems, staff, compliance
  DA->>ATL: Coverholder application
  Note over ATL: Referral criteria review where required
  CH->>ATL: Coverholder Undertaking
  ATL-->>DA: Approval - each location, conditional on binder within six months
  LB->>PLT: Binding authority on MRC format
  LUW->>PLT: Lead and follow lines on binder
  DA->>ATL: Register binder before inception
  DA->>DA: Load structured binder terms into contract register
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Coverholder | Own systems | Provide due diligence data; sign undertaking | Requests | Evidence, undertaking |
| Lloyd's broker | Placing system | Introduce; place binder | Proposal | Binder MRC |
| MA DA team | DA platform | Due diligence; contract register | Evidence, BAA | Structured binder terms |
| Lloyd's | ATLAS | Applications, approvals, records | Applications | Approval, permissions |
| Platform / lead UW | PPL / Whitespace; workbench | Agree binder terms and lines | Binder MRC | Bound binder |

**Watch points:** binder terms left in PDF; registration after inception; ATLAS records not maintained.

---

## Stage 7 – Delegated binding, bordereaux and oversight

```mermaid
sequenceDiagram
  participant CL as Insured and retail agent
  participant CH as Coverholder<br/>Rating and policy system
  participant LB as Lloyd's broker<br/>Broker accounting
  participant DA as MA DA team<br/>DA and bordereaux platform
  participant EXP as MA exposure<br/>Cat models
  participant TA as MA technical accounting
  participant AUD as Auditor<br/>Audit tools
  CL->>CH: Request cover
  CH->>CH: Rate and bind within authority, issue certificate
  CH->>DA: Monthly risk and premium bordereaux
  DA->>DA: Map to standard model and validate against binder terms
  DA-->>CH: Queries on exceptions
  DA->>EXP: Validated locations and values
  DA->>TA: Premium rows by binder
  CH->>LB: Net premium remittance
  LB->>TA: Settlement via bureau
  TA->>TA: Match premium rows to cash
  AUD->>CH: Risk-based audit
  AUD-->>DA: Findings and rating
  Note over DA: Oversight MI - timeliness, data quality, GPI use, loss ratio, breaches
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Coverholder | Rating and policy system | Bind within authority; produce bordereaux | Customer data | Certificates; bordereaux |
| MA DA team | DA platform (e.g., DCOM-type services or specialist platforms) **[likely]** | Ingest, map, validate; oversight MI | Bordereaux; binder terms | Validated rows; exceptions; MI |
| MA exposure | Cat models | Update aggregates and RDS | Validated locations | Aggregates |
| MA technical accounting | Accounting tools | Book and reconcile DA premium | Premium rows; cash | Reconciled premium |
| Auditor | Audit tools | Audit coverholder | Files, systems | Audit report |

**Watch points:** each coverholder layout different; each carrier on the binder processes the same file; exposure weeks out of date.

---

## Stage 8 – Open market claims

```mermaid
sequenceDiagram
  participant CL as Insured
  participant LB as Lloyd's broker<br/>Broker claims system
  participant ECF as Velonetic<br/>ECF and CLASS
  participant LEAD as Lead claims handler<br/>MA claims system
  participant SEC as Second lead<br/>Own claims system
  participant EXPT as Adjusters and lawyers
  participant TA as MA accounting
  CL->>LB: Notify loss
  LB->>ECF: Claim advice linked to UMR - UCR created
  ECF->>LEAD: Claim available for review
  LEAD->>LEAD: Triage standard or complex, check coverage and sanctions
  LEAD->>EXPT: Appoint adjuster and experts
  EXPT-->>LEAD: Reports
  LEAD->>SEC: Agreement needed if complex
  SEC-->>ECF: Agree
  LEAD->>ECF: Agree claim and reserve
  LB->>ECF: Settlement request
  ECF->>TA: Claim payment entries by syndicate
  ECF-->>LB: Funds via settlement
  LB->>CL: Pay claim
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Lloyd's broker | Broker claims system | Notify; present; request settlement | Client notice | Claim advice |
| Velonetic | ECF, CLASS **[likely]** | Share documents; record agreements and movements | Advices, agreements | UCR, TR, movements |
| Lead / second lead | MA claims systems | Triage, coverage, reserve, agree | Claim file | Agreement, reserve |
| Experts | Own tools | Investigate | Instructions | Reports |
| MA accounting | Accounting tools | Book payments | Claim entries | Postings |

**Watch points:** follower claims systems updated manually; complex/standard triage not recorded; sanctions check missed at payment.

---

## Stage 9 – Delegated and catastrophe claims

```mermaid
sequenceDiagram
  participant CL as Insured
  participant DCA as DCA or TPA<br/>DCA claims system
  participant DA as MA DA platform
  participant CLM as MA claims<br/>Claims system
  participant EXP as MA exposure<br/>Cat models
  participant RI as MA reinsurance<br/>RI system
  participant LLY as Lloyd's<br/>Major loss reporting
  CL->>DCA: Report claim
  DCA->>DCA: Handle and pay within authority from loss fund
  DCA->>CLM: Refer large or complex claims
  DCA->>DA: Monthly claims bordereau
  DA->>CLM: Validated claims rows with event code
  Note over EXP: Catastrophe event - event code assigned
  EXP->>CLM: Modelled loss estimate
  CLM->>LLY: Initial loss estimates
  CLM->>RI: Event-coded claims for recoveries
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| DCA / TPA | DCA claims system | Handle claims; loss fund accounting | Claims | Payments; claims bordereaux |
| MA DA platform | Bordereaux platform | Validate claims rows | Claims bordereaux | Validated claims |
| MA claims | Claims system | Referred claims; reserves; event coding | Referrals, rows | Reserves; event-coded claims |
| MA exposure | Cat models | Event loss estimates | Exposure, event footprint | Loss estimates |
| Lloyd's | Market reporting | Major loss estimates **[likely]** | Estimates | Market view |
| MA reinsurance | RI system | Recoveries | Event-coded claims | Collections |

---

## Stage 10 – Reinsurance

```mermaid
sequenceDiagram
  participant ACT as MA actuarial<br/>Capital model
  participant RI as MA reinsurance<br/>RI system
  participant RIB as Reinsurance broker<br/>Broker systems
  participant PLT as Placing platform
  participant RIN as Reinsurers<br/>Own systems
  participant PAS as MA policy admin
  participant TA as MA accounting
  ACT->>RI: Capital and RDS results
  RI->>RIB: Programme design
  RIB->>PLT: Reinsurance MRCs
  RIN->>PLT: Lines written
  PLT->>RI: Bound treaties
  PAS->>RI: Inwards risks for cessions
  RI->>TA: Ceded premium accounting
  RI->>RIB: Collection notes for recoverable claims
  RIB->>RIN: Collections
  RIN-->>TA: Recoveries paid
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| Actuarial | Capital model | Value capital benefit of cover | Exposures | uSCR change |
| MA reinsurance | RI system (e.g., specialist reinsurance administration systems) **[likely]** | Programme, cessions, recoveries | Treaties, risks, claims | Cessions, collections |
| Reinsurance broker | Broker systems; platforms | Place programme | Programme | Bound treaties |
| Reinsurers | Own systems | Accept and pay | Submissions, collections | Lines, payments |
| PAS / accounting | PAS; accounting | Feed risks; account for RI | Policy data | RI postings |

---

## Stage 11 – Reserve, close the year and report

```mermaid
sequenceDiagram
  participant CLM as MA claims<br/>Claims system
  participant ACT as MA actuarial<br/>Reserving tools
  participant SA as Signing actuary
  participant FIN as MA finance<br/>Ledger, IFRS 17 and UK GAAP
  participant DP as MA data<br/>Data platform
  participant LLY as Lloyd's<br/>CMR, MDC, SecureShare
  participant REG as Regulators<br/>BEEDS and RegData
  participant MEM as Members
  CLM->>ACT: Paid and outstanding by YOA and class
  ACT->>ACT: IBNR and ultimates
  ACT->>SA: Reserve analysis
  SA-->>LLY: Statement of Actuarial Opinion
  ACT->>FIN: Booked reserves
  FIN->>FIN: Close year of account by RITC at 36 months
  FIN->>MEM: Results, distributions or cash calls
  DP->>FIN: Reporting data
  FIN->>LLY: Quarterly and annual returns
  FIN->>REG: Solvency and regulatory returns
```

| Lane | System | How it is used | Data in | Data out |
|---|---|---|---|---|
| MA claims | Claims system | Provide claims data | Claims | Triangles input |
| Actuarial | Reserving tools (e.g., ResQ, Arius) **[likely]** | Reserve analysis | Triangles | Reserves, RITC pricing |
| Signing actuary | Own tools | Independent opinion | Reserve analysis | SAO |
| Finance | Ledger; IFRS 17 / UK GAAP | Accounts; YOA closure | Reserves, premium | Accounts, RITC, member results |
| Data platform | Data platform | Single reporting data | All domains | Reporting datasets |
| Lloyd's | CMR, MDC, SecureShare | Collect returns | Returns | Market oversight |
| Regulators | BEEDS, RegData **[likely]** | Collect returns | Returns | Supervision |

---

## 2. Application × stage matrix

● = main use; ○ = supporting use.

| Application | 1 Plan | 2 Place | 3 UW | 4 Bind | 5 Premium | 6 CH set-up | 7 BDX | 8 Claims | 9 DA/cat claims | 10 RI | 11 Report |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Broker placing and accounting | — | ● | ○ | ● | ● | ○ | ○ | ● | — | ○ | — |
| PPL / Whitespace | — | ● | ○ | ● | — | ● | — | — | — | ● | — |
| Submission ingestion | — | ● | ○ | — | — | — | — | — | — | — | — |
| Underwriting workbench | ○ | ○ | ● | ● | — | ○ | — | — | — | — | — |
| Pricing models | ● | — | ● | — | — | — | — | — | — | ○ | — |
| Exposure and cat models | ● | — | ● | — | — | — | ● | — | ● | ● | ○ |
| Policy administration | ○ | — | — | ● | ● | — | ○ | ○ | — | ● | ○ |
| DA and bordereaux platform | ○ | — | — | — | ○ | ● | ● | — | ● | — | ○ |
| Coverholder systems | — | — | — | — | — | ○ | ● | — | ○ | — | — |
| Velonetic premium, IMR, settlement | — | — | — | — | ● | — | ○ | ○ | — | ○ | — |
| ECF and CLASS | — | — | — | — | — | — | — | ● | ○ | ○ | — |
| MA claims system | — | — | — | — | — | — | — | ● | ● | ○ | ○ |
| DCA claims systems | — | — | — | — | — | — | — | — | ● | — | — |
| Outwards RI system | ○ | — | — | — | — | — | — | ○ | ○ | ● | ○ |
| Technical accounting | — | — | — | — | ● | — | ● | ○ | ○ | ● | ○ |
| Reserving tools | ○ | — | — | — | — | — | — | — | — | — | ● |
| Capital model | ● | — | — | — | — | — | — | — | — | ● | ○ |
| General ledger / IFRS 17 | ○ | — | — | — | ● | — | — | — | — | ○ | ● |
| Data platform and MI | ● | ○ | ○ | ○ | ○ | ○ | ● | ○ | ○ | ○ | ● |
| Sanctions screening | — | ● | ● | — | — | ○ | ○ | ● | ○ | — | — |
| ATLAS | — | — | — | — | — | ● | ● | — | — | — | — |
| Crystal | — | — | ● | — | ○ | — | ○ | — | — | — | — |
| CMR / MDC / SecureShare | ● | — | — | — | — | — | — | — | ○ | — | ● |
| BEEDS / RegData | — | — | — | — | — | — | — | — | — | — | ● |

---

## 3. How to use these views with a client

| Situation | How to use the swimlanes |
|---|---|
| Executive briefing | Show the seven layers and one stage swimlane; point to the hand-offs where cost and errors build up |
| Current-state workshop | Replace generic lanes with the client's real systems; mark each arrow as automated, manual or re-keyed |
| Target architecture | Redraw each stage with integrations replacing manual arrows; name golden sources |
| Vendor selection | Script demos from the swimlanes (e.g., Stage 4 signing down; Stage 7 bordereaux validation) |
| AI use cases | Look for arrows carrying unstructured documents (submissions, bordereaux, claims reports) – these are the best AI candidates |

---

## 4. Partner's lens

1. **One stage, one slide.** Executives absorb one swimlane at a time. Lead with the stage that hurts most (often Stage 5 or Stage 7) and show the cost of its manual arrows.
2. **Colour the arrows.** In workshops, colour each hand-off green (integrated), amber (file transfer) or red (re-keyed). The red arrows are the business case.
3. **Separate market from firm.** Lanes owned by Velonetic, platforms and Lloyd's change on the market's timetable; lanes owned by the client change on theirs. Prioritise what the client controls.
4. **Keep it current.** Bureau services and platforms are changing after Blueprint Two. Date every landscape diagram and refresh it at least once a year.

---

## 5. Practice tasks

1. Redraw Stage 5 and Stage 7 with a real client's applications and colour every arrow.
2. Pick one stage and write the target-state version with integrations and golden sources.
3. Identify five red arrows across all stages and size the value of automating each (method in [Module 11 §5](11-Consulting-Playbook.md)).

---

## 6. Sources

- [Lloyd's – Core Market Returns](https://www.lloyds.com/market-resources/tools/core-market-returns)
- [Lloyd's – Market Data Collections](https://www.lloyds.com/market-resources/tools/market-data-collections)
- [Lloyd's – new coverholder applications (ATLAS)](https://www.lloyds.com/market-resources/delegated-authorities/coverholders/new-coverholder-applications)
- [Keoghs – Lloyd's Claims Lead Arrangements](https://keoghs.co.uk/keoghs-insight/keoghs-guide-to-lloyds-claims-lead-arrangements)
- [Crunchbase – Velonetic profile](https://crunchbase.com/organization/velonetic)
- [Insurance Insider – PPL Next Gen goes live](https://www.insuranceinsider.com/article/2bd65d4pn7amg8t7mmadc/london-market-section/ppl-next-gen-platform-goes-live-after-delays)
