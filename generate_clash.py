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
            rules[current_category].append(line)  # Сохраняем домен без лишних символов

    return rules

def generate_clash_yaml(rules, output_file='Clash.yaml'):
    with open(output_file, 'w') as f:
        f.write("payload:\n")
        for category, domains in rules.items():
            f.write(f"  {category}\n")  # Пишем название категории с отступом
            for domain in domains:
                f.write(f"  - {domain}\n")  # Записываем домены с правильным отступом

if __name__ == "__main__":
    rules = parse_list_file('list.lst')
    generate_clash_yaml(rules)
