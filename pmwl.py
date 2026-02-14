#!/usr/bin/env python3
# pmwl - Pimp My Wordlist - Custom wordlist generator

import os
import subprocess
from dataclasses import dataclass, field
from itertools import product
from datetime import datetime

# Complexity levels as integers for efficient comparison
COMPLEXITY_LOW = 1
COMPLEXITY_MEDIUM = 2
COMPLEXITY_HIGH = 3
COMPLEXITY_EXTREME = 4

COMPLEXITY_MAP = {
    'low': COMPLEXITY_LOW,
    'medium': COMPLEXITY_MEDIUM,
    'high': COMPLEXITY_HIGH,
    'extreme': COMPLEXITY_EXTREME,
}

SIZE_DEFAULTS = {
    'small': 500,
    'medium': 2000,
    'large': 10000,
    'massive': 50000,
}

LEET_MAP = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1'],
    'o': ['0'],
    's': ['$'],
    't': ['7'],
}

SPECIAL_CHARS = ['!', '@', '#', '$']
SEPARATORS = ['.', '_', '-']
COMMON_SUFFIXES = ['123', '1234', '12345', '!', '!!', '@', '#']


@dataclass
class Config:
    """Wordlist generation configuration."""
    size: str = 'medium'
    complexity: str = 'medium'
    output_file: str = 'wordlist.txt'
    custom_size: int = 0

    @property
    def target_size(self):
        if self.size == 'custom':
            return self.custom_size
        return SIZE_DEFAULTS[self.size]

    @property
    def complexity_level(self):
        return COMPLEXITY_MAP[self.complexity]


@dataclass
class TargetInfo:
    """Target-specific information for wordlist generation."""
    first_name: str = ''
    middle_name: str = ''
    last_name: str = ''
    birth_year: str = ''
    spouse_name: str = ''
    pet_names: list = field(default_factory=list)
    children_names: list = field(default_factory=list)
    important_dates: list = field(default_factory=list)
    hobbies_teams: list = field(default_factory=list)

    def has_info(self):
        """Check if any target information has been provided."""
        return any(
            (isinstance(v, str) and v) or (isinstance(v, list) and v)
            for v in [self.first_name, self.middle_name, self.last_name,
                      self.birth_year, self.spouse_name, self.pet_names,
                      self.children_names, self.important_dates,
                      self.hobbies_teams]
        )


def display_banner():
    """Display the ASCII art banner for the application"""
    banner = """
 ██▓███   ██▓ ███▄ ▄███▓ ██▓███      ███▄ ▄███▓▓██   ██▓    █     █░ ▒█████   ██▀███  ▓█████▄  ██▓     ██▓  ██████ ▄▄▄█████▓
▓██░  ██▒▓██▒▓██▒▀█▀ ██▒▓██░  ██▒   ▓██▒▀█▀ ██▒ ▒██  ██▒   ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒▒██▀ ██▌▓██▒    ▓██▒▒██    ▒ ▓  ██▒ ▓▒
▓██░ ██▓▒▒██▒▓██    ▓██░▓██░ ██▓▒   ▓██    ▓██░  ▒██ ██░   ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒░██   █▌▒██░    ▒██▒░ ▓██▄   ▒ ▓██░ ▒░
▒██▄█▓▒ ▒░██░▒██    ▒██ ▒██▄█▓▒ ▒   ▒██    ▒██   ░ ▐██▓░   ░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ░▓█▄   ▌▒██░    ░██░  ▒   ██▒░ ▓██▓ ░
▒██▒ ░  ░░██░▒██▒   ░██▒▒██▒ ░  ░   ▒██▒   ░██▒  ░ ██▒▓░   ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒░▒████▓ ░██████▒░██░▒██████▒▒  ▒██▒ ░
▒▓▒░ ░  ░░▓  ░ ▒░   ░  ░▒▓▒░ ░  ░   ░ ▒░   ░  ░   ██▒▒▒    ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒▓  ▒ ░ ▒░▓  ░░▓  ▒ ▒▓▒ ▒ ░  ▒ ░░
░▒ ░      ▒ ░░  ░      ░░▒ ░        ░  ░      ░ ▓██ ░▒░      ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ▒  ▒ ░ ░ ▒  ░ ▒ ░░ ░▒  ░ ░    ░
░░        ▒ ░░      ░   ░░          ░      ░    ▒ ▒ ░░       ░   ░  ░ ░ ░ ▒    ░░   ░  ░ ░  ░   ░ ░    ▒ ░░  ░  ░    ░
          ░         ░                       ░    ░ ░           ░        ░ ░     ░        ░        ░  ░ ░        ░
                                                 ░ ░                                     ░
                                              [Wordlist Generator]
    """
    print(banner)


