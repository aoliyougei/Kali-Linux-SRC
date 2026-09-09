#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    "kali-security-scope",
    "kali-security-remote",
    "kali-security-inventory",
    "kali-security-recon",
    "kali-security-web",
    "kali-security-nuclei",
    "kali-security-validation",
    "kali-security-evidence",
    "kali-security-reporting",
    "kali-security-internal",
]
REQUIRED = {
    "kali-security-scope": ["references/authorization-template.md", "references/scope-example.json"],
    "kali-security-remote": ["references/job-protocol.md", "references/export-protocol.md", "references/execution-manifest-example.json"],
    "kali-security-inventory": ["references/packages.tsv", "references/executables.tsv", "references/tool-usage-catalog.tsv", "references/security-tools.md", "references/capability-matrix.md"],
    "kali-security-recon": ["references/dns-tools.md", "references/host-discovery.md", "references/port-scanning.md", "references/http-fingerprinting.md", "references/osint-tools.md"],
    "kali-security-web": ["references/content-discovery.md", "references/web-scanners.md", "references/api-testing.md", "references/injection-tools.md", "references/proxy-and-traffic.md"],
    "kali-security-nuclei": ["references/nuclei-cli.md", "references/templates.md", "references/headless.md", "references/code-templates.md"],
    "kali-security-validation": ["references/finding-gates.md", "references/reproduction.md"],
    "kali-security-evidence": ["references/redaction.md", "references/artifact-layout.md"],
    "kali-security-reporting": ["references/report-template.md", "references/finding-template.md"],
    "kali-security-internal": ["references/smb-ad-tools.md", "references/credential-auditing.md", "references/restricted-tools.md"],
}
ATTRIBUTION = "Claude-BugHunter"
FIXED_IMAGE = "docker.io/aoliyougei/kali-linux-nuclei-headless:v3.11.1-2026.3.4"
errors = []

def require(ok, message):
    if not ok:
        errors.append(message)

for name in SKILLS:
    directory = ROOT / name
    skill = directory / "SKILL.md"
    require(skill.is_file(), f"{name}: missing SKILL.md")
    if not skill.is_file():
        continue
    text = skill.read_text()
    parts = text.split("---", 2)
    require(len(parts) == 3, f"{name}: invalid frontmatter delimiters")
    if len(parts) == 3:
        frontmatter = parts[1]
        n = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.M)
        d = re.search(r"^description:\s*(.+)\s*$", frontmatter, re.M)
        require(bool(n and n.group(1) == name), f"{name}: frontmatter name mismatch")
        require(bool(d and d.group(1).startswith("Use when")), f"{name}: description must start with Use when")
        require(len(frontmatter) <= 1024, f"{name}: frontmatter exceeds 1024 chars")
    require(ATTRIBUTION in text and "CC BY 4.0" in text, f"{name}: missing attribution")
    for relative in REQUIRED[name]:
        require((directory / relative).is_file(), f"{name}: missing {relative}")

remote = (ROOT / "kali-security-remote/SKILL.md").read_text()
require(FIXED_IMAGE in remote, "remote: fixed image missing")
require(remote.find("ssh_list_servers") < remote.find("ssh_exec"), "remote: ssh_list_servers must precede ssh_exec")
require("network: host" in remote, "remote: host network missing")
require("禁止 `--rm`" in remote, "remote: --rm prohibition missing")
require("禁止默认 `--privileged`" in remote, "remote: privileged prohibition missing")
require("只有本地校验成功后才停止容器" in remote, "remote: local verification stop gate missing")
require("不重跑、不停止、不删除" in remote, "remote: uncertain-state preservation missing")

result_pattern = "security-results/YYYY-MM-DD_<scheme-host-port|multi-target>_<engagement-id>/"
export = (ROOT / "kali-security-remote/references/export-protocol.md").read_text()
artifacts = (ROOT / "kali-security-evidence/references/artifact-layout.md").read_text()
reporting = (ROOT / "kali-security-reporting/SKILL.md").read_text()
for path, text in [("remote", remote), ("export", export), ("artifacts", artifacts), ("reporting", reporting)]:
    require(result_pattern in text, f"{path}: normalized result directory missing")
