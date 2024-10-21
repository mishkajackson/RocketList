import os

def parse_list_file(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return {}

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

    print(f"Parsed rules: {rules}")  # Отладочный вывод
    return rules

def generate_clash_yaml(rules, output_file='Clash.yaml'):
    print(f"Generating {output_file}...")
    with open(output_file, 'w') as f:
        f.write("payload:\n")
        for category, domains in rules.items():
            f.write(f"  {category}\n")
            for domain in domains:
                f.write(f"  - {domain}\n")
    print(f"{output_file} generated successfully.")

def generate_shadowrocket_conf(rules, output_file='Shadowrocket.conf'):
    print(f"Generating {output_file}...")
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
            f.write(f"\n{category}\n")
            for domain in domains:
                # Избавляемся от дублирования "DOMAIN-SUFFIX" и других ключевых слов
                clean_domain = domain.replace('DOMAIN-SUFFIX,', '').replace('DOMAIN-KEYWORD,', '')
                f.write(f"DOMAIN-SUFFIX,{clean_domain},PROXY\n")
    print(f"{output_file} generated successfully.")

if __name__ == "__main__":
    print("Parsing list.lst...")
    rules = parse_list_file('list.lst')
    if rules:
        generate_clash_yaml(rules)
        generate_shadowrocket_conf(rules)
    else:
        print("No rules found. Exiting.")
