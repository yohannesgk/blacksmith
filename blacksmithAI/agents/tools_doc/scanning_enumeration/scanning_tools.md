# Scanning and Enumeration Tools Documentation

This document provides comprehensive technical documentation for scanning and enumeration tools used in cybersecurity assessments. Each tool section includes description, syntax, options, examples, and best practices.

## 1. NMAP

### Description
Nmap (Network Mapper) is one of the most powerful and versatile open-source tools for network exploration, security scanning, and penetration testing. It performs host discovery, service detection, operating system fingerprinting, and vulnerability detection. Nmap uses raw IP packets to determine available hosts, services, operating systems, and network characteristics.

### Basic Syntax

```bash
nmap [Scan Type] [Options] {target}
```

### Available Options

#### Target Specification

| Option | Description |
|--------|-------------|
| `target` | IP address, hostname, CIDR range, or file with targets |
| `-iL inputfile` | Read targets from file |
| `-iR num_hosts` | Pick random targets |
| `--exclude host1,host2` | Exclude hosts from scan |
| `--excludefile exclude_file` | Exclude hosts from file |

#### Host Discovery Options

| Option | Description |
|--------|-------------|
| `-sn` | Ping scan (disable port scan) |
| `-Pn` | Treat all hosts as online (skip host discovery) |
| `-PS` | TCP SYN discovery on port 22 (default) |
| `-PA` | TCP ACK discovery on port 80 (default) |
| `-PU` | UDP discovery on port 40125 |
| `-PY` | SCTP discovery on port 80 |
| `-PE` | ICMP Echo Request discovery |
| `-PP` | ICMP Timestamp discovery |
| `-PM` | ICMP Address Mask discovery |
| `-PR` | ARP discovery (local network) |

#### Port Specification Options

| Option | Description |
|--------|-------------|
| `-p port_range` | Scan specific ports (e.g., `-p 80,443` or `-p 1-1000`) |
| `-p-` | Scan all 65535 ports |
| `-F` | Fast scan (top 100 ports) |
| `-r` | Scan ports in sequential order (no randomization) |
| `--top-ports N` | Scan top N most common ports |

#### Scan Techniques

| Option | Description |
|--------|-------------|
| `-sS` | TCP SYN scan (default, requires root) |
| `-sT` | TCP connect scan (default without root) |
| `-sU` | UDP scan |
| `-sN` | TCP Null scan |
| `-sF` | TCP FIN scan |
| `-sX` | TCP Xmas scan |
| `-sA` | TCP ACK scan |
| `-sW` | TCP Window scan |
| `-sM` | TCP Maimon scan |
| `-sI` | Idle scan (zombie scan) |
| `-sO` | IP protocol scan |
| `-sY` | SCTP INIT scan |

#### Service and Version Detection

| Option | Description |
|--------|-------------|
| `-sV` | Probe open ports to determine service/version info |
| `--version-intensity level` | Set version detection intensity (0-9) |
| `--version-light` | Light mode (lower intensity) |
| `--version-all` | Try all probes (highest intensity) |
| `--version-trace` | Track version scan activity |

#### OS Detection

| Option | Description |
|--------|-------------|
| `-O` | Enable OS detection |
| `--osscan-limit` | Limit OS detection to promising targets |
| `--osscan-guess` | Guess OS more aggressively |

#### Output Options

| Option | Description |
|--------|-------------|
| `-oN file` | Normal output to file |
| `-oX file` | XML output to file |
| `-oG file` | Grepable output to file |
| `-oA basename` | Output in all formats |
| `-v` | Increase verbosity level |
| `-d` | Increase debugging level |
| `--reason` | Show reason for port state |
| `--open` | Show only open ports |

#### Timing and Performance

| Option | Description |
|--------|-------------|
| `-T0` | Paranoid timing (slowest) |
| `-T1` | Sneaky timing |
| `-T2` | Polite timing |
| `-T3` | Normal timing (default) |
| `-T4` | Aggressive timing |
| `-T5` | Insane timing (fastest) |
| `--min-parallelism num` | Minimum parallel probes |
| `--max-parallelism num` | Maximum parallel probes |
| `--min-rtt-timeout time` | Minimum RTT timeout |
| `--max-rtt-timeout time` | Maximum RTT timeout |
| `--initial-rtt-timeout time` | Initial RTT timeout |

