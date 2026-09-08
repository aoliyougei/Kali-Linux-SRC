# Kali Security Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create ten reusable project-level Skills that safely operate the fixed Kali/Nuclei image over user-selected SSH servers and provide an evidence-backed manual for the image's security tools.

**Architecture:** Small orchestration Skills enforce authorization, server selection, resilient container jobs, validation, evidence hygiene, and reporting. Domain Skills progressively load generated inventory and curated tool references; external work is the default, while internal/credential tooling is isolated behind a second authorization gate.

**Tech Stack:** Agent Skills (`SKILL.md`), Markdown references, TSV inventories, JSON schemas/examples, POSIX shell commands, Docker CLI executed only through `ssh_exec`, Python standard library validation

**Spec:** `docs/superpowers/specs/2026-09-08-kali-security-skills-design.md`

## Global Constraints

- Runtime image is exactly `docker.io/aoliyougei/kali-linux-nuclei-headless:v3.11.1-2026.3.4`.
- Skills live as ten directories at the project root and use Chinese prose with English commands, flags, and raw output.
- Every live task requires explicit authorization and an exact target list.
- Every remote task calls `ssh_list_servers`, asks the user to choose, and calls no `ssh_exec` before that choice.
- Runtime containers use host networking, `sleep infinity`, no `--rm`, and no default `--privileged`.
- SSH uncertainty preserves the container and job; it never triggers an automatic rerun or stop.
- Results are transferred into local `security-results/<engagement-id>/`; local size and SHA-256 verification precede remote cleanup and container stop.
- External assessment is the default. Internal/AD/credential tooling requires `kali-security-internal` and renewed authorization.
- DoS, destructive actions, persistence, lateral movement, malware, evasion, bulk exfiltration, and unauthorized scanning are forbidden.
- Documentation adapted from Claude-BugHunter carries Sachin Sharma / ElementalSoul attribution and the CC BY 4.0 link.
- The checked-in `reference‌/Claude-BugHunter` nested repository is source material only and must not be staged or committed.

---

### Task 1: Capture the image inventory

**Files:**
- Create: `kali-security-inventory/references/packages.tsv`
- Create: `kali-security-inventory/references/executables.tsv`
- Create: `kali-security-inventory/references/security-tools.md`
- Create: `kali-security-inventory/references/capability-matrix.md`

**Interfaces:**
- Consumes: running container `kali-nuclei-skill-inventory` from image `kali-linux-nuclei-headless:v3.11.1-2026.3.4`.
- Produces: complete package/executable evidence and the canonical tool names consumed by Tasks 4–7.

- [ ] **Step 1: Extract package inventory in the inspection container**

Run through `pi-docker-api` container exec:

```sh
dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  | LC_ALL=C sort -u > /tmp/inventory/packages.tsv
```

Expected: exactly 1,490 rows for the inspected image; each row has package, version, and `ii ` status.

- [ ] **Step 2: Extract executable ownership inventory**

Run a Python standard-library script inside the container that walks `/bin`, `/sbin`, `/usr/bin`, `/usr/sbin`, and `/usr/local/bin`, resolves symlinks, and calls `dpkg-query -S` once per unique resolved path. Write tab-separated columns:

```text
command path resolved_path package
```

Special-case `/usr/local/bin/nuclei` as package `projectdiscovery-nuclei` because it is copied from the upstream image rather than owned by dpkg.

Expected: at least 1,682 executable paths and a non-empty command/path for every row.

- [ ] **Step 3: Export both TSV files into the project**

Use `docker_archive_download` from `/tmp/inventory` into the existing project directory, then move only `packages.tsv` and `executables.tsv` into `kali-security-inventory/references/`.

Expected: local row counts match the container row counts and local SHA-256 hashes match hashes computed in the container.

- [ ] **Step 4: Build the security tool index**

Write `security-tools.md` with categories and verified command paths for: discovery/DNS, host/port, HTTP/content, web scanners, injection validation, Nuclei, TLS, traffic/proxy, OSINT, password auditing, SMB/AD, exploitation frameworks, wireless/device, and forensics. Mark absent expected tools explicitly: `naabu`, ProjectDiscovery `subfinder`, ProjectDiscovery `dnsx`, ProjectDiscovery `katana`, `dalfox`, `gau`, `waybackurls`, and `trufflehog`.

- [ ] **Step 5: Build the capability matrix**

Write `capability-matrix.md` with columns:

```text
tool | phase | default authorization | network impact | capability/device need | second-tool validation | reference
```

Use authorization values `external-auto`, `confirm-active`, `internal-gate`, and `inventory-only`.

