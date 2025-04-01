import os
import sys
import platform
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

# Detect the operating system
OPERATING_SYSTEM = platform.system().lower()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Custom post-install commands
def post_install():
    """Configure platform-specific integration after installation"""
    script_path = os.path.join(sys.prefix, 'bin' if OPERATING_SYSTEM != 'windows' else 'Scripts', 'pmwl')
    
    if OPERATING_SYSTEM == 'linux':
        # Create a desktop file for Linux
        desktop_dir = os.path.expanduser('~/.local/share/applications')
        if not os.path.exists(desktop_dir):
            os.makedirs(desktop_dir)
        
        desktop_file = os.path.join(desktop_dir, 'pmwl.desktop')
        with open(desktop_file, 'w') as f:
            f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Pimp My Wordlist
Comment=Custom wordlist generator for penetration testing
Exec={script_path}
Terminal=true
Categories=Security;Utility;
Keywords=security;wordlist;penetration;testing;
""")
        os.chmod(desktop_file, 0o755)
        print(f"Created desktop entry at {desktop_file}")
    
    elif OPERATING_SYSTEM == 'windows':
        # Create a Windows Start Menu shortcut
        try:
            import winshell
            from win32com.client import Dispatch
            
            start_menu = winshell.start_menu()
            link_filepath = os.path.join(start_menu, 'Programs', 'PMWL.lnk')
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(link_filepath)
            shortcut.Targetpath = script_path
            shortcut.WorkingDirectory = os.path.dirname(script_path)
            shortcut.Description = "Custom wordlist generator for penetration testing"
            shortcut.IconLocation = sys.executable
            shortcut.save()
            print(f"Created Start Menu shortcut at {link_filepath}")
        except ImportError:
            print("For Windows shortcuts, install optional dependencies: pip install pywin32 winshell")
            print(f"Executable installed at: {script_path}")
    
    print(f"Pimp My Wordlist installed successfully! Run with 'pmwl' command.")

# Custom command classes
class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.execute(post_install, [], msg="Running post-installation tasks...")

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        self.execute(post_install, [], msg="Running post-installation tasks...")

class PostEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)

# Define package structure
packages = ['pimp_my_wordlist'] if os.path.isdir('pimp_my_wordlist') else []

# For single file installation
py_modules = ['pimp_my_wordlist'] if os.path.isfile('pimp_my_wordlist.py') else []

# Optional dependencies based on platform
extras_require = {
    'windows': ['pywin32', 'winshell'],
}

setup(
    name="pimp-my-wordlist",
    version="1.0.0",
    author="",
    author_email="",
    description="A custom wordlist generator for professional penetration testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/pimp-my-wordlist",
    project_urls={
        "Bug Tracker": "https://github.com/username/pimp-my-wordlist/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Security",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
    ],
    packages=packages,
    py_modules=py_modules,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'pmwl=pimp_my_wordlist:main',
        ],
    },
    extras_require=extras_require,
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
        'egg_info': PostEggInfoCommand,
    },
)
