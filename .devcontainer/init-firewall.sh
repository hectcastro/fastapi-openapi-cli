#!/bin/bash
set -e

echo "🔥 Initializing firewall..."

# Save Docker DNS nameserver before flushing rules
DOCKER_DNS=$(grep nameserver /etc/resolv.conf | head -n1 | awk '{print $2}')
echo "📋 Docker DNS: $DOCKER_DNS"

# Flush existing rules
echo "🧹 Flushing existing rules..."
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Destroy and recreate ipset for allowed domains
ipset destroy allowed-domains 2>/dev/null || true
ipset create allowed-domains hash:ip

# Function to resolve domain and add to ipset
add_domain() {
    local domain=$1
    echo "  🌐 Resolving $domain..."
    local ips=$(dig +short "$domain" @$DOCKER_DNS | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$')
    if [ -z "$ips" ]; then
        echo "    ⚠️  Warning: Could not resolve $domain"
        return
    fi
    for ip in $ips; do
        echo "    ✓ Adding $ip ($domain)"
        ipset add allowed-domains "$ip" 2>/dev/null || true
    done
}

# Function to add CIDR range to ipset
add_cidr() {
    local cidr=$1
    echo "  📦 Adding CIDR range: $cidr"
    ipset add allowed-domains "$cidr" 2>/dev/null || true
}

echo "📝 Building allowlist..."

# Add Docker DNS
if [ -n "$DOCKER_DNS" ]; then
    echo "  🐳 Adding Docker DNS: $DOCKER_DNS"
    ipset add allowed-domains "$DOCKER_DNS"
fi

# Fetch and add GitHub IP ranges
echo "  🐙 Fetching GitHub IP ranges..."
GITHUB_IPS=$(curl -s https://api.github.com/meta | jq -r '.git[]' 2>/dev/null || echo "")
if [ -n "$GITHUB_IPS" ]; then
    for cidr in $GITHUB_IPS; do
        add_cidr "$cidr"
    done
else
    echo "    ⚠️  Warning: Could not fetch GitHub IPs, adding fallback domains"
    add_domain "github.com"
    add_domain "api.github.com"
fi

echo "  🤖 Adding Anthropic API domains..."
add_domain "api.anthropic.com"
add_domain "claude.ai"

echo "  🔧 Adding VSCode and development tool domains..."
add_domain "marketplace.visualstudio.com"
add_domain "vscode-sync.trafficmanager.net"
add_domain "update.code.visualstudio.com"
add_domain "vscode.download.prss.microsoft.com"
add_domain "main.vscode-cdn.net"

echo "  📦 Adding VSCode extension gallery API domains..."
add_domain "anthropic.gallery.vsassets.io"
add_domain "ms-python.gallery.vsassets.io"
add_domain "charliermarsh.gallery.vsassets.io"
add_domain "astral-sh.gallery.vsassets.io"
add_domain "tamasfe.gallery.vsassets.io"

echo "  📦 Adding VSCode extension CDN domains..."
add_domain "anthropic.gallerycdn.vsassets.io"
add_domain "ms-python.gallerycdn.vsassets.io"
add_domain "charliermarsh.gallerycdn.vsassets.io"
add_domain "astral-sh.gallerycdn.vsassets.io"
add_domain "tamasfe.gallerycdn.vsassets.io"

echo "  🐍 Adding Python package index..."
add_domain "pypi.org"
add_domain "files.pythonhosted.org"

echo "  🌍 Adding additional development resources..."
add_domain "astral.sh"
add_domain "github.com"
add_domain "raw.githubusercontent.com"

# Detect host network
HOST_NETWORK=$(ip route | grep default | awk '{print $3}' | cut -d'.' -f1-3).0/24
echo "  🏠 Host network detected: $HOST_NETWORK"
ipset add allowed-domains "$HOST_NETWORK" 2>/dev/null || true

echo "🛡️  Setting up iptables rules..."

# Set default policies to DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow localhost traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow DNS queries to Docker DNS
iptables -A OUTPUT -p udp -d $DOCKER_DNS --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp -d $DOCKER_DNS --dport 53 -j ACCEPT

# Allow SSH (if needed)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Allow outbound traffic to allowed domains
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT

# Reject everything else with ICMP response for faster feedback
iptables -A OUTPUT -j REJECT --reject-with icmp-host-prohibited

echo "✅ Firewall configured successfully!"

# Verify firewall is working
echo "🧪 Testing firewall..."

# Test that we can reach GitHub API (should succeed)
if curl -s --max-time 5 https://api.github.com > /dev/null 2>&1; then
    echo "  ✓ GitHub API accessible"
else
    echo "  ❌ ERROR: Cannot reach GitHub API (this should work)"
    echo "  ⚠️  Firewall verification failed!"
fi

# Test that we cannot reach example.com (should fail)
if curl -s --max-time 5 https://example.com > /dev/null 2>&1; then
    echo "  ❌ ERROR: example.com is accessible (should be blocked)"
    echo "  ⚠️  Firewall verification failed!"
else
    echo "  ✓ example.com blocked (as expected)"
fi

echo "🎉 Firewall initialization complete!"
echo ""
echo "ℹ️  You can now run Claude Code with --dangerously-skip-permissions"
echo "   The firewall restricts network access to approved destinations only."
