# Tools

## mini-kali

docker image with pre-installed tools for each step in penetration testing
Those are **Strict stdin/stdout CLI Tools** or Non-interactive CLI.
These accept command‑line arguments, run, print results, then exit — exactly what AI agents love:

**Recon**

* `assetfinder`
* `subfinder`
* `whois`
* `dig`
* `nslookup`
* `hping3`
* `dnsrecon`

**Scanning & Enumeration**

* `nmap`
* `masscan`
* `enum4linux-ng`
* `nikto`
* `whatweb`
* `fingerprintx`
* `gobuster`
* `wpscan`

**Vulnerability Mapping & Hypothesis**

* `nuclei`
* `sslscan`

**Exploitation**

* `sqlmap`
* `hydra`
* `medusa`
* `ncrack`
* `exploit_crafting and executing with programming langauages(python, go, perl, ruby)`

**Post‑Exploitation**

* `netcat`
* `socat`
* `ssh -D` (via `openssh-client`)
* `impacket` CLI tools(`psexec, secretsdump`)

**programming-languages**
* `python`
* `go`
* `perl`
* `ruby`

**General Utilities**

* `curl`
* `httpie`
* `trufflehog`

## web-browser

**mcp-playwright** would allow the agent to browse the internet and fetch results

## code-interpreter

**mcp-code-interpreter** would allow the agent to execute python code

## exploits database

**exploitdb-tool** would allow the agent to search and download exploit scripts(https://www.exploit-db.com/)

## support to interactive penetration testing tools (comming soon)
e.g metasploit,...

# Agent workflow

## orchestrator deep-agent

Think of it as the **general commandar** of the agents army.
It holds the high-level mission plan, manages the todo list, and calls out subagents as needed.
langchain DeepAgents gives it tools for planning (write_todos), context offloading (filesystem tools), and delegate work (task() to subagents).

responsible for generating a structured final report (findings, severity, evidences, remediation guidance).

**available tools** (deepagents tools, web-browser)

## recon subagent

Specialized in building the attack surface map. Suitable tasks:

**Passive OSINT gathering** (DNS, certificates, WHOIS).
**Active network scans** (port, service detection).
**Fingerprint tech stacks**
**available tools** (recon tools,General Utilities)

## scan_enum subagent

After the attack surface is known, this agent deepens the view:

**User enumeration**
**API / endpoint probing**
**Version and misconfiguration discovery**
**available tools** (Scanning & Enumeration tools, General Utilities)

## vuln_analysis subagent

This one reads outputs from **scan_enum** and frames attack hypotheses:

**Map services to known vulnerabilities (CVEs, logic flaws)**
**Prioritize by impact, exploitability, and business risk**
**Generate concise evidence summaries**
**available tools** (Vulnerability Mapping & Hypothesis tools, General Utilities)

## exploit subagent

This agent is the proof-of-concept runner:

**Execute controlled exploits**
**Validate impact without causing collateral damage**
**Return proof (e.g., “we got a shell here”) cleanly**
**available tools** (Exploitation tools, sploitus-tool, code-interpreter, General Utilities)

## post_exploit subagent

After exploitation, we want meaning, not chaos:

**Assess blast radius**
**Identify pivot paths**
**identify cracks and passcodes**
**available tools** (Post‑Exploitation, General Utilities)