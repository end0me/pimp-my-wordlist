#!/usr/bin/env python3
# pmwl - Pimp My Wordlist - Custom wordlist generator

import os
from datetime import datetime

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
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Initialize target information dictionary
    target_info = {
        'first_name': '',
        'middle_name': '',
        'last_name': '',
        'birth_year': '',
        'pet_names': [],
        'spouse_name': '',
        'children_names': [],
        'important_dates': [],
        'hobbies_teams': []
    }
    
    # Configure default wordlist parameters
    wordlist_size = 'medium'
    wordlist_complexity = 'medium'
    output_file = 'wordlist.txt'
    
    # Define wordlist size options 
    size_options = {
        'small': 500,
        'medium': 2000,
        'large': 10000,
        'massive': 50000,
        'custom': 0
    }
    
    # Display banner at startup
    clear_screen()
    display_banner()
    input("\nPress Enter to start...")
    
    # Main program loop
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
        
        if choice == '1':
            target_info = collect_target_info(target_info)
        elif choice == '2':
            wordlist_size, wordlist_complexity, output_file = configure_wordlist(size_options, wordlist_size, wordlist_complexity, output_file)
        elif choice == '3':
            generate_wordlist(target_info, wordlist_size, wordlist_complexity, size_options, output_file)
        elif choice == '4':
            view_configuration(target_info, wordlist_size, wordlist_complexity, size_options, output_file)
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            input("Invalid choice. Press Enter to continue...")


def collect_target_info(target_info):
    """Gather target-specific information for wordlist generation"""
    clear_screen()
    print("\n===== TARGET INFORMATION =====")
    
    # Collect single value fields
    print("\nEnter information (leave blank to skip):")
    target_info['first_name'] = input("First Name: ")
    target_info['middle_name'] = input("Middle Name: ")
    target_info['last_name'] = input("Last Name: ")
    
    # Birth year with validation
    while True:
        birth_year = input("Birth Year (YYYY): ")
        if birth_year == '':
            break
        if birth_year.isdigit() and len(birth_year) == 4 and 1900 <= int(birth_year) <= datetime.now().year:
            target_info['birth_year'] = birth_year
            break
        else:
            print("Please enter a valid 4-digit year.")
    
    target_info['spouse_name'] = input("Spouse Name: ")
    
    # Collect multi-value fields
    target_info['pet_names'] = collect_list_items("Pet Names")
    target_info['children_names'] = collect_list_items("Children Names")
    target_info['hobbies_teams'] = collect_list_items("Hobbies/Sports Teams")
    
    # Collect important dates
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
    
    target_info['important_dates'] = dates
    
    input("\nTarget information updated. Press Enter to continue...")
    return target_info


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


def configure_wordlist(size_options, current_size, current_complexity, current_file):
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
    
    if size_choice == '1':
        selected_size = 'small'
    elif size_choice == '2':
        selected_size = 'medium'
    elif size_choice == '3':
        selected_size = 'large'
    elif size_choice == '4':
        selected_size = 'massive'
    elif size_choice == '5':
        try:
            custom_size = int(input("Enter custom wordlist size: "))
            if custom_size > 0:
                size_options['custom'] = custom_size
                selected_size = 'custom'
            else:
                print("Size must be greater than 0.")
                selected_size = current_size
        except ValueError:
            print("Invalid number. Keeping current size.")
            selected_size = current_size
    else:
        print("Invalid choice. Keeping current size.")
        selected_size = current_size
    
    # Complexity configuration
    clear_screen()
    print("\n--- WORDLIST COMPLEXITY ---")
    print("1. Low (simple variations like capitalization and basic substitutions)")
    print("2. Medium (more variations, common patterns, and simple combinations)")
    print("3. High (extensive variations, complex patterns, special characters)")
    print("4. Extreme (all of the above plus extensive combinations and permutations)")
    
    complexity_choice = input("\nSelect complexity option (1-4): ")
    
    if complexity_choice == '1':
        selected_complexity = 'low'
    elif complexity_choice == '2':
        selected_complexity = 'medium'
    elif complexity_choice == '3':
        selected_complexity = 'high'
    elif complexity_choice == '4':
        selected_complexity = 'extreme'
    else:
        print("Invalid choice. Keeping current complexity.")
        selected_complexity = current_complexity
    
    # Output file
    clear_screen()
    print("\n--- OUTPUT FILE ---")
    print(f"Current output file: {current_file}")
    
    change = input("Change output file? (y/n): ").lower()
    if change == 'y':
        new_file = input("Enter new filename: ")
        if new_file:
            output_file = new_file
            # Add .txt extension if not present
            if not output_file.endswith('.txt'):
                output_file += '.txt'
        else:
            output_file = current_file
    else:
        output_file = current_file
    
    input("\nWordlist configuration updated. Press Enter to continue...")
    return selected_size, selected_complexity, output_file


