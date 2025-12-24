# Reconnaissance Tools Documentation

This document provides comprehensive technical documentation for reconnaissance tools used in cybersecurity assessments. Each tool section includes description, syntax, options, examples, and best practices.

## 1. WHOIS

### Description
Whois is a query and response protocol used to query databases that store registered users or assignees of an Internet resource such as a domain name, an IP address block, or an autonomous system. It is primarily used for gathering information about domain ownership, registration details, name servers, and contact information.

### Basic Syntax
```bash
whois [options] domain_name
```

### Available Options

| Option | Description |
|--------|-------------|
| `-h host`, `--host=host` | Connect to a specific WHOIS server |
| `-p port`, `--port=port` | Specify port number (default: 43) |
| `-H` | Hide legal disclaimers from output |
| `-a`, `--all` | Search all available databases |
| `-i` | Show network addresses (inverse lookup) |
| `-d` | Show delegation record |
| `-T type` | Search for objects of specific type (domain, person, etc.) |

### Examples

**Basic domain lookup:**
```bash
whois example.com
```

**Query specific WHOIS server:**
```bash
whois -h whois.verisign-grs.com example.com
```

**Get domain registration details with parsed output:**
```bash
whois example.com | grep -E "Domain Name|Registrar|Registrant|Name Server"
```

**Query IP address ownership:**
```bash
whois 93.184.216.34
```

### Best Practices

1. Use `-h` to query authoritative WHOIS servers for more accurate data
2. Always verify information from multiple sources as WHOIS data can be protected or outdated
3. Combine with other reconnaissance tools for comprehensive domain intelligence
4. Use grep/awk to parse specific fields from output for automation
5. Respect privacy regulations when handling personal data found in WHOIS records

---

## 2. DNSUTILS (dig/nslookup)

### Description
DNS utilities provide tools for querying Domain Name System servers to obtain domain name or IP address mapping. Two primary tools are available: `dig` (Domain Information Groper) and `nslookup`. Dig is more feature-rich and flexible, while nslookup provides interactive querying capability.

### Basic Syntax (dig)

```bash
dig [@server] [domain] [query-type] [query-class] [+option] [-option]
```

### Basic Syntax (nslookup)

```bash
nslookup [-option] [host] [server]
```

### Available Options (dig)

| Option | Description |
|--------|-------------|
| `@server` | DNS server to query (default from /etc/resolv.conf) |
| `query-type` | Record type (A, AAAA, MX, NS, TXT, SOA, ANY, etc.) |
| `+short` | Short output (just the answer) |
| `+noall` | Remove all default output formatting |
| `+answer` | Show answer section only |
| `+trace` | Trace DNS resolution path |
| `-4` | Force IPv4 query |
| `-6` | Force IPv6 query |
| `-p port` | Use alternative port number |
| `-b address` | Source IP address for query |

### Examples (dig)

**Basic A record query:**
```bash
dig example.com A
```

**Query with short output:**
```bash
dig example.com +short
```

**Get MX records (mail servers):**
```bash
dig example.com MX
```

**Query specific DNS server:**
```bash
dig @8.8.8.8 example.com A
```

**Get all available records:**
```bash
dig example.com ANY +noall +answer
```

**Reverse DNS lookup:**
```bash
dig -x 93.184.216.34 +short
```

**Trace DNS resolution:**
```bash
dig example.com +trace
```

**Batch DNS lookup from file:**
```bash
dig -f domains.txt +short
```

### Available Options (nslookup)

| Option | Description |
|--------|-------------|
| `-type=query_type` | Specify DNS record type |
| `-server=server` | Use specific DNS server |
| `-port=port` | Use alternative port |
| `-timeout=seconds` | Set query timeout |
| `-retry=count` | Set number of retries |

### Examples (nslookup)

**Interactive mode:**
```bash
nslookup
> set type=MX
> example.com
> exit
```

**Single command query:**
```bash
nslookup -type=NS example.com
```

**Query from specific server:**
```bash
nslookup example.com 8.8.8.8
```

### Best Practices

1. Use `dig` for complex queries and scripting due to better output control
2. Query multiple DNS servers to identify inconsistencies or cached responses
3. Use `+trace` to understand DNS resolution chain and identify issues
4. Combine `dig` with grep/awk for parsing specific fields in scripts
5. Use reverse DNS to enumerate hostnames from IP addresses
6. Always check for DNS zone transfers (AXFR) when authorized
7. Be aware of DNSSEC validation when analyzing DNS responses

---

## 3. DNSRECON

### Description
dnsrecon is a powerful DNS enumeration tool written in Python. It provides comprehensive DNS reconnaissance capabilities including standard record enumeration, zone transfer testing, reverse lookup enumeration, domain brute-forcing, and cache snooping. It supports multiple output formats and provides detailed information for security assessments.

### Basic Syntax

```bash
dnsrecon [options]
```

### Available Options