#### Script Scanning

| Option | Description |
|--------|-------------|
| `-sC` | Run default script scan |
| `--script=script.nse` | Run specific script |
| `--script=category` | Run scripts by category |
| `--script-args` | Pass arguments to scripts |
| `--script-trace` | Trace script execution |

#### Script Categories

| Category | Description |
|----------|-------------|
| `auth` | Authentication scripts |
| `broadcast` | Discovery scripts |
| `brute` | Brute-force scripts |
| `default` | Default scripts |
| `discovery` | Host discovery scripts |
| `dos` | Denial of service scripts |
| `exploit` | Exploitation scripts |
| `external` | External resource scripts |
| `fuzzer` | Fuzzing scripts |
| `intrusive` | Intrusive scripts |
| `malware` | Malware detection scripts |
| `safe` | Safe scripts |
| `version` | Version detection scripts |
| `vuln` | Vulnerability detection scripts |

### Examples

**Basic host discovery:**
```bash
nmap -sn 192.168.1.0/24
```

**Quick port scan:**
```bash
nmap -F 192.168.1.100
```

**Full port scan with service detection:**
```bash
nmap -p- -sV 192.168.1.100
```

**Operating system detection:**
```bash
nmap -O 192.168.1.100
```

**Vulnerability scanning with scripts:**
```bash
nmap --script=vuln 192.168.1.100
```

**Aggressive scan with all options:**
```bash
nmap -A -T4 192.168.1.100
```

**UDP port scanning:**
```bash
nmap -sU -p 53,67,68,161,162 192.168.1.100
```

**Idle/zombie scan for anonymity:**
```bash
nmap -sI zombie_host:port target_ip
```

**Custom script execution:**
```bash
nmap --script=http-title,http-headers,http-methods target.com
```

### Best Practices

1. Start with host discovery (`-sn`) to identify live hosts before port scanning
2. Use `-T4` for most assessments to balance speed and reliability
3. Combine `-sS` (SYN scan) with `-sV` (version detection) for comprehensive enumeration
4. Use script categories like `vuln` or `safe` based on your assessment goals
5. Save output in multiple formats (`-oA`) for different use cases
6. Use `--reason` to understand why ports are reported in certain states
7. Adjust timing options for different network conditions and evasion needs
8. Always document your scan parameters for reproducibility
9. Use `-Pn` when hosts are not responding to ping probes

---

## 2. MASSCAN

### Description
Masscan is an extremely fast Internet port scanner capable of scanning the entire Internet in under 6 minutes at 10 million packets per second. It uses asynchronous transmission of TCP packets, making it significantly faster than Nmap for large-scale port scanning. It supports custom packet crafting and flexible configuration options.

### Basic Syntax

```bash
masscan [options] [targets]
```

### Available Options

| Option | Description |
|--------|-------------|
| `--ports` | Specify ports to scan (e.g., `1-65535` or `80,443,8000-9000`) |
| `--rate` | Set packets per second (e.g., `--rate 10000`) |
| `--bandwidth` | Set bandwidth in bits per second |
| `-c`, `--conf` | Load configuration from file |
| `--echo` | Print current configuration to stdout |
| `--offline` | Drop root privileges after startup |
| `-p`, `--source-port` | Set source port for packets |
| `--ttl` | Set IP time-to-live |
| `--retries` | Number of retries for failed packets |
| `--nmap` | Show nmap-compatible command line |
| `--nobanner` | Suppress startup banner |
| `--pcap` | Save received packets to PCAP file |
| `--regress` | Run regression test |
| `--ttl` | Set time-to-live for packets |
| `--max-rate` | Maximum packet rate |
| `--minsize` | Minimum packet size |
| `--maxsize` | Maximum packet size |
| `--seed` | Seed for random number generator |
| `-e`, `--adapter` | Use specific network interface |
| `-S`, `--source-ip` | Set source IP address |
| `--adapter-ip` | Set adapter IP address |
| `--adapter-mac` | Set adapter MAC address |
| `--router-mac` | Set router MAC address |
| `--exclude` | IP addresses to exclude |
| `--excludefile` | File with IP addresses to exclude |
| `--open-only` | Show only open ports |
| `--output-format` | Specify output format |
| `--output-filename` | Output file name |

