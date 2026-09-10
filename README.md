\# NetSage AI â€” Applied AI + Network Troubleshooting



\## 1. Project Overview



NetSage AI is an AI-assisted network troubleshooting system designed to help junior network engineers diagnose common connectivity and configuration problems.



The system takes network symptoms, topology information, and command output as evidence. It then produces a structured diagnosis containing:



\* Likely root cause

\* Confidence level

\* Evidence

\* OSI layer

\* Affected network entity

\* Recommended next command

\* Suggested fix steps



The system also includes a deterministic rule checker and a human-review workflow so that configuration changes are not accepted automatically.



\---



\## 2. Problem Statement



Network troubleshooting can be difficult for junior engineers because a single connectivity problem may have several possible causes.



For example, a device that cannot access another network may have:



\* A missing VLAN

\* An incorrect gateway

\* A wrong subnet mask

\* A missing route

\* An interface that is shut down

\* An ACL blocking traffic

\* A NAT configuration problem

\* A wireless configuration problem



NetSage AI organizes the troubleshooting process and provides evidence-based diagnostic suggestions.



\---



\## 3. Main Features



\### 3.1 Network Troubleshooting Cases



The project contains 30 troubleshooting cases covering:



\* VLAN

\* Gateway

\* DHCP

\* DNS

\* Routing

\* ACL

\* NAT

\* Wireless



Each case contains:



\* Case ID

\* Issue type

\* Symptom

\* Topology notes

\* Show-command output

\* Expected fault

\* OSI layer

\* Networking concept

\* Severity



\---



\### 3.2 Structured AI Diagnosis



The diagnosis engine produces a structured response:



```text

Root Cause

Confidence

Evidence

OSI Layer

Affected Entity

Next Command

Fix Steps

```



The system uses the supplied case evidence rather than generating unsupported command output.



\---



\### 3.3 Deterministic Rule Checker



A rule-based checker is included to identify basic configuration problems.



The checker currently contains rules for:



\* Missing VLAN

\* Duplicate IP address

\* Incorrect subnet mask

\* Gateway mismatch

\* Interface down

\* Missing route



The rule checker provides PASS/FAIL results and an overall status.



This provides a deterministic validation layer alongside the diagnosis engine.



\---



\### 3.4 Human-in-the-Loop Review



Network configuration changes should not be accepted automatically.



The project therefore includes human review with three possible decisions:



```text

Accepted

Edited

Rejected

```



Five cases were specifically recorded where the initial diagnosis was edited by a human reviewer.



This demonstrates responsible AI usage and keeps the final decision with the network engineer.



\---



\## 4. System Workflow



```text

Network Symptoms

&#x20;      |

&#x20;      v

Topology + Show Output

&#x20;      |

&#x20;      v

Case Dataset

&#x20;      |

&#x20;      v

Diagnosis Engine

&#x20;      |

&#x20;      +------------------+

&#x20;      |                  |

&#x20;      v                  v

AI Diagnosis       Deterministic

&#x20;                  Rule Checker

&#x20;      |                  |

&#x20;      +--------+---------+

&#x20;               |

&#x20;               v

&#x20;       Human Review

&#x20;               |

&#x20;      +--------+--------+

&#x20;      |        |        |

&#x20;   Accepted  Edited  Rejected

&#x20;      |

&#x20;      v

&#x20;    Results

&#x20;      |

&#x20;      v

&#x20;  Dashboard

```



\---



\## 5. Project Structure



```text

NetSage-AI/

â”‚

â”œâ”€â”€ data/

â”‚   â”œâ”€â”€ cases.csv

â”‚   â””â”€â”€ evidence/

â”‚

â”œâ”€â”€ prompts/

â”‚   â””â”€â”€ diagnose\_prompt.md

â”‚

â”œâ”€â”€ src/

â”‚   â”œâ”€â”€ ai\_engine.py

â”‚   â”œâ”€â”€ rule\_checker.py

â”‚   â””â”€â”€ review.py

â”‚

â”œâ”€â”€ results/

â”‚   â”œâ”€â”€ results.csv

â”‚   â”œâ”€â”€ responsible\_ai\_log.csv

â”‚   â””â”€â”€ evaluation.json

â”‚

â”œâ”€â”€ dashboard/

â”‚   â””â”€â”€ index.html

â”‚

â”œâ”€â”€ scripts/

â”‚   â”œâ”€â”€ run\_cases.py

â”‚   â”œâ”€â”€ human\_review.py

â”‚   â”œâ”€â”€ evaluate.py

â”‚   â””â”€â”€ create\_dashboard.py

â”‚

â”œâ”€â”€ tests/

â”‚

â”œâ”€â”€ requirements.txt

â””â”€â”€ README.md

```



\---



\## 6. Dataset



The dataset contains 30 network troubleshooting cases.



| Category  | Number of Cases |

| --------- | --------------: |