for term in ["multi-target", "userinfo", "path", "query", "fragment"]:
    require(term in export and term in artifacts, f"results: missing normalization rule {term}")
require("security-results/<engagement-id>/" not in remote + export + artifacts + reporting, "results: legacy directory format remains")

scope = (ROOT / "kali-security-scope/SKILL.md").read_text()
for term in ["engagement-id", "授权依据", "精确目标", "允许测试类型", "禁止动作", "时间窗口", "blackbox", "greybox"]:
    require(term in scope, f"scope: missing {term}")
for term in ["Bug Bounty 默认值", "项目规则或范围证据", "@", "www", "*", "top-1000", "TCP Connect", "T3", "非破坏性 CVE", "非破坏性配置", "默认 `blackbox`", "登录尝试", "SQL 注入利用", "OOB/Interactsh", "DoS/资源耗尽"]:
    require(term in scope, f"scope: missing Bug Bounty default {term}")
require("只有项目规则明确" in scope, "scope: wildcard/root evidence gate missing")
require("禁止列表优先" in scope, "scope: deny precedence missing")

authorization_template = (ROOT / "kali-security-scope/references/authorization-template.md").read_text()
scope_example = (ROOT / "kali-security-scope/references/scope-example.json").read_text()
for term in ["bug_bounty_scope_evidence", "top-1000", "blackbox"]:
    require(term in authorization_template, f"authorization template: missing {term}")
for term in ["bug_bounty_scope_evidence", '"mode": "blackbox"', '"requests_per_second": 10', '"concurrency": 25']:
    require(term in scope_example, f"scope example: missing {term}")

packages = (ROOT / "kali-security-inventory/references/packages.tsv").read_text().splitlines()
executables = (ROOT / "kali-security-inventory/references/executables.tsv").read_text().splitlines()
tools = (ROOT / "kali-security-inventory/references/security-tools.md").read_text()
catalog = (ROOT / "kali-security-inventory/references/tool-usage-catalog.tsv").read_text().splitlines()
require(len(packages) == 1490, f"inventory: expected 1490 packages, got {len(packages)}")
require(len(catalog) == 194, f"inventory: expected 193 catalog entries, got {len(catalog)-1}")
require(sum(row.split("\t")[2] != "-" for row in catalog[1:]) == 178, "inventory: expected 178 command-bearing catalog entries")
require(len(executables) >= 1682, f"inventory: too few executable rows: {len(executables)}")
require(any(row.startswith("nuclei\t/usr/local/bin/nuclei\t") for row in executables), "inventory: nuclei missing")
for absent in ["naabu", "subfinder", "dnsx", "katana", "dalfox", "gau", "waybackurls", "trufflehog"]:
    require(absent in tools, f"inventory: absent tool not documented: {absent}")
require("not installed" in tools, "inventory: missing not-installed marker")

external_names = [name for name in SKILLS if name != "kali-security-internal"]
for name in external_names:
    text = (ROOT / name / "SKILL.md").read_text()
    require(not re.search(r"自动.{0,30}kali-security-internal|kali-security-internal.{0,30}自动", text), f"{name}: auto-loads internal skill")

restricted = (ROOT / "kali-security-internal/references/restricted-tools.md").read_text().lower()
for pattern in [r"msfvenom\s+-p", r"secretsdump[^`\n]*@", r"ntlmrelayx[^`\n]*-t", r"mimikatz\s+privilege::", r"empire\s+server"]:
    require(not re.search(pattern, restricted), f"internal: forbidden executable pattern: {pattern}")

all_text = "\n".join(p.read_text(errors="replace") for name in SKILLS for p in (ROOT / name).rglob("*.md"))
for placeholder in ["TBD", "TODO", "fill in details", "implement later"]:
    require(placeholder not in all_text, f"skills: placeholder found: {placeholder}")

if errors:
    print(f"FAIL skills={len(SKILLS)} errors={len(errors)}")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print(f"PASS skills={len(SKILLS)} structural_failures=0 forbidden_patterns=0 packages={len(packages)} executable_entries={len(executables)-1}")