def clear_screen():
    """Clear the terminal screen for better readability"""
    if os.name == 'nt':
        subprocess.run('cls', shell=True, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    else:
        subprocess.run(['clear'], stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


def main():
    target = TargetInfo()
    config = Config()

    clear_screen()
    display_banner()
    input("\nPress Enter to start...")

    while True:
        clear_screen()
        display_banner()
        print("\n===== PIMP MY WORDLIST =====")
        print("1. Enter target information")
        print("2. Configure wordlist options")
        print("3. Generate wordlist")
        print("4. View current configuration")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        actions = {
            '1': lambda: collect_target_info(target),
            '2': lambda: configure_wordlist(config),
            '3': lambda: generate_wordlist(target, config),
            '4': lambda: view_configuration(target, config),
        }

        if choice in actions:
            actions[choice]()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            input("Invalid choice. Press Enter to continue...")


def collect_target_info(target):
    """Gather target-specific information for wordlist generation"""
    clear_screen()
    print("\n===== TARGET INFORMATION =====")

    print("\nEnter information (leave blank to skip):")
    target.first_name = input("First Name: ")
    target.middle_name = input("Middle Name: ")
    target.last_name = input("Last Name: ")

    while True:
        birth_year = input("Birth Year (YYYY): ")
        if birth_year == '':
            break
        if (birth_year.isdigit() and len(birth_year) == 4
                and 1900 <= int(birth_year) <= datetime.now().year):
            target.birth_year = birth_year
            break
        print("Please enter a valid 4-digit year.")

    target.spouse_name = input("Spouse Name: ")

    target.pet_names = collect_list_items("Pet Names")
    target.children_names = collect_list_items("Children Names")
    target.hobbies_teams = collect_list_items("Hobbies/Sports Teams")

    clear_screen()
    print("\n===== IMPORTANT DATES =====")
    print("Examples: Wedding anniversary (MM-DD), Graduation (YYYY-MM-DD)")

    dates = []
    while True:
        date_description = input("\nDate Description (or press Enter to finish): ")
        if date_description == '':
            break
        date_value = input("Date (YYYY-MM-DD or MM-DD): ")
        if date_value:
            dates.append(f"{date_description}: {date_value}")

    target.important_dates = dates

    input("\nTarget information updated. Press Enter to continue...")


def collect_list_items(item_type):
    """Collect multiple related items from user input"""
    clear_screen()
    print(f"\n===== {item_type.upper()} =====")

    items = []
    print(f"Enter {item_type.lower()} one at a time (press Enter when done):")

    while True:
        item = input(f"Enter {item_type.lower()} item: ")
        if item == '':
            break
        items.append(item)

    return items


def configure_wordlist(config):
    """Configure wordlist parameters including size and complexity"""
    clear_screen()
    print("\n===== WORDLIST CONFIGURATION =====")

    # Size configuration
    print("\n--- WORDLIST SIZE ---")
    print("1. Small (approximately 500 words)")
    print("2. Medium (approximately 2000 words)")
    print("3. Large (approximately 10000 words)")
    print("4. Massive (approximately 50000 words)")
    print("5. Custom size")

    size_choice = input("\nSelect size option (1-5): ")
    size_map = {'1': 'small', '2': 'medium', '3': 'large', '4': 'massive'}

    if size_choice in size_map:
        config.size = size_map[size_choice]
    elif size_choice == '5':
        try:
            custom_size = int(input("Enter custom wordlist size: "))
            if custom_size > 0:
                config.custom_size = custom_size
                config.size = 'custom'
            else:
                print("Size must be greater than 0. Keeping current size.")
        except ValueError:
            print("Invalid number. Keeping current size.")
    else:
        print("Invalid choice. Keeping current size.")

    # Complexity configuration
    clear_screen()
    print("\n--- WORDLIST COMPLEXITY ---")
    print("1. Low (simple variations like capitalization and basic substitutions)")
    print("2. Medium (more variations, common patterns, and simple combinations)")
    print("3. High (extensive variations, complex patterns, special characters)")
    print("4. Extreme (all of the above plus extensive combinations and permutations)")

    complexity_choice = input("\nSelect complexity option (1-4): ")
    complexity_map = {'1': 'low', '2': 'medium', '3': 'high', '4': 'extreme'}
    config.complexity = complexity_map.get(complexity_choice, config.complexity)

    # Output file
    clear_screen()
    print("\n--- OUTPUT FILE ---")
    print(f"Current output file: {config.output_file}")

    if input("Change output file? (y/n): ").lower() == 'y':
        new_file = input("Enter new filename: ")
        if new_file:
            if not new_file.endswith('.txt'):
                new_file += '.txt'
            config.output_file = new_file

    input("\nWordlist configuration updated. Press Enter to continue...")


# --- Wordlist generation helpers ---


def apply_leet_variants(word, complexity_level):
    """Generate leet-speak variants with combinatorial substitutions."""
    variants = set()

    # Find positions in the word that have leet replacements
    positions = []
    for i, ch in enumerate(word):
        lower_ch = ch.lower()
        if lower_ch in LEET_MAP:
            options = [ch]  # original character is always an option
            if complexity_level >= COMPLEXITY_HIGH:
                options.extend(LEET_MAP[lower_ch])
            else:
                options.append(LEET_MAP[lower_ch][0])
            positions.append((i, options))

    if not positions:
        return variants

    # Extreme: combinatorial substitutions (all combinations)
    # Other levels: individual substitutions only
    if complexity_level >= COMPLEXITY_EXTREME and len(positions) <= 6:
        indices = [p[0] for p in positions]
        option_lists = [p[1] for p in positions]
        for combo in product(*option_lists):
            chars = list(word)
            for idx, replacement in zip(indices, combo):
                chars[idx] = replacement
            result = ''.join(chars)
            if result != word:
                variants.add(result)
    else:
        for i, options in positions:
            for replacement in options[1:]:  # skip the original char
                chars = list(word)
                chars[i] = replacement
                variants.add(''.join(chars))

    return variants


def extract_date_numbers(important_dates):
    """Extract numeric portions from date entries."""
    date_numbers = []
    for entry in important_dates:
        parts = entry.split(': ', 1)
        if len(parts) > 1:
            nums = ''.join(c for c in parts[1] if c.isdigit())
            if nums:
                date_numbers.append(nums)
    return date_numbers


def generate_wordlist(target, config):
    """Generate customized wordlist based on target information"""
    clear_screen()
    print("\n===== PIMPING YOUR WORDLIST =====")

    if not target.has_info():
        print("No target information provided.")
        input("Please add target information before generating a wordlist. "
              "Press Enter to continue...")
        return

    print("Processing target information...")

    level = config.complexity_level
    birth_year = target.birth_year
    birth_year_short = birth_year[2:] if birth_year else ''

    # Build base words from target info
    base_words = []
    string_fields = [target.first_name, target.middle_name,
                     target.last_name, target.spouse_name]
    for val in string_fields:
        if val:
            base_words.append(val.lower())

    if birth_year:
        base_words.append(birth_year)
        base_words.append(birth_year_short)

    for field_list in [target.pet_names, target.children_names,
                       target.hobbies_teams]:
        for item in field_list:
            if item:
                base_words.append(item.lower())

    date_numbers = extract_date_numbers(target.important_dates)

    print("Generating password variations...")

    wordlist = set()

    for word in base_words:
        if not word:
            continue

        cap = word.capitalize()

        # Base word and case variants (all levels)
        wordlist.add(word)
        wordlist.add(cap)
        wordlist.add(word.upper())

        # Leet-speak variants
        wordlist.update(apply_leet_variants(word, level))

        # Suffix and prefix digits 0-9
        for i in range(10):
            wordlist.add(f"{word}{i}")
            wordlist.add(f"{cap}{i}")
            wordlist.add(f"{i}{word}")

        # Birth year suffixes
        if birth_year:
            wordlist.add(f"{word}{birth_year}")
            wordlist.add(f"{word}{birth_year_short}")
            wordlist.add(f"{cap}{birth_year}")
            wordlist.add(f"{cap}{birth_year_short}")

        # Medium+ complexity
        if level >= COMPLEXITY_MEDIUM:
            for suffix in COMMON_SUFFIXES:
                wordlist.add(f"{word}{suffix}")
                wordlist.add(f"{cap}{suffix}")

            for num in date_numbers:
                wordlist.add(f"{word}{num}")
                wordlist.add(f"{cap}{num}")

        # High+ complexity
        if level >= COMPLEXITY_HIGH:
            for char in SPECIAL_CHARS:
                wordlist.add(f"{word}{char}")
                wordlist.add(f"{cap}{char}")
                wordlist.add(f"{char}{word}")
                wordlist.add(f"{char}{cap}")

            if birth_year:
                for char in SPECIAL_CHARS:
                    wordlist.add(f"{word}{birth_year}{char}")
                    wordlist.add(f"{cap}{birth_year}{char}")

        # Extreme complexity
        if level >= COMPLEXITY_EXTREME:
            reversed_word = word[::-1]
            rev_cap = reversed_word.capitalize()
            wordlist.add(reversed_word)
            wordlist.add(rev_cap)
            for i in range(10):
                wordlist.add(f"{reversed_word}{i}")

    # Name combinations (medium+)
    if level >= COMPLEXITY_MEDIUM:
        name_parts = [n.lower() for n in [target.first_name,
                      target.middle_name, target.last_name] if n]

        # All ordered pairs of name parts
        for i, a in enumerate(name_parts):
            for j, b in enumerate(name_parts):
                if i != j:
                    combined = f"{a}{b}"
                    wordlist.add(combined)
                    wordlist.add(combined.capitalize())
                    # CamelCase
                    wordlist.add(f"{a.capitalize()}{b.capitalize()}")
                    # Separator combinations
                    for sep in SEPARATORS:
                        wordlist.add(f"{a}{sep}{b}")

                    if birth_year:
                        wordlist.add(f"{combined}{birth_year}")
                        wordlist.add(f"{combined}{birth_year_short}")

        # First name + pet/children/spouse combinations
        if target.first_name:
            fn = target.first_name.lower()
            combo_names = (
                [p.lower() for p in target.pet_names if p]
                + [c.lower() for c in target.children_names if c]
                + ([target.spouse_name.lower()] if target.spouse_name else [])
            )
            for name in combo_names:
                wordlist.add(f"{fn}{name}")
                wordlist.add(f"{name}{fn}")
                wordlist.add(f"{fn.capitalize()}{name.capitalize()}")
                for sep in SEPARATORS:
                    wordlist.add(f"{fn}{sep}{name}")

    # Extreme: reversed name combos
    if level >= COMPLEXITY_EXTREME and target.first_name and target.last_name:
        fn = target.first_name.lower()
        ln = target.last_name.lower()
        wordlist.add(f"{fn}{ln[::-1]}")
        wordlist.add(f"{ln}{fn[::-1]}")

    # Sort first, then truncate (fixes non-deterministic output bug)
    target_size = config.target_size
    total_unique = len(wordlist)
    wordlist_sorted = sorted(wordlist)

    if len(wordlist_sorted) > target_size:
        wordlist_sorted = wordlist_sorted[:target_size]

    # Bulk write
    with open(config.output_file, 'w') as f:
        f.write('\n'.join(wordlist_sorted) + '\n')

    generated_count = len(wordlist_sorted)
    print(f"\nWordlist generated with {generated_count} entries.")
    if total_unique > target_size:
        print(f"({total_unique} unique words generated; "
              f"capped to {target_size} by size setting.)")
    elif total_unique < target_size:
        print(f"(Only {total_unique} unique words could be generated "
              f"from the provided information.)")
        print("Tip: Add more target details or increase complexity "
              "for a larger wordlist.")
    print(f"Saved to: {os.path.abspath(config.output_file)}")
    input("Press Enter to continue...")


def view_configuration(target, config):
    """Display current configuration and target information"""
    clear_screen()
    print("\n===== CURRENT CONFIGURATION =====")

    print("\n--- TARGET INFORMATION ---")
    fields = [
        ('First Name', target.first_name),
        ('Middle Name', target.middle_name),
        ('Last Name', target.last_name),
        ('Birth Year', target.birth_year),
        ('Spouse Name', target.spouse_name),
        ('Pet Names', target.pet_names),
        ('Children Names', target.children_names),
        ('Important Dates', target.important_dates),
        ('Hobbies Teams', target.hobbies_teams),
    ]
    for label, value in fields:
        if isinstance(value, list):
            print(f"{label}: {', '.join(value) if value else 'None'}")
        else:
            print(f"{label}: {value if value else ''}")

    print("\n--- WORDLIST CONFIGURATION ---")
    print(f"Size: {config.size.title()} ({config.target_size} words)")
    print(f"Complexity: {config.complexity.title()}")
    print(f"Output file: {config.output_file}")

    input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