def generate_wordlist(target_info, size, complexity, size_options, output_file):
    """Generate customized wordlist based on target information"""
    clear_screen()
    print("\n===== PIMPING YOUR WORDLIST =====")
    
    # Verify target information exists
    has_info = False
    for key, value in target_info.items():
        if isinstance(value, str) and value:
            has_info = True
            break
        elif isinstance(value, list) and value:
            has_info = True
            break
    
    if not has_info:
        print("No target information provided.")
        input("Please add target information before generating a wordlist. Press Enter to continue...")
        return
    
    print("Processing target information...")
    
    # Generate base words from target information
    base_words = []
    
    # Add individual items
    for key, value in target_info.items():
        if isinstance(value, str) and value:
            if key == 'birth_year':
                base_words.append(value)
                # Add last two digits of year
                base_words.append(value[2:])
            else:
                base_words.append(value.lower())
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item:
                    base_words.append(item.lower())
    
    # Extract dates from important dates
    date_numbers = []
    for date_entry in target_info['important_dates']:
        parts = date_entry.split(': ')
        if len(parts) > 1:
            date_part = parts[1]
            # Extract numbers from dates
            nums = []
            for char in date_part:
                if char.isdigit():
                    nums.append(char)
            if nums:
                date_numbers.append(''.join(nums))
    
    print("Generating password variations...")
    
    # Create empty set for wordlist (using set to avoid duplicates)
    wordlist = set()
    
    # Apply transformations based on complexity
    for word in base_words:
        if not word:  # Skip empty strings
            continue
            
        # Add the base word
        wordlist.add(word)
        
        # Basic transformations (all complexity levels)
        wordlist.add(word.capitalize())
        wordlist.add(word.upper())
        
        # Number substitutions
        if 'a' in word:
            wordlist.add(word.replace('a', '4'))
        if 'e' in word:
            wordlist.add(word.replace('e', '3'))
        if 'i' in word:
            wordlist.add(word.replace('i', '1'))
        if 'o' in word:
            wordlist.add(word.replace('o', '0'))
        
        # Add numbers (1-9) to the end
        for i in range(1, 10):
            wordlist.add(f"{word}{i}")
        
        # Add birth year to words if available
        if target_info['birth_year']:
            wordlist.add(f"{word}{target_info['birth_year']}")
            wordlist.add(f"{word}{target_info['birth_year'][2:]}")
        
        # Medium and high complexity
        if complexity in ['medium', 'high']:
            # Add common number patterns
            wordlist.add(f"{word}123")
            wordlist.add(f"{word}12345")
            
            # Add date numbers to words
            for num in date_numbers:
                if num:
                    wordlist.add(f"{word}{num}")
        
        # High complexity only
        if complexity == 'high':
            # Add special characters
            for char in ['!', '@', '#', '$']:
                wordlist.add(f"{word}{char}")
                wordlist.add(f"{word.capitalize()}{char}")
            
            # More complex substitutions
            if 'a' in word:
                wordlist.add(word.replace('a', '@'))
            if 's' in word:
                wordlist.add(word.replace('s', '$'))
            
            # Combinations with birth year and special chars
            if target_info['birth_year']:
                wordlist.add(f"{word}{target_info['birth_year']}!")
                wordlist.add(f"{word.capitalize()}{target_info['birth_year']}$")
    
    # Create simple combinations (first+last name, etc.)
    if complexity in ['medium', 'high']:
        if target_info['first_name'] and target_info['last_name']:
            combined = f"{target_info['first_name'].lower()}{target_info['last_name'].lower()}"
            wordlist.add(combined)
            wordlist.add(combined.capitalize())
            
            # With birth year
            if target_info['birth_year']:
                wordlist.add(f"{combined}{target_info['birth_year']}")
                wordlist.add(f"{combined}{target_info['birth_year'][2:]}")
        
        # First name + pet name
        if target_info['first_name'] and target_info['pet_names']:
            for pet in target_info['pet_names']:
                if pet:
                    combined = f"{target_info['first_name'].lower()}{pet.lower()}"
                    wordlist.add(combined)
    
    # Determine the final size of the wordlist
    target_size = size_options[size]
    wordlist_list = list(wordlist)
    
    # Limit wordlist size if needed
    if len(wordlist_list) > target_size:
        wordlist_list = wordlist_list[:target_size]
    
    # Sort the wordlist
    wordlist_list.sort()
    
    # Save to file
    with open(output_file, 'w') as f:
        for word in wordlist_list:
            f.write(f"{word}\n")
    
    print(f"\nWordlist successfully generated with {len(wordlist_list)} entries.")
    print(f"Saved to: {os.path.abspath(output_file)}")
    input("Press Enter to continue...")


def view_configuration(target_info, size, complexity, size_options, output_file):
    """Display current configuration and target information"""
    clear_screen()
    print("\n===== CURRENT CONFIGURATION =====")
    
    print("\n--- TARGET INFORMATION ---")
    for key, value in target_info.items():
        if isinstance(value, str):
            print(f"{key.replace('_', ' ').title()}: {value}")
        elif isinstance(value, list):
            if value:
                print(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
            else:
                print(f"{key.replace('_', ' ').title()}: None")
    
    print("\n--- WORDLIST CONFIGURATION ---")
    print(f"Size: {size.title()} ({size_options[size]} words)")
    print(f"Complexity: {complexity.title()}")
    print(f"Output file: {output_file}")
    
    input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