| Option | Description |
|--------|-------------|
| `-d`, `--domain` | Target domain name |
| `-n`, `--name_server` | DNS server to query |
| `-r`, `--range` | IP range for reverse lookups (e.g., 192.168.1.0/24) |
| `-D`, `--dictionary` | Dictionary file for subdomain brute-forcing |
| `-t`, `--type` | Type of enumeration to perform |
| `-a` | Perform AXFR (zone transfer) test |
| `-s` | Perform reverse lookups of all SPF records |
| `-g` | Perform Google enumeration |
| `-w` | Perform deep whois record analysis |
| `--threads` | Number of threads for parallel queries |
| `--timeout` | Query timeout in seconds |
| `-o`, `--output` | Output file (XML, CSV, JSON) |
| `--xml` | Output to XML format |
| `--json` | Output to JSON format |
| `--csv` | Output to CSV format |

### Enumeration Types (-t)

| Type | Description |
|------|-------------|
| `std` | Standard enumeration (SOA, NS, A, AAAA, MX, TXT) |
| `rvl` | Reverse lookups of given IP range |
| `brt` | Brute-force hostnames from dictionary |
| `srv` | SRV record enumeration |
| `axfr` | Test for zone transfers |
| `goo` | Google search enumeration |
| `tld` | TLD expansion enumeration |
| `zonewalk` | Perform DNSSEC zone walking |

### Examples

**Standard enumeration:**
```bash
dnsrecon -d example.com
```

**Zone transfer test:**
```bash
dnsrecon -d example.com -t axfr
```

**Subdomain brute-forcing:**
```bash
dnsrecon -d example.com -D /usr/share/wordlists/subdomains.txt -t brt
```

**Reverse lookup enumeration:**
```bash
dnsrecon -r 192.168.1.0/24 -n 192.168.1.1
```

**Save output to file:**
```bash
dnsrecon -d example.com --xml results.xml
```

**Threaded enumeration with timeout:**
```bash
dnsrecon -d example.com --threads 10 --timeout 5
```

**Combined enumeration with multiple types:**
```bash
dnsrecon -d example.com -a -s -t std --threads 5
```

### Best Practices

1. Always start with standard enumeration (`-t std`) before specialized tests
2. Test for zone transfers first as they provide the most information
3. Use wordlists appropriate to the target organization (company name, products, etc.)
4. Increase thread count for faster results on large domains but be mindful of rate limiting
5. Save results in JSON format for easier parsing in scripts
6. Combine with other reconnaissance tools for comprehensive results
7. Use `-t zonewalk` to enumerate DNSSEC-signed zones

---

## 4. ASSETFINDER

### Description
assetfinder is a subdomain discovery tool that finds domains and subdomains related to a given organization. It queries multiple sources including crt.sh, VirusTotal, Facebook's CertStream, Google BigQuery, and other threat intelligence sources to discover subdomains. It is known for its speed and comprehensive coverage.

### Basic Syntax

```bash
assetfinder [options] domain
```

### Available Options

| Option | Description |
|--------|-------------|
| `--subs-only` | Only show subdomains, not the base domain |
| `--include-meta` | Include meta domains (e.g., github.io) |
| `--include-ips` | Include IP addresses in output |
| `--exclude-sans` | Exclude results with no DNS records |
| `--max-records` | Maximum number of records to query |
| `--timeout` | Timeout for HTTP requests (seconds) |
| `--verbose` | Show verbose output |
| `--json` | Output in JSON format |

### Examples

**Basic subdomain enumeration:**
```bash
assetfinder example.com
```

**Get only subdomains:**
```bash
assetfinder --subs-only example.com
```

**Include IP addresses:**
```bash
assetfinder --include-ips example.com
```

**Output in JSON format:**
```bash
assetfinder --json example.com
```

**Exclude domains without DNS records:**
```bash
assetfinder --exclude-sans example.com
```

**Combine with other tools (amass):**
```bash
assetfinder example.com | amass intel -active -d example.com
```

### Best Practices

1. Use `--subs-only` to filter out the main domain when focusing on subdomains
2. Pipe results to `grep` or other tools for filtering based on patterns
3. Combine with `amass` or `subfinder` for more comprehensive coverage
4. Use `--include-ips` when you need IP addresses for further enumeration
5. Save results to file for integration with other tools
6. Run assetfinder regularly to track changes in target's attack surface
7. Use multiple subdomain enumeration tools for maximum coverage

---

## 5. FINDOMAIN

### Description
findomain is a fast and comprehensive subdomain discovery tool that uses multiple sources including certificate transparency logs (crt.sh), Facebook's CertStream, VirusTotal, SpyOnWeb, BufferOver, and DNS over TCP. It supports both passive and active reconnaissance modes and provides cross-platform support.

### Basic Syntax

```bash
findomain [options]
```

### Available Options

