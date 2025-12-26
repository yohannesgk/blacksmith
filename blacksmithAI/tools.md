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

## web-browser [comming_soon]

**mcp-playwright** would allow the agent to browse the internet and fetch results

## code-interpreter [comming_soon]

**mcp-code-interpreter** would allow the agent to execute python code

## exploits database [comming_soon]

**exploitdb-tool** would allow the agent to search and download exploit scripts(e.g. https://www.exploit-db.com/)
