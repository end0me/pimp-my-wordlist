# Pimp My Wordlist (PMWL)

A customizable wordlist generator for professional penetration testing engagements.

![Banner](https://github.com/username/pimp-my-wordlist/raw/main/assets/banner.png)

## Overview

PMWL is a lightweight Python tool designed to generate targeted wordlists for password cracking during authorized penetration testing. By incorporating target-specific information, PMWL creates more effective wordlists than generic alternatives, potentially reducing the time needed to identify weak passwords.

### Features

- **Interactive Interface**: Menu-driven approach for straightforward data collection and configuration
- **Flexible Output Sizing**: Generate wordlists from 500 to 50,000+ entries based on your requirements
- **Customizable Complexity**: Four complexity levels from basic to extreme password variations
- **Pattern Recognition**: Incorporates common password creation patterns observed in real-world scenarios
- **Target-Specific Customization**: Leverages gathered information for more relevant password candidates

## Installation

### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/username/pimp-my-wordlist.git

# Navigate to directory
cd pimp-my-wordlist

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
```

### Windows

1. Download or clone the repository
2. Right-click `install.ps1` and select "Run with PowerShell"
3. Follow the on-screen prompts

Once installed, PMWL can be run from anywhere using the command:

```bash
pmwl
```

## Usage Guide

PMWL provides a straightforward four-option menu:

1. **Enter target information** - Input details like names, birth dates, and other relevant information
2. **Configure wordlist options** - Select size and complexity settings
3. **Generate wordlist** - Create your custom wordlist
4. **View current configuration** - Review current settings and target information

### Typical Workflow

1. Gather information about the target through open-source intelligence
2. Enter the collected information through the interface
3. Select appropriate size and complexity based on your testing requirements
4. Generate the wordlist and use with your preferred password testing tools

## Responsible Usage

This tool is intended exclusively for authorized security testing. Please ensure:

- You have proper written authorization before testing
- You comply with applicable laws and regulations
- You adhere to professional ethical standards
- You handle any discovered credentials with appropriate care

## Contributing

Contributions to this project are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the security community for sharing knowledge and techniques.
- Appreciation to any penetration testers who provide feedback and suggestions.
- Respect to security researchers advancing the field of password security.