### Output Format Options

| Format | Description |
|--------|-------------|
| `binary` | Binary output (default for PCAP) |
| `xml` | XML output |
| `json` | JSON output |
| `grepable` | Grepable output (compatible with Nmap) |
| `list` | Simple list format |

### Examples

**Basic fast scan:**
```bash
masscan 0.0.0.0/0 --ports 80,443,22 --rate 10000
```

**Scan entire Internet for specific ports:**
```bash
masscan 0.0.0.0/0 -p 80,443,8080 --rate 1000000
```

**Scan specific IP range:**
```bash
masscan 192.168.1.0/24 -p 1-1000 --rate 1000
```

**Save results to JSON:**
```bash
masscan 192.168.1.0/24 -p 1-65535 --output-format json --output-filename results.json
```

**Custom packet rate:**
```bash
masscan target.com --ports 1-65535 --rate 500000
```

**Exclude IP addresses:**
```bash
masscan 10.0.0.0/8 -p 80,443 --exclude 10.0.0.1,10.0.0.2
```

**Exclude from file:**
```bash
masscan 10.0.0.0/8 -p 80,443 --excludefile excluded.txt
```

**Echo current configuration:**
```bash
masscan --echo > masscan.conf
```

**Load configuration from file:**
```bash
masscan -c masscan.conf
```

**Use specific network interface:**
```bash
masscan 192.168.1.0/24 -p 80,443 -e eth0
```

### Best Practices

1. Use appropriate `--rate` values based on network capacity and target tolerance
2. Start with lower rates and increase based on network responsiveness
3. Use `--exclude` or `--excludefile` to avoid scanning critical infrastructure
4. Save configuration with `--echo` for reusable scan profiles
5. Use JSON output for programmatic parsing of results
6. Combine with Nmap for comprehensive scanning (masscan for discovery, nmap for detailed enumeration)
7. Use `--nobanner` for scripting environments

---

## 3. ENUM4LINUX-NG

### Description
enum4linux-ng is a modern fork and improvement of enum4linux, designed for enumerating information from Windows and Samba systems. It performs discovery, user enumeration, share enumeration, group and user listing, password policy extraction, and more. It provides both passive and active reconnaissance capabilities for Windows-based networks.

### Basic Syntax

```bash
enum4linux-ng [options] target
```

### Available Options

| Option | Description |
|--------|-------------|
| `-A` | Enable all simple options (combines -U, -S, -G, -P, -O, -L) |
| `-U` | Get user list |
| `-S` | Get share list |
| `-G` | Get group and member list |
| `-P` | Get password policy information |
| `-O` | Get OS information |
| `-L` | Get LDAP information (if applicable) |
| `-N` | Dump user list without names |
| `-W` | Workgroup name |
| `-u user` | Username to use (default: "") |
| `-p pass` | Password to use (default: "") |
| `-s file` | File with username:password pairs |
| `-k username` | Username for kerberos authentication |
| `-aesKey hex` | AES key for kerberos |
| `--continue` | Continue on authentication failures |
| `--nocolor` | Disable color output |
| `--json` | Output in JSON format |
| `--csv` | Output in CSV format |
| `-d` | Show detailed output |
| `-h` | Show help message |

### Examples

**Basic enumeration with all options:**
```bash
enum4linux-ng -A 192.168.1.100
```

**Get user list:**
```bash
enum4linux-ng -U 192.168.1.100
```

**Get share enumeration:**
```bash
enum4linux-ng -S 192.168.1.100
```

**Get all information with specific credentials:**
```bash
enum4linux-ng -A -u administrator -p password123 192.168.1.100
```

**Get password policy:**
```bash
enum4linux-ng -P 192.168.1.100
```

**Output in JSON format:**
```bash
enum4linux-ng -A 192.168.1.100 --json
```

**Specify workgroup:**
```bash
enum4linux-ng -A -W WORKGROUP 192.168.1.100
```

**Brute force with credentials file:**
```bash
enum4linux-ng -s credentials.txt 192.168.1.100
```

**LDAP enumeration:**
```bash
enum4linux-ng -L -u domain\\user -p password 192.168.1.100
```

### Best Practices

