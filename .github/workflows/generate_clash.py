import yaml

def parse_list_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    rules = {}
    current_category = None

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            current_category = line  # Заголовок категории
            rules[current_category] = []
        elif line and current_category:
            rules[current_category].append(f"  - {line}")

    return rules

def generate_clash_yaml(rules, output_file='Clash.yaml'):
    payload = []
    for category, domains in rules.items():
        payload.append(category)
        payload.extend(domains)

    content = {'payload': payload}
    with open(output_file, 'w') as f:
        yaml.dump(content, f, default_flow_style=False, allow_unicode=True)

if __name__ == "__main__":
    rules = parse_list_file('list.lst')
    generate_clash_yaml(rules)
