FROM kalilinux/kali-rolling

# ---- CORE PACKAGES (Layer 1: Largest, Least Likely to Change) ----
RUN apt update && apt install -y \
    python3 python3-pip \
    nmap masscan \
    whois dnsutils dnsrecon \
    hydra medusa ncrack john \
    gobuster wpscan sslscan \
    netcat-traditional socat \
    hping3 openssh-client \
    perl ruby \
    enum4linux-ng samba-common-bin smbclient \
    httpie \
    trufflehog python3-flask python3-impacket \
    && apt autoremove -y \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# ---- GO TOOLCHAIN (Layer 2: Changes Only When Go Version Changes) ----
# Kali already has Go, but we'll use official Go binaries for better control
# ---- GO TOOLCHAIN (Layer 2: Changes Only When Go Version Changes) ----
RUN apt update && apt install -y golang-go
ENV GOBIN=/usr/local/bin
ENV PATH="$GOBIN:$PATH"
RUN go version  # Optional: verify it works

# ---- GO TOOLS (Layer 3: Changes Only When Go Tools Change) ----
RUN go install github.com/tomnomnom/assetfinder@latest \
    && go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest \
    && go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Download Nuclei templates during build
RUN nuclei -update-templates

# ---- PYTHON DEPENDENCIES (Layer 4: Changes When Requirements Change) ----
# Note: Install impacket carefully as Kali has its own version

RUN apt update && apt install -y \
    python3-trufflehog \
    python3-flask \
    python3-impacket \
    && ln -sf /usr/bin/psexec.py /usr/local/bin/psexec 2>/dev/null || true \
    && ln -sf /usr/bin/secretsdump.py /usr/local/bin/secretsdump 2>/dev/null || true

RUN go clean -cache -modcache

# ---- APPLICATION CODE (Layer 5: Changes Most Frequently) ----
WORKDIR /app
COPY server.py server_async.py requirements.txt /app/

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE 9756
CMD ["python3", "server_async.py"]