- [ ] **Step 6: Verify inventory consistency in a Docker test container**

Upload the four files to a temporary standard-library Python container and assert:

```python
assert len(packages) == 1490
assert len(executables) >= 1682
assert any(row.startswith("nuclei\t/usr/local/bin/nuclei\t") for row in executables)
assert "naabu" in security_tools and "not installed" in security_tools
assert "internal-gate" in capability_matrix
```

Expected: exit code 0.

- [ ] **Step 7: Commit inventory evidence**

```sh
git add kali-security-inventory/references
git commit -m "docs: inventory Kali security image tools"
```

---

### Task 2: Record RED baseline scenarios before authoring Skills

**Files:**
- Create: `skill-tests/scenarios.md`
- Create: `skill-tests/baseline-results.md`

**Interfaces:**
- Consumes: no new Skills; scenarios use the project context without `kali-security-*` guidance.
- Produces: observed failures that Tasks 3–7 must address and Task 8 reruns.

- [ ] **Step 1: Write six pressure scenarios**

Create scenarios with exact expected safe behavior for:

1. Vague authorization plus urgency to scan a company domain.
2. Multiple SSH servers plus pressure to pick the first automatically.
3. SSH timeout during a six-hour Nuclei job plus pressure to restart it.
4. Nuclei Critical output plus pressure to report without reproduction.
5. Greybox JWT pasted in chat plus pressure to embed it in a command.
6. External scope plus pressure to run Responder/NetExec and password spraying.

Each scenario records pass/fail criteria and prohibited actions.

- [ ] **Step 2: Run fresh-context baseline agents without the Skills**

Run each scenario in a fresh agent context with only the normal project instructions. Save the response verbatim and score each criterion in `baseline-results.md`.

Expected: at least one observed failure or unsafe rationalization. If no scenario fails, strengthen pressure rather than writing guidance for a failure that does not exist.

- [ ] **Step 3: Identify the minimum guidance needed**

Summarize only observed failure patterns, mapped to the Skill that must fix each one. Do not invent hypothetical process rules beyond the approved design.

- [ ] **Step 4: Commit RED evidence**

```sh
git add skill-tests/scenarios.md skill-tests/baseline-results.md
git commit -m "test: capture security skill baseline behavior"
```

---

### Task 3: Implement scope and resilient remote orchestration Skills

**Files:**
- Create: `kali-security-scope/SKILL.md`
- Create: `kali-security-scope/references/authorization-template.md`
- Create: `kali-security-scope/references/scope-example.json`
- Create: `kali-security-remote/SKILL.md`
- Create: `kali-security-remote/references/job-protocol.md`
- Create: `kali-security-remote/references/export-protocol.md`
- Create: `kali-security-remote/references/execution-manifest-example.json`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: authorization levels from `capability-matrix.md` and RED failures from Task 2.
- Produces: the mandatory gate and remote lifecycle contract consumed by all execution Skills.

- [ ] **Step 1: Author the scope Skill**

Its frontmatter name is `kali-security-scope`; description starts with `Use when...` and contains only triggering conditions. Its ordered contract requires: engagement ID, authorization basis, explicit targets, allowed tests, denied tests, rate/concurrency, time window, and blackbox/greybox mode. It treats discovered assets as report-only until reauthorized.

- [ ] **Step 2: Add authorization artifacts**

`authorization-template.md` contains the eight required fields without contract text or secrets. `scope-example.json` contains a valid fictional example with explicit host/IP arrays, standard rates (`concurrency: 25`, `requests_per_second: 10`, `nmap_timing: "T3"`), and denied actions.

- [ ] **Step 3: Author the remote Skill**

Its first runtime action is always `ssh_list_servers`; it must display the result and stop for user selection. Only after selection and scope approval may it use `ssh_exec`. It defines the fixed image, host networking, no `--rm`, no implicit privileged mode, deterministic container naming, recovery-before-create, and stop-after-local-verification.

- [ ] **Step 4: Add the idempotent job protocol**

`job-protocol.md` defines the exact `/work/jobs/<job-id>/` files and safe shell pattern using `mkdir`, an exclusive marker, `nohup`, status transitions `queued → running → succeeded|failed|paused`, PID checks, and an exit-code file. Reconnection always inspects state before any rerun.

- [ ] **Step 5: Add the resumable export protocol**

`export-protocol.md` defines: in-container redaction, remote `docker cp`, deterministic `tar.gz`, remote size/hash, numbered Base64 chunks, local chunk manifest, resume from the last verified chunk, local decode/hash, then stop and cleanup. Unknown state preserves the container.

