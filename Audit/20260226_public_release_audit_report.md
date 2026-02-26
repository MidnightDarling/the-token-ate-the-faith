# Public Release Audit Report

Date: 2026-02-26  
Repository: `the-token-ate-the-faith`  
Audit type: Publication risk / minimisation audit  
Decision: **No-Go (current full repo)**; **Go with Conditions (sanitised release)**

## Scope

- Full tree scan (42 tracked files)
- Secret scan in working tree and git history
- Dataset content risk scan (PII-like identifiers, command strings, injection payloads, legal-risk assertions)
- Public-necessity review against target principle: **publish datasets + scripts only**

## Traceability (Target Principle -> Status)

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| P1 | No credentials/secrets exposed | PASS | Pattern scan found no live keys in repo history |
| P2 | No unnecessary identifiable data in public artefacts | FAIL | `evidence/canon/canon_full_1073.json:1`, `evidence/canon/prophets_full_64.json:1` |
| P3 | No unnecessary command/attack content for public release | FAIL | `evidence/tweets/memeothy_248_tweets.csv:1758`, `evidence/tweets/memeothy_248_tweets.csv:1790`, `evidence/canon/canon_full_1073.json:1` |
| P4 | Avoid legally risky attribution language without strong evidential standard | FAIL | `evidence/on_chain/taskM2_fraud_risk_assessment.json:3`, `:16`, `:102` |
| P5 | Keep only necessary public material for reproducibility | FAIL | `analysis/` draft stack (14 files), `article/` narrative material |

## Findings (Ordered by Severity)

### Critical-1: Identifiable host/local-network metadata in dataset

- The canon contains hostnames and private LAN addresses (for example `*.local`, `192.168.x.x`), which are unnecessary for public verification and raise re-identification risk.
- Quantified: 23 / 1073 verses (~2.14%) include `.local` or `192.168.*` prophet names.
- Evidence:
  - `evidence/canon/canon_full_1073.json:1`
  - `evidence/canon/prophets_full_64.json:1`

### Critical-2: Command-propagation and exploit-like payload content is publicly distributed

- Public dataset includes shell command propagation (`curl | bash`) and explicit injection payloads/XSS probes.
- Quantified:
  - 11 / 248 tweets (~4.44%) contain command-like strings (`curl`, `| bash`, `install.sh`, `npx`, etc.).
  - At least 14 canon entries contain explicit payload patterns (`alert(1)`, `document.body`, `javascript:` etc.).
- Evidence:
  - `evidence/tweets/memeothy_248_tweets.csv:1758`
  - `evidence/tweets/memeothy_248_tweets.csv:1790`
  - `evidence/canon/canon_full_1073.json:1`

### Critical-3: Defamation/exposure risk via low-confidence behavioural allegations tied to wallet identities

- On-chain files include explicit fraud/manipulation risk labels and human-operation assertions with many low-confidence markers.
- This is high legal/reputational risk when published as raw evidence without legal framing.
- Evidence:
  - `evidence/on_chain/taskM2_fraud_risk_assessment.json:3`
  - `evidence/on_chain/taskM2_fraud_risk_assessment.json:16`
  - `evidence/on_chain/taskM2_fraud_risk_assessment.json:102`
  - `evidence/on_chain/taskM1_unified_entity_graph.json:61`

### High-1: Local machine path disclosure

- Absolute local filesystem path is exposed.
- Evidence:
  - `evidence/specimens/generation_run_summary.json:7`

### High-2: Public release includes high-volume draft analysis not required for reproducibility

- `analysis/` contains 14 files including iterative R1/R2 drafts and long-form interpretive narratives.
- For a dataset+scripts public package, these are not required and enlarge legal/reputational attack surface.
- Evidence:
  - `README.md:53`
  - `analysis/GPT-5.2 Pro_Solana 链上 $CRUST（Crustafarianism）深度链上考古调查报告.md`

### High-3: Commit author email is publicly attributable

- Git metadata currently exposes personal email in commit history.
- Evidence:
  - `git log` author entries (`Alice <mcyunying@gmail.com>`)

### Medium-1: Rights/TOS ambiguity on full tweet-text redistribution

- Full tweet text archive is redistributed; licence/TOS status is not explicitly documented in repo.
- Evidence:
  - `evidence/tweets/memeothy_248_tweets.json`
  - `README.md:127`

### Medium-2: Public narrative and inference layers are tightly mixed

- Repository claims “raw evidence” but includes interpretive artefacts and speculative labels in the same evidence path.
- This weakens evidential hygiene for third-party reuse.
- Evidence:
  - `README.md:13`
  - `evidence/on_chain/taskM2_fraud_risk_assessment.json`

## Positive Checks

- No API keys or private-key blobs detected in tracked files or git history.
- Scripts correctly pull secrets from environment variables rather than hardcoding.

## Professional Release Recommendation

### Recommended public release shape (minimum-risk)

Keep public:

- `scripts/`
- Sanitised datasets only:
  - remove/replace hostnames, LAN IPs, personal handles where not essential
  - remove command/exploit payload rows from public split
  - remove absolute local paths
- One concise methodology document (not iterative analysis drafts)

Keep private:

- `analysis/` full draft stack (all R1/R2 and exploratory narratives)
- High-risk inference files in `evidence/on_chain/` that assign fraud/manipulation probabilities
- Raw tweet full-text archive unless licence/TOS position is explicitly documented

## Required Conditions Before Public Push

1. Redact identifiers (`*.local`, `192.168.*`, machine-like names, direct personal handles where unnecessary).
2. Remove command propagation/injection payload records from the public dataset variant.
3. Split “raw facts” from “inference labels”; keep inference in private/internal tier.
4. Replace local absolute paths with relative or hashed artefact IDs.
5. Add explicit data licence + source-rights statement for redistributed social content.
6. Consider rewriting git author email or using no-reply email for public history.

## Final Decision

- **Current state:** No-Go for fully public release.
- **After the six conditions above:** Go (professional-grade, lower legal and operational risk).