| VLAN      |               4 |

| Gateway   |               4 |

| DHCP      |               4 |

| DNS       |               3 |

| Routing   |               4 |

| ACL       |               4 |

| NAT       |               4 |

| Wireless  |               3 |

| \*\*Total\*\* |          \*\*30\*\* |



The cases cover common network configuration problems and provide evidence that can be used during diagnosis.



\---



\## 7. Diagnosis Process



For each case, the system:



1\. Reads the case information.

2\. Identifies the issue category.

3\. Generates a structured diagnosis.

4\. Includes the supplied command output as evidence.

5\. Identifies the relevant OSI layer.

6\. Recommends a useful next troubleshooting command.

7\. Provides corrective steps.

8\. Runs deterministic checks.

9\. Records the result.

10\. Sends the result through human review.



\---



\## 8. Responsible AI



Human oversight is an important part of NetSage AI.



The system does not treat an automated diagnosis as an unquestionable configuration change.



The responsible AI log records five examples where the human reviewer modified the initial diagnosis.



Examples include:



\* Verifying the client VLAN and DHCP configuration before changing a gateway.

\* Checking DHCP exclusions and active leases before declaring a pool exhausted.

\* Verifying routing between a client VLAN and DNS server.

\* Confirming ACL direction and interface placement before changing an ACL.

\* Verifying guest isolation policy and ACL configuration.



These examples demonstrate that the AI recommendation should be reviewed against the actual network environment.



\---



\## 9. Evaluation



The current deterministic baseline was executed against all 30 cases.



```text

Total cases       : 30

Processed cases   : 30

Diagnosis matches : 30

Match rate        : 100.0%



Human review:

&#x20; Accepted : 25

&#x20; Edited   : 5

&#x20; Rejected : 0

```



The responsible AI requirement is satisfied because five human corrections are recorded.



\### Important Note



The current implementation is a deterministic baseline for demonstrating the complete troubleshooting workflow. The reported 100% match rate represents matching the prepared case expectations and should not be interpreted as real-world LLM accuracy.



A future version can connect the diagnosis layer to a local or hosted language model and evaluate its predictions independently.



\---



\## 10. Dashboard



The project includes an HTML dashboard.



The dashboard displays:



\* Total number of cases

\* Processed cases

\* Human decisions

\* Issue-type distribution

\* Severity distribution

\* Deterministic rule-check results

\* Human corrections

\* Individual case results



The dashboard can be opened directly from:



```text

dashboard/index.html

```



\---



\## 11. Running the Project



Open PowerShell in the project directory:



```powershell

cd C:\\NetSage-AI

```



\### Run the troubleshooting cases



```powershell

python scripts\\run\_cases.py

```



\### Run human review



```powershell

python scripts\\human\_review.py

```



\### Evaluate the results



```powershell

python scripts\\evaluate.py

```



\### Generate the dashboard



```powershell

python scripts\\create\_dashboard.py

```



Then open:



```text

dashboard/index.html

```



\---



\## 12. Example Diagnosis



Example:



```text

Issue:

Incorrect default gateway



Root Cause:

Incorrect default gateway



Confidence:

High



Evidence:

Supplied router/client configuration output



OSI Layer:

Layer 3 â€” Network



Next Command:

show ip interface brief



Fix:

1\. Verify the configured gateway.

2\. Correct the gateway configuration.

3\. Repeat the relevant show command.

4\. Test connectivity again.

5\. Have a network engineer review the change.

```



\---



\## 13. Technologies Used



\* Python

\* CSV

\* HTML

\* CSS

\* JavaScript

\* Networking concepts

\* OSI model

\* Deterministic rule-based validation

\* Structured AI diagnosis

\* Human-in-the-loop review



\---



\## 14. Limitations



The current version uses a deterministic diagnosis baseline rather than a live large language model.



It also works with prepared troubleshooting evidence rather than directly connecting to a live Cisco Packet Tracer session.



Therefore, it should be considered a prototype demonstrating the troubleshooting workflow.



\---



\## 15. Future Improvements



Future versions could include:



1\. Direct Packet Tracer evidence collection.

2\. Real LLM integration.

3\. Automated parsing of Cisco `show` commands.

4\. More sophisticated network configuration validation.

5\. Real-time troubleshooting assistance.

6\. Historical troubleshooting knowledge base.

7\. Confidence calibration.

8\. Interactive network topology visualization.

9\. Automatic comparison between AI and expert diagnosis.

10\. Integration with real network monitoring systems.



\---



\## 16. Conclusion



NetSage AI demonstrates how AI-assisted reasoning, deterministic validation, and human expertise can be combined for network troubleshooting.



The system covers 30 troubleshooting scenarios, provides evidence-based structured diagnoses, performs deterministic checks for common configuration errors, records human corrections, and presents the results through a dashboard.



The key principle of the project is:



> AI assists the network engineer; the human engineer makes the final decision.