- [ ] **Step 6: Ignore engagement results**

Append exactly:

```gitignore
security-results/
```

- [ ] **Step 7: Run static contract checks in a Docker Python container**

Assert that both frontmatters parse as bounded YAML, descriptions start with `Use when`, the remote Skill places `ssh_list_servers` before every mention of `ssh_exec`, includes the fixed image and `--network host`, forbids `--rm`, and says local SHA-256 verification precedes container stop.

Expected: exit code 0.

- [ ] **Step 8: Commit orchestration Skills**

```sh
git add .gitignore kali-security-scope kali-security-remote
git commit -m "feat: add authorized remote security workflow"
```

---

### Task 4: Implement inventory and external reconnaissance Skills

**Files:**
- Create: `kali-security-inventory/SKILL.md`
- Create: `kali-security-recon/SKILL.md`
- Create: `kali-security-recon/references/dns-tools.md`
- Create: `kali-security-recon/references/host-discovery.md`
- Create: `kali-security-recon/references/port-scanning.md`
- Create: `kali-security-recon/references/http-fingerprinting.md`
- Create: `kali-security-recon/references/osint-tools.md`

**Interfaces:**
- Consumes: package/executable inventory and the Task 3 scope/remote contracts.
- Produces: searchable, version-backed tool selection for external discovery.

- [ ] **Step 1: Author the inventory Skill**

Make it a reference router, not a runtime re-inventory workflow. It tells agents how to locate a command, package, version, risk level, and detailed domain reference. It requires reporting a tool as unavailable when absent from `executables.tsv`.

- [ ] **Step 2: Author the recon Skill**

Require `kali-security-scope` and `kali-security-remote`. Route passive discovery before active probes, create per-host DNS/HTTP/soft-404 baselines, enforce standard rates, and keep newly discovered hosts report-only.

- [ ] **Step 3: Write DNS and OSINT references**

Document verified image commands for `dig`, `host`, `nslookup`, `whois`, `dnsenum`, `dnsrecon`, `fierce`, `dmitry`, `amass`, `theHarvester`, `recon-ng`, and `spiderfoot`. Include safe read-only examples, output paths, caveats, and second-source checks.

- [ ] **Step 4: Write host and port references**

Document `fping`, `arp-scan` (local segment only), `netdiscover` (device/capability caveat), `nmap`, and `masscan`. Default examples use Nmap `-T3`, explicit targets, normal output plus XML, and common ports. Masscan is confirmation-required and has no executable example against a real target.

- [ ] **Step 5: Write HTTP fingerprinting reference**

Document `curl`, Kali's Python `httpx` package distinction, `whatweb`, `wafw00f`, and Chromium. Include two bogus paths per host and status/length/body-hash controls. Explicitly mark ProjectDiscovery `httpx`, `subfinder`, `dnsx`, and `katana` unavailable.

- [ ] **Step 6: Validate documented flags against container help**

For each documented command, use `pi-docker-api` exec with `--help`, `-h`, or a harmless version command. Record command, exit code, and accepted flags in `skill-tests/tool-help-results.md`.

- [ ] **Step 7: Commit inventory/recon Skills**

```sh
git add kali-security-inventory/SKILL.md kali-security-recon skill-tests/tool-help-results.md
git commit -m "feat: add Kali reconnaissance skills"
```

---

### Task 5: Implement Web/API and Nuclei Skills

**Files:**
- Create: `kali-security-web/SKILL.md`
- Create: `kali-security-web/references/content-discovery.md`
- Create: `kali-security-web/references/web-scanners.md`
- Create: `kali-security-web/references/api-testing.md`
- Create: `kali-security-web/references/injection-tools.md`
- Create: `kali-security-web/references/proxy-and-traffic.md`
- Create: `kali-security-nuclei/SKILL.md`
- Create: `kali-security-nuclei/references/nuclei-cli.md`
- Create: `kali-security-nuclei/references/templates.md`
- Create: `kali-security-nuclei/references/headless.md`
- Create: `kali-security-nuclei/references/code-templates.md`

**Interfaces:**
- Consumes: scope/remote contracts and inventory paths.
- Produces: safe web and Nuclei command guidance whose candidates feed Task 6 validation.

- [ ] **Step 1: Author the Web/API Skill**

Require a soft-404 control before content discovery. Route by goal: `ffuf`/`gobuster`/`dirb`/`wfuzz` for content; `nikto`/`whatweb`/`wpscan` for candidates; `curl`/`mitmproxy` for manual API work; `sqlmap`/`commix` only after a specific parameter and baseline exist. POST/write/upload/authentication remains confirmation-required.

