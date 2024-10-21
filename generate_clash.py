def parse_list_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    rules = {}
    current_category = None

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            current_category = line  # Название категории
            rules[current_category] = []
        elif line and current_category:
            rules[current_category].append(line)  # Сохраняем домен

    return rules

def generate_clash_yaml(rules, output_file='Clash.yaml'):
    with open(output_file, 'w') as f:
        f.write("payload:\n")
        for category, domains in rules.items():
            f.write(f"  {category}\n")
            for domain in domains:
                f.write(f"  - {domain}\n")

def generate_shadowrocket_conf(rules, output_file='Shadowrocket.conf'):
    general_section = """[General]
bypass-system = true
skip-proxy = 127.0.0.1, 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local, captive.apple.com
bypass-tun = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32
dns-server = https://dns.adguard-dns.com/dns-query, 8.8.8.8, 8.8.4.4
fallback-dns-server = system
update-url = https://raw.githubusercontent.com/mishkajackson/Domain_List/refs/heads/main/Shadowrocket.conf

[Rule]
"""
    with open(output_file, 'w') as f:
        f.write(general_section)
        for category, domains in rules.items():
            f.write(f"{category}\n")
            for domain in domains:
                f.write(f"DOMAIN-SUFFIX,{domain},PROXY\n")

if __name__ == "__main__":
    rules = parse_list_file('list.lst')
    generate_clash_yaml(rules)
    generate_shadowrocket_conf(rules)