1. Start with `-A` for comprehensive enumeration in one pass
2. Use `-u` and `-p` for authenticated scans when credentials are available
3. Use `--json` or `--csv` for structured output suitable for reporting
4. Combine with Nmap SMB scripts for additional enumeration capabilities
5. Look for RID cycling to discover additional users when user listing fails
6. Check for anonymous access on shares which may reveal sensitive information
7. Document password policy information for password guessing campaigns
8. Use `-d` flag for more verbose output when debugging
9. Test against multiple targets to identify patterns in share permissions

---

## 4. GOBUSTER

### Description
Gobuster is a fast, versatile, and powerful directory/file and DNS busting tool written in Go. It is designed to brute-force URIs (directories and files), DNS subdomains, and virtual host names. Gobuster is significantly faster than similar tools due to Go's concurrency model and is widely used for web application reconnaissance and penetration testing.

### Basic Syntax

```bash
gobuster [mode] [options]
```

### Modes

| Mode | Description |
|------|-------------|
| `dir` | Directory/File brute-force mode |
| `dns` | DNS subdomain brute-force mode |
| `vhost` | Virtual host brute-force mode |
| `fuzz` | Fuzzing mode |
| `gcs` | Google Cloud Storage bucket enumeration |
| `s3` | AWS S3 bucket enumeration |

### Available Options (dir mode)

| Option | Description |
|--------|-------------|
| `-u`, `--url` | Target URL |
| `-w`, `--wordlist` | Path to wordlist file |
| `-c`, `--cookies` | Cookies to use |
| `-H`, `--header` | Custom HTTP header |
| `-x`, `--extensions` | File extensions to search (e.g., `.php,.html`) |
| `-e`, `--expanded` | Expanded mode (print full URLs) |
| `-n`, `--no-status` | Don't print status codes |
| `-k`, `--no-tls-validation` | Skip TLS certificate verification |
| `-r`, `--follow-redirect` | Follow redirects |
| `-t`, `--threads` | Number of concurrent threads |
| `--timeout` | HTTP timeout in seconds |
| `-o`, `--output` | Output file for results |
| `--delay` | Delay between requests |
| `-q`, `--quiet` | Quiet mode (no output) |
| `-v`, `--verbose` | Verbose output |
| `-z` | Don't print progress |

### Available Options (dns mode)

| Option | Description |
|--------|-------------|
| `-d`, `--domain` | Target domain |
| `-w`, `--wordlist` | Path to subdomain wordlist |
| `-t`, `--threads` | Number of concurrent threads |
| `--timeout` | DNS timeout in seconds |
| `-o`, `--output` | Output file |
| `-r`, `--resolver` | Use specific DNS resolver |
| `--wildcard` | Allow wildcard responses |
| `-i`, `--show-ips` | Show IP addresses |

### Available Options (vhost mode)

| Option | Description |
|--------|-------------|
| `-u`, `--url` | Target URL |
| `-w`, `--wordlist` | Path to wordlist |
| `-t`, `--threads` | Number of concurrent threads |
| `-c`, `--cookies` | Cookies to use |
| `-H`, `--header` | Custom HTTP header |
| `--timeout` | HTTP timeout |
| `-o`, `--output` | Output file |
| `-k`, `--no-tls-validation` | Skip TLS verification |

### Examples

**Directory brute-force:**
```bash
gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt
```

**Directory scan with extensions:**
```bash
gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt -x .php,.html,.txt
```

**DNS subdomain enumeration:**
```bash
gobuster dns -d example.com -w /usr/share/wordlists/subdomains.txt
```

**Virtual host discovery:**
```bash
gobuster vhost -u http://example.com -w subdomains.txt
```

**Threaded scan with output:**
```bash
gobuster dir -u http://example.com -w large_wordlist.txt -t 50 -o results.txt
```

**Scan with custom headers:**
```bash
gobuster dir -u http://example.com -w wordlist.txt -H "Authorization: Bearer token"
```

**Scan with cookies:**
```bash
gobuster dir -u http://example.com/admin -w wordlist.txt -c "PHPSESSID=abc123"
```

**Quiet mode with extensions:**
```bash
gobuster dir -u http://example.com -w wordlist.txt -x .php,.bak,.old -q
```

**DNS with IP display:**
```bash
gobuster dns -d example.com -w subdomains.txt -i
```

**Follow redirects:**
```bash
gobuster dir -u http://example.com -w wordlist.txt -r
```

