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
    "kali-security-validation": ["references/finding-gates.md", "references/reproduction.md", "references/non-reportable-findings.md", "references/platform-acceptance.md"],
    "kali-security-evidence": ["references/redaction.md", "references/artifact-layout.md"],
    "kali-security-reporting": ["references/report-template.md", "references/finding-template.md", "references/hardening-template.md"],
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
for term in ["用户只需提供", "目标域名或 URL", "自动生成", "UTC 日期", "用户最终确认时间", "任务完成或用户停止", "-02", "一次结构化确认", "不再逐项询问"]:
    require(term in scope, f"scope: missing minimal intake rule {term}")
require("缺一项就停止" not in scope, "scope: legacy ask-every-field gate remains")

authorization_template = (ROOT / "kali-security-scope/references/authorization-template.md").read_text()
scope_example = (ROOT / "kali-security-scope/references/scope-example.json").read_text()
for term in ["bug_bounty_scope_evidence", "top-1000", "blackbox", "auto-generated", "until-complete-or-user-stop"]:
    require(term in authorization_template, f"authorization template: missing {term}")
for term in ["bug_bounty_scope_evidence", '"mode": "blackbox"', '"requests_per_second": 10', '"concurrency": 25', '"generated_automatically": true', '"end": "until-complete-or-user-stop"']:
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

validation = (ROOT / "kali-security-validation/SKILL.md").read_text()
finding_gates = (ROOT / "kali-security-validation/references/finding-gates.md").read_text()
non_reportable_path = ROOT / "kali-security-validation/references/non-reportable-findings.md"
platform_path = ROOT / "kali-security-validation/references/platform-acceptance.md"
non_reportable = non_reportable_path.read_text() if non_reportable_path.exists() else ""
platform = platform_path.read_text() if platform_path.exists() else ""
for term in ["技术事实", "平台接受性", "实际安全影响", "KILL", "HARDENING", "内容欺骗", "Secure", "HSTS", ".htaccess", "web.config", "TLS 1.0/1.1", "Source Map", "新影响证据", "不得重复提交"]:
    require(term in validation + finding_gates + non_reportable + platform, f"validation: missing non-reportable rule {term}")
for term in ["认证 Cookie", "会话", "有效凭据", "密钥", "私钥", "HTML", "脚本执行", "合规"]:
    require(term in non_reportable, f"validation: missing impact exception {term}")
for term in ["soft-404", "状态码", "公开数据", "GraphQL introspection", "Open Redirect", "Clickjacking", "CORS", "DNS-only", "限流", "Self-XSS"]:
    require(term in non_reportable, f"validation: missing broader non-reportable class {term}")
for term in ["补天", "review-reason-mismatch", "审核理由", "不重报"]:
    require(term in platform, f"validation: missing platform acceptance rule {term}")
require("平台接受性" in finding_gates and finding_gates.find("平台接受性") < finding_gates.find("严重性"), "validation: acceptance must precede severity")

artifact_layout = (ROOT / "kali-security-evidence/references/artifact-layout.md").read_text()
report_template = (ROOT / "kali-security-reporting/references/report-template.md").read_text()
finding_template = (ROOT / "kali-security-reporting/references/finding-template.md").read_text()
hardening_path = ROOT / "kali-security-reporting/references/hardening-template.md"
hardening_template = hardening_path.read_text() if hardening_path.exists() else ""
web_scanners = (ROOT / "kali-security-web/references/web-scanners.md").read_text()
nuclei_skill = (ROOT / "kali-security-nuclei/SKILL.md").read_text()
require("hardening/" in artifact_layout, "evidence: hardening directory missing")
require("加固项" in report_template, "reporting: hardening section missing")
require("Platform Acceptance" in finding_template and finding_template.find("Platform Acceptance") < finding_template.find("Severity"), "reporting: finding acceptance must precede severity")
for term in ["Outcome: KILL", "Disposition: HARDENING", "不得重复提交", "新影响证据"]:
    require(term in hardening_template, f"reporting: hardening template missing {term}")
for text, name in [(web_scanners, "web scanners"), (nuclei_skill, "nuclei")]:
    require("技术事实" in text and "实际安全影响" in text, f"{name}: fact-impact distinction missing")

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