| Option | Description |
|--------|-------------|
| `-t`, `--target` | Target domain name |
| `-o`, `--output` | Output file for results |
| `-p`, `--progress` | Show progress during execution |
| `-q`, `--quiet` | Suppress output to stdout |
| `-u`, `--unique-output` | Output only unique subdomains |
| `-0`, `--only-resolving` | Only output subdomains that resolve |
| `--monitor` | Continuous monitoring mode |
| `--get-ips` | Get IP addresses for discovered subdomains |
| `--thread` | Number of threads to use |
| `--timeout` | Request timeout in seconds |
| `--sources` | Specify which sources to use |
| `--config` | Configuration file path |

### Examples

**Basic subdomain enumeration:**
```bash
findomain -t example.com
```

**Get only resolving subdomains:**
```bash
findomain -t example.com --only-resolving
```

**Save results to file:**
```bash
findomain -t example.com -o results.txt
```

**Get IP addresses for subdomains:**
```bash
findomain -t example.com --get-ips
```

**Use specific sources:**
```bash
findomain -t example.com --sources crt.sh,virustotal,sponweb
```

**Monitor for new subdomains:**
```bash
findomain -t example.com --monitor
```

### Best Practices

1. Use `--only-resolving` (`-0`) to filter out non-functional subdomains
2. Combine `--get-ips` with subdomains for immediate reconnaissance data
3. Use `--monitor` for continuous monitoring of target domains
4. Customize sources based on your assessment goals and time constraints
5. Save results in structured format for integration with other tools
6. Use `--unique-output` to remove duplicates from results
7. Increase thread count for faster results on large targets
8. Use in combination with other subdomain enumeration tools for completeness

---

## 6. SUBFINDER

### Description
subfinder is a subdomain discovery tool designed to enumerate valid subdomains for websites using passive online sources. It uses a highly optimized parallel asynchronous approach and supports numerous sources including crt.sh, DNSdumpster, Shodan, and many others. It is part of the Project Discovery toolkit and integrates well with other security tools.

### Basic Syntax

<citations>
[1]
</citations>

```bash
subfinder [flags] [options]
```

### Available Options

| Option | Description |
|--------|-------------|
| `-d`, `--domain` | Target domain name |
| `-dL`, `--domain-list` | File containing list of domains |
| `-o`, `--output` | Output file path |
| `-oJ`, `--json` | Output in JSON format |
| `-oD`, `--csv` | Output in CSV format |
| `-nW` | Remove wildcards from output |
| `-all` | Use all available sources |
| `-r` | Use resolvers for validation |
| `-rL`, `--resolver-list` | File containing DNS resolvers |
| `--timeout` | Timeout in seconds |
| `--max-timeout` | Maximum timeout for retries |
| `--threads` | Number of concurrent threads |
| `--retry` | Number of retry attempts |
| `-v`, `--verbose` | Enable verbose output |
| `-silent` | Show only subdomains in output |
| `--only-active` | Only return subdomains that are active |
| `-t`, `--tools` | Specify which tools to use as sources |

### Examples

**Basic subdomain enumeration:**
```bash
subfinder -d example.com
```

**Multiple domains from file:**
```bash
subfinder -dL domains.txt
```

**Save results to JSON:**
```bash
subfinder -d example.com -oJ results.json
```

**Use all sources with verbose output:**
```bash
subfinder -d example.com -all -v
```

**Filter wildcards and inactive subdomains:**
```bash
subfinder -d example.com -nW --only-active
```

**Use custom resolvers:**
```bash
subfinder -d example.com -rL resolvers.txt
```

**Combine with passive sources only:**
```bash
subfinder -d example.com -sources crt.sh,dnsdumpster,shodan
```

### Best Practices

1. Use `-nW` to remove wildcard subdomains which can clutter results
2. Use `--only-active` to filter subdomains to only those currently responding
3. Maintain and update your resolver list (`-rL`) for accurate validation
4. Use `-oJ` for programmatic parsing of results in scripts
5. Combine with other tools like `assetfinder` and `findomain` for comprehensive coverage
6. Use the `-dL` option for batch processing multiple domains
7. Regularly update subfinder to get new data sources
8. Use `-silent` for cleaner output in pipelines
9. Configure default sources in config file for faster execution

---

## General Reconnaissance Best Practices

### 1. Methodology

1. **Start with passive reconnaissance** using WHOIS, DNS queries, and subdomain enumeration tools
2. **Document all findings** in a structured format for analysis
3. **Cross-reference data** from multiple sources for accuracy
4. **Identify scope boundaries** based on gathered information
5. **Proceed to active reconnaissance** after proper authorization

### 2. Tool Integration

```bash
# Comprehensive subdomain enumeration pipeline
assetfinder --subs-only example.com | \
    findomain -t example.com --only-resolving | \
    subfinder -d example.com -silent | \
    sort -u > all_subdomains.txt
```

### 3. Output Management

1. Use standardized output formats (JSON, CSV) for machine parsing
2. Maintain timestamped logs of all reconnaissance activities
3. Store results in organized directory structures
4. Implement data deduplication across tool outputs
5. Use version control for reconnaissance scripts and results