### Best Practices

1. Use appropriate wordlists based on the target technology (common.txt for general, specific wordlists for frameworks)
2. Increase thread count (`-t`) for faster scanning but be mindful of rate limiting
3. Use `-x` to scan for specific file extensions relevant to the technology stack
4. Combine gobuster with other enumeration tools for comprehensive results
5. Save output to file for further analysis and reporting
6. Use `-k` for self-signed certificates to avoid TLS verification errors
7. Use `-c` and `-H` for authenticated scanning when required
8. Use DNS mode to discover subdomains that might not be publicly listed
9. Use vhost mode to identify virtual hosts on shared infrastructure
10. Always respect robots.txt and scope limitations

---

## 5. WPSCAN

### Description
WPScan is a black box WordPress security scanner written in Ruby. It enumerates themes, plugins, users, and detects known vulnerabilities in WordPress installations. It is an essential tool for WordPress security assessments and is regularly updated with new vulnerability data.

### Basic Syntax

```bash
wpscan [options] [targets]
```

### Available Options

| Option | Description |
|--------|-------------|
| `--url` | Target WordPress URL (required) |
| `-t`, `--threads` | Number of threads to use |
| `-e`, `--enumerate` | Enumeration options |
| `--detection-mode` | Detection mode (mixed, passive, aggressive) |
| `--user-agent` | Custom user agent string |
| `-o`, `--output` | Output file for results |
| `--format` | Output format (cli, json, xml) |
| `--api-token` | WPScan API token for vulnerability data |
| `--cache-dir` | Cache directory |
| `--cache-ttl` | Cache time-to-live in seconds |
| `-v`, `--verbose` | Verbose output |
| `-q`, `--quiet` | Quiet mode |
| `-h`, `--help` | Show help |

#### Enumeration Options (`-e`)

| Option | Description |
|--------|-------------|
| `ap` | All plugins |
| `vp` | Vulnerable plugins |
| `p` | Popular plugins only |
| `at` | All themes |
| `vt` | Vulnerable themes |
| `t` | Popular themes only |
| `u` | User IDs range (e.g., `u1-50`) |
| `uo` | User IDs from options (requires auth) |
| `m` | Media IDs range |

#### Plugin/Theme Detection Modes

| Mode | Description |
|------|-------------|
| `passive` | Detection from page content only (slowest) |
| `aggressive` | Detection with additional requests (fastest) |
| `mixed` | Use both methods (default) |

#### Additional Options

| Option | Description |
|--------|-------------|
| `--passwords` | Passwords to use for brute force |
| `--usernames` | Usernames to use for brute force |
| `--random-user-agent` | Use random user agent |
| `--disable-tls-checks` | Disable SSL/TLS verification |
| `--force` | Force scan even if WordPress not detected |
| `--wp-content-dir` | Custom wp-content directory |
| `--wp-plugins-dir` | Custom plugins directory |

### Examples

**Basic scan:**
```bash
wpscan --url http://example.com
```

**Enumerate all plugins:**
```bash
wpscan --url http://example.com --enumerate ap
```

**Enumerate vulnerable plugins only:**
```bash
wpscan --url http://example.com --enumerate vp
```

**Enumerate users:**
```bash
wpscan --url http://example.com --enumerate u
```

**Enumerate vulnerable themes:**
```bash
wpscan --url http://example.com --enumerate vt
```

**Aggressive plugin detection:**
```bash
wpscan --url http://example.com --enumerate ap --detection-mode aggressive
```

**Password brute force:**
```bash
wpscan --url http://example.com --usernames admin --passwords passwords.txt
```

**Complete scan with all enumerations:**
```bash
wpscan --url http://example.com -e ap,vp,at,vt,u
```

**Output to JSON:**
```bash
wpscan --url http://example.com --format json -o results.json
```

**With custom user agent:**
```bash
wpscan --url http://example.com --user-agent "Mozilla/5.0"
```

**Using API token for vulnerability data:**
```bash
wpscan --url http://example.com --api-token YOUR_API_TOKEN
```

### Best Practices