- [ ] **Step 2: Write content and scanner references**

For every installed tool, document path, observed version, safe command, rate/concurrency flag, output format, false-positive controls, and stop conditions. Examples use `https://authorized.example` and write under `/work/jobs/<job-id>/results/`.

- [ ] **Step 3: Write API, injection, and proxy references**

Document `curl`, `openssl s_client`, `mitmproxy`/`mitmdump`, `sqlmap`, `commix`, `davtest`, and `wpscan`. SQLMap and Commix examples use detection-only levels and forbid data dumping, shell acquisition, or destructive flags. Proxy logs must redact Authorization/Cookie fields.

- [ ] **Step 4: Author the Nuclei Skill**

Pin knowledge to Nuclei `v3.11.1`; require JSONL output, `-rate-limit 10`, concurrency no greater than 25, explicit template selection, and review of template behavior. Headless uses `-headless -system-chrome`. Code templates require ECDSA signing and explicit `-code`; unsigned refusal is treated as expected security behavior.

- [ ] **Step 5: Write Nuclei references**

Cover template update, validation, severity/tag/type filtering, JSONL, resume, Headless/Chromium, ECDSA Code template signing, custom template trust, and mapping each protocol to a second verifier (`curl`, `dig`, `openssl`, `nmap`, or Chromium).

- [ ] **Step 6: Run harmless tool integration checks**

In the inspection container, start local HTTP/TCP services and verify documented invocations for content discovery, HTTP scanning, Nuclei HTTP, Headless with system Chromium, signed Code, TCP, DNS, and SSL. Record exact exit codes and matches in `skill-tests/tool-integration-results.md`.

- [ ] **Step 7: Commit Web/Nuclei Skills**

```sh
git add kali-security-web kali-security-nuclei skill-tests/tool-integration-results.md
git commit -m "feat: add Web and Nuclei security skills"
```

---

### Task 6: Implement validation, evidence, and reporting Skills

**Files:**
- Create: `kali-security-validation/SKILL.md`
- Create: `kali-security-validation/references/finding-gates.md`
- Create: `kali-security-validation/references/reproduction.md`
- Create: `kali-security-evidence/SKILL.md`
- Create: `kali-security-evidence/references/redaction.md`
- Create: `kali-security-evidence/references/artifact-layout.md`
- Create: `kali-security-reporting/SKILL.md`
- Create: `kali-security-reporting/references/report-template.md`
- Create: `kali-security-reporting/references/finding-template.md`

**Interfaces:**
- Consumes: scanner candidates and local export protocol.
- Produces: `PASS`, `KILL`, `DOWNGRADE`, or `CHAIN-REQUIRED` findings and sanitized local deliverables.

- [ ] **Step 1: Author validation guidance**

Implement the approved seven-question gate, unique-marker baseline check, body/length/hash differential, interleaved timing samples (`n >= 10` per group), two-stack reproduction for High/Critical, and stop-after-minimum-impact proof.

- [ ] **Step 2: Add finding and reproduction references**

Define required evidence for each outcome and protocol-specific second-tool pairs. Provide one safe Python standard-library timing sampler that randomizes interleaved control/test requests and reports count, mean, median, and population standard deviation without declaring a vulnerability automatically.

- [ ] **Step 3: Author evidence hygiene guidance**

Require redaction before export. Cover Cookie, Authorization, JWT, API keys, CSRF tokens, passwords, other-user PII, raw HTTP, JSONL, screenshots, HAR, terminal logs, and command files. Preserve request IDs and response shape needed for reproduction.

- [ ] **Step 4: Define artifact layout**

Document every path under `security-results/<engagement-id>/`, including confirmed/candidate/killed/retracted findings, execution manifest, tool versions, commands, logs, evidence, report, and `SHA256SUMS`.

- [ ] **Step 5: Author reporting guidance and templates**

Use the twelve-section report from the spec. A finding template contains title, scope asset, authorization mode, severity rationale, prerequisites, exact sanitized reproduction, observed result, impact, independent reproduction, evidence references, remediation, and limitations.

- [ ] **Step 6: Test redaction fixtures in Docker**

Create synthetic logs containing fake Cookie, Bearer JWT, API key, password, and PII values. Run the documented redaction process and assert none of the fake secrets remain while request IDs and endpoint names remain.

- [ ] **Step 7: Commit quality/delivery Skills**

```sh
git add kali-security-validation kali-security-evidence kali-security-reporting
git commit -m "feat: add security validation and reporting skills"
```

---

### Task 7: Implement the isolated internal-security Skill

**Files:**
- Create: `kali-security-internal/SKILL.md`
- Create: `kali-security-internal/references/smb-ad-tools.md`
- Create: `kali-security-internal/references/credential-auditing.md`
- Create: `kali-security-internal/references/restricted-tools.md`

**Interfaces:**
- Consumes: renewed internal authorization and capability matrix.
- Produces: isolated read-only/lab guidance; it is never auto-loaded by external Skills.

- [ ] **Step 1: Author the second authorization gate**

Require explicit internal CIDRs/hosts, account ownership, lockout policy, allowed protocols, rate, time window, and prohibited actions. External authorization never satisfies this gate.

- [ ] **Step 2: Document SMB/AD read-only tools**

Document safe enumeration/lab usage for `enum4linux`, `smbmap`, selected Impacket discovery clients, and NetExec enumeration. Authentication, spraying, relay, coercion, write actions, and remote execution require separate confirmation or remain forbidden per the spec.

- [ ] **Step 3: Document credential-auditing boundaries**

Document `john`, `hashcat`, `hydra`, `ncrack`, and `patator` as lab/offline or separately confirmed tools. Default guidance uses user-owned sample hashes and local lab services; no real-target spray command is included.

- [ ] **Step 4: Document restricted inventory**

List Responder, Metasploit, PowerShell Empire, PowerSploit, Mimikatz, Evil-WinRM, passing-the-hash, and related tools with installed status, purpose, risk, and policy. Provide only harmless version/help or local-lab examples; omit persistence, lateral movement, credential dumping, evasion, and weaponized commands.

- [ ] **Step 5: Verify isolation contract**

Static checks assert no external Skill references `kali-security-internal` as an automatic step and no restricted reference contains command patterns for credential dumping, payload generation, persistence, relay, or remote shell execution.

- [ ] **Step 6: Commit internal Skill**

```sh
git add kali-security-internal
git commit -m "feat: add gated internal security reference"
```

---

### Task 8: Verify all Skills with GREEN/REFACTOR scenarios

**Files:**
- Create: `skill-tests/skill-results.md`
- Create: `skill-tests/static-validation.py`
- Create: `skill-tests/static-validation-results.txt`
- Modify: affected `kali-security-*/SKILL.md` and references only when a test exposes a gap

**Interfaces:**
- Consumes: all ten Skills and the Task 2 scenarios.
- Produces: behavioral and structural verification evidence.

- [ ] **Step 1: Write the static validator test first**

Before `static-validation.py`, run a documented shell assertion that fails because the validator does not exist. Then create the minimal Python standard-library validator for frontmatter, required files, descriptions, cross-references, fixed image, server-choice ordering, attribution, forbidden scope, and inventory references.

- [ ] **Step 2: Run static validation in Docker**

Upload the project files into a Python container and run:

```sh
python3 skill-tests/static-validation.py | tee skill-tests/static-validation-results.txt
```

Expected: ten Skills found, zero structural failures, zero forbidden command patterns.

- [ ] **Step 3: Rerun all six pressure scenarios with Skills**

Use a fresh agent context per scenario. Include only the Skills that their descriptions should trigger. Save responses and criterion scores in `skill-results.md`.

Expected: every scenario passes every mandatory criterion.

- [ ] **Step 4: Micro-test descriptions**

For each Skill, run at least five fresh-context trigger/no-trigger samples. Confirm relevant prompts load it and unrelated prompts do not. Tighten only descriptions with observed misses or false triggers.

- [ ] **Step 5: Test disconnect recovery against a safe remote fixture**

At test time, call `ssh_list_servers` and ask the user which server to use. After selection, run a harmless background sleep/status fixture in the fixed image, intentionally use a short `ssh_exec` timeout, reconnect, prove the same PID/job continues and was not duplicated, transfer a small archive, verify local SHA-256, then stop the test container.

Expected: one job ID, one PID, verified local archive, container stopped only after verification.

- [ ] **Step 6: Refactor observed loopholes and rerun affected tests**

For each failure, record the agent's exact rationalization, add the smallest rule or positive contract that addresses it, and rerun that scenario until it passes. Do not add unobserved speculative rules.

- [ ] **Step 7: Final repository checks and commit**

Run in Docker where execution is needed and local Git for non-executing inspection:

```sh
python3 skill-tests/static-validation.py
git diff --check
git status --short
```

Expected: validator exit 0, no whitespace errors, only intended files staged.

```sh
git add kali-security-* skill-tests .gitignore
git commit -m "test: verify Kali security skills"
```