1. Always update WPScan before scans to get latest vulnerability database
2. Use `--enumerate vp` to focus on vulnerable plugins/themes first
3. Use `-e u` to enumerate users, then attempt password guessing
4. Use aggressive mode (`--detection-mode aggressive`) for faster but noisier scans
5. Use API token for accurate vulnerability matching
6. Use `--random-user-agent` for stealthier scanning
7. Focus on recent and popular plugins as they are common attack vectors
8. Combine with manual inspection for comprehensive assessment
9. Test plugins and themes in staging environment before production
10. Document version numbers for accurate vulnerability mapping

---

## 6. FINGERPRINTX

### Description
FingerprintX is a fast and versatile service fingerprinting tool that identifies services running on open ports. It is designed to be faster and more accurate than traditional service detection methods, using protocol-specific probes and response analysis. It supports multiple output formats and can be integrated into larger scanning workflows.

### Basic Syntax

```bash
fingerprintx [options] [targets]
```

### Available Options

| Option | Description |
|--------|-------------|
| `-a`, `--all` | Run all probes |
| `-p`, `--probe` | Specify probe to run |
| `-i`, `--input` | Input file (Nmap XML or JSON) |
| `-o`, `--output` | Output file |
| `-f`, `--format` | Output format (json, text, nmap-xml) |
| `-t`, `--threads` | Number of threads |
| `--timeout` | Connection timeout in milliseconds |
| `-v`, `--verbose` | Verbose output |
| `-q`, `--quiet` | Quiet mode |
| `-h`, `--help` | Show help |

### Probes

| Probe | Description |
|-------|-------------|
| `ftp` | FTP service detection |
| `ssh` | SSH service detection |
| `telnet` | Telnet service detection |
| `smtp` | SMTP service detection |
| `http` | HTTP service detection |
| `https` | HTTPS service detection |
| `mysql` | MySQL service detection |
| `postgres` | PostgreSQL service detection |
| `redis` | Redis service detection |
| `mongodb` | MongoDB service detection |
| `oracle` | Oracle service detection |
| `mssql` | MSSQL service detection |
| `ldap` | LDAP service detection |
| `rdp` | RDP service detection |
| `vnc` | VNC service detection |
| `winrm` | Windows Remote Management |
| `snmp` | SNMP service detection |

### Examples

**Basic fingerprinting:**
```bash
fingerprintx 192.168.1.100:22
```

**Fingerprint multiple ports:**
```bash
fingerprintx 192.168.1.100:21,22,80,443,3306
```

**Scan from file (Nmap XML output):**
```bash
fingerprintx -i nmap_results.xml
```

**Run specific probe:**
```bash
fingerprintx -p http 192.168.1.100:80
```

**All probes with output:**
```bash
fingerprintx -a -o results.json -f json 192.168.1.100
```

**Threaded fingerprinting:**
```bash
fingerprintx -t 10 192.168.1.0/24
```

**Verbose output:**
```bash
fingerprintx -v 192.168.1.100:22
```

### Best Practices

1. Use fingerprintX as a supplement to Nmap's service detection (`-sV`)
2. Use specific probes when you know the expected service type
3. Use `-a` for comprehensive fingerprinting of unknown services
4. Parse JSON output for integration with other tools
5. Use with Nmap XML output for existing scan data enrichment
6. Increase threads for faster scanning of large ranges
7. Adjust timeout for slow or unreliable connections
8. Combine with vulnerability scanners for complete assessment
9. Document fingerprinting results for baseline comparison

---

## General Scanning and Enumeration Best Practices

### 1. Methodology

1. **Start with host discovery** to identify live systems before detailed scanning
2. **Perform port scanning** to identify open services and attack surface
3. **Use service fingerprinting** to identify exact versions and configurations
4. **Enumerate specific services** based on discovered ports
5. **Document all findings** systematically for analysis

### 2. Tool Integration

```bash
# Comprehensive scanning workflow
nmap -sn 192.168.1.0/24 | grep "Nmap scan report" | awk '{print $5}'

# For each discovered host
nmap -sV -sC -p- --script=vuln 192.168.1.100

# Web-focused scanning
gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirb/common.txt

# WordPress-specific
wpscan --url http://192.168.1.100 -e vp,vt,u
```

### 3. Output Management

1. Use standardized formats (JSON, XML) for machine parsing
2. Maintain organized directory structures for scan results
3. Implement data correlation across multiple tools
4. Use version control for scan configurations and scripts
5. Maintain baselines for comparison over time