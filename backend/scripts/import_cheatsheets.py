"""
Import the Linux commands cheat sheet from phoenixnap.com/kb/linux-commands-cheat-sheet
into the app's cheat sheet library.

One CheatSheet row per category (topic="commands"). Existing sheets are preserved.
Content fixes applied: "prgrep" typo -> "pgrep".
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.db.session import SessionLocal  # noqa: E402
from app.models.curriculum import CheatSheet  # noqa: E402

SOURCE = "phoenixNAP — Linux Commands Cheat Sheet (phoenixnap.com/kb/linux-commands-cheat-sheet)"

def e(cmd, what, safety=None, distro="All"):
    return {
        "cmd": cmd,
        "syntax": cmd,
        "what": what,
        "opts": [],
        "example": cmd,
        "output": "",
        "mistake": "",
        "safety": safety or "Safe.",
        "distro": distro,
    }

CATEGORIES = [
    ("pnap-hardware", "Hardware Information",
     "Inspect CPU, disk, memory, and connected devices.", [
        e("lscpu", "See CPU information."),
        e("lsblk", "See information about block devices."),
        e("lspci -tv", "Show PCI devices (graphics card, network card) in a tree-like diagram."),
        e("lsusb -tv", "Display USB devices in a tree-like diagram."),
        e("lshw", "List hardware configuration information."),
        e("cat /proc/cpuinfo", "Show detailed CPU information."),
        e("cat /proc/meminfo", "View detailed system memory information."),
        e("cat /proc/mounts", "See mounted file systems."),
        e("free -h", "Display free and used memory."),
        e("sudo dmidecode", "Show hardware information from the BIOS.", "Needs sudo."),
        e("hdparm -i /dev/[device_name]", "Display disk data information."),
        e("hdparm -tT /dev/[device_name]", "Conduct a read speed test on the device/disk."),
        e("badblocks -s /dev/[device_name]", "Test for unreadable blocks on the device/disk.", "Read-only test but slow on large disks."),
        e("fsck /dev/[device_name]", "Run a disk check on an unmounted disk or partition.", "Never run on a mounted filesystem."),
    ]),
    ("pnap-searching", "Searching",
     "Find files, directories, and text anywhere on the system.", [
        e("find [path] -name [search_pattern]", "Find files and directories matching the specified pattern in a location."),
        e("find [path] -size +100M", "See files and directories larger than the specified size."),
        e("grep [search_pattern] [file_name]", "Search for a specific pattern in a file."),
        e("grep -r [search_pattern] [directory_name]", "Recursively search for a pattern in a directory."),
        e("locate [name]", "Locate all files and directories related to a particular name."),
        e("which [command]", "Search the command path in the $PATH environment variable."),
        e("whereis [command]", "Find the source, binary, and manual page for a command."),
        e("awk '/[search_pattern]/ {print $0}' [file_name]", "Print all lines matching a pattern in a file."),
        e("sed 's/[old_text]/[new_text]/' [file_name]", "Find and replace text in a specified file."),
    ]),
    ("pnap-files", "File Commands",
     "Create, delete, move, and inspect files from the terminal.", [
        e("mkdir [directory_name]", "Create a new directory."),
        e("rm [file_name]", "Remove a file.", "Permanently deletes the file."),
        e("rm -r [directory_name]", "Remove a directory recursively.", "Destructive — deletes directory and everything inside."),
        e("rm -rf [directory_name]", "Recursively remove a directory without confirmation.", "DANGEROUS: no confirmation, irreversible."),
        e("cp [source_file] [destination_file]", "Copy the contents of one file to another."),
        e("cp -r [source_directory] [destination_directory]", "Recursively copy a directory."),
        e("mv [source_file] [destination_file]", "Move or rename files or directories."),
        e("ln -s [path]/[file_name] [link_name]", "Create a symbolic link to a file."),
        e("touch [file_name]", "Create a new (empty) file."),
        e("cat [file_name]", "Show the contents of a file."),
        e("cat [source_file] >> [destination_file]", "Append file contents to another file."),
        e("head [file_name]", "Show the first ten lines of a file."),
        e("tail [file_name]", "Show the last ten lines of a file."),
        e("more [file_name]", "Display contents of a file page by page."),
        e("less [file_name]", "Show the contents of a file with navigation."),
        e("nano [file_name]", "Open or create a file in the nano text editor."),
        e("vi [file_name]", "Open or create a file in the Vi/Vim text editor."),
        e("gpg -c [file_name]", "Encrypt a file.", "Ask for a passphrase; keep it safe."),
        e("gpg [file_name].gpg", "Decrypt an encrypted .gpg file."),
        e("wc -w [file_name]", "Show the number of words, lines and bytes in a file."),
        e("ls | xargs wc -l", "Count lines in each file of a directory."),
        e("cut -d [delimiter] [file_name]", "Cut a section of a file and print it to standard output."),
        e("[data] | cut -d [delimiter]", "Cut a section of piped data and print it."),
        e("shred -u [file_name]", "Overwrite a file to prevent recovery, then delete it.", "Destructive: file cannot be recovered."),
        e("diff [first_file] [second_file]", "Compare two files and display differences."),
        e("source [file_name]", "Read and execute the file content in the current shell."),
        e("[command] | tee [file_name] >/dev/null", "Store the command output in a file, skip terminal output."),
    ]),
    ("pnap-navigation", "Directory Navigation",
     "Move around the filesystem quickly.", [
        e("ls", "List files and directories in the current directory."),
        e("ls -a", "List all files incl. hidden files."),
        e("ls -l", "List files and directories in long format."),
        e("pwd", "Show the current working directory."),
        e("cd ~", "Change directory to $HOME."),
        e("cd ..", "Move up one directory level."),
        e("cd -", "Change to the previous directory."),
        e("cd [directory_path]", "Change to a specified directory."),
        e("dirs", "Show the current directory stack."),
    ]),
    ("pnap-compression", "File Compression",
     "Archive and compress data.", [
        e("tar cf [archive.tar] [file/directory]", "Archive an existing file or directory."),
        e("tar xf [archive.tar]", "Extract an archived file."),
        e("tar czf [archive.tar.gz] [file/directory]", "Create a .gz-compressed tar archive."),
        e("gzip [file_name]", "Compress a .gz file. Use gunzip to decompress."),
        e("bzip2 [file_name]", "Compress a .bz2 file. Use bunzip2 to decompress."),
    ]),
    ("pnap-transfer", "File Transfer",
     "Move files between machines and download from servers.", [
        e("scp [source_file] [user]@[remote_host]:[destination_path]", "Copy a file to a server directory securely.", "Requires SSH access."),
        e("rsync -a [source_dir] [user]@[remote_host]:[destination_dir]", "Synchronize a directory with a backup directory."),
        e("wget [link]", "Download files from FTP or web servers."),
        e("curl -O [link]", "Transfer data to/from a server; -O saves with the remote filename."),
        e("ftp [remote_host]", "Interactive file transfer over FTP.", "Not encrypted — prefer sftp."),
        e("sftp [user]@[remote_host]", "Securely transfer files between local and remote hosts."),
    ]),
    ("pnap-users", "Users and Groups",
     "Manage accounts, groups, sudo, and logins.", [
        e("id", "See details about the active user."),
        e("last", "Show the last system logins."),
        e("who", "Display who is currently logged in."),
        e("w", "Show logged-in users and their activity."),
        e("finger [user_name]", "Show user information."),
        e("sudo useradd [user_name]", "Create a new user account.", "Needs sudo."),
        e("sudo adduser [user_name]", "Create a user through the interactive adduser interface.", "Needs sudo."),
        e("sudo userdel [user_name]", "Delete a user account.", "Removing a user is hard to undo."),
        e("sudo usermod -aG [group_name] [user_name]", "Modify a user (e.g. add to a group).", "Needs sudo."),
        e("passwd", "Change your own password. Use sudo passwd [user] for others.", "Needs sudo for other users."),
        e("sudo groupadd [group_name]", "Add a new group.", "Needs sudo."),
        e("sudo groupdel [group_name]", "Delete a group.", "Needs sudo."),
        e("sudo groupmod -n [new_name] [old_name]", "Rename a group.", "Needs sudo."),
        e("sudo [command]", "Temporarily elevate privileges to root.", "Use with care — system-wide changes."),
        e("su - [user_name]", "Switch the user account or become superuser."),
        e("chgrp [group_name] [file/directory]", "Change the group of a file or directory."),
    ]),
    ("pnap-packages-debian", "Packages · Debian/Ubuntu (apt, dpkg)",
     "Package management on Debian and Ubuntu-based distributions.", [
        e("sudo apt install [package_name]", "Install an APT package.", "Needs sudo.", "Debian/Ubuntu"),
        e("sudo apt-get install [package_name]", "Install a package with the classic apt-get utility.", "Needs sudo.", "Debian/Ubuntu"),
        e("apt search [keyword]", "Search for a package in APT repositories.", None, "Debian/Ubuntu"),
        e("apt list", "List packages installed with APT.", None, "Debian/Ubuntu"),
        e("apt show [package_name]", "Show information about a package.", None, "Debian/Ubuntu"),
        e("sudo dpkg -i [package_name.deb]", "Install a .deb package with the Debian package manager.", "Needs sudo.", "Debian/Ubuntu"),
        e("sudo dpkg -l", "List packages installed with dpkg.", None, "Debian/Ubuntu"),
    ]),
    ("pnap-packages-rhel", "Packages · Red Hat (yum, dnf, rpm)",
     "Package management on RHEL, CentOS and Fedora.", [
        e("sudo yum install [package_name]", "Install a package with the YUM package manager.", "Needs sudo.", "RHEL/CentOS"),
        e("yum search [keyword]", "Find a package in YUM repositories.", None, "RHEL/CentOS"),
        e("yum list installed", "List all packages installed with YUM.", None, "RHEL/CentOS"),
        e("yum info [package_name]", "Show package information.", None, "RHEL/CentOS"),
        e("sudo dnf install [package_name]", "Install a package with DNF (successor of yum).", "Needs sudo.", "Fedora/RHEL 8+"),
        e("sudo rpm -i [package_name.rpm]", "Install a .rpm package from a local file.", "Needs sudo.", "RHEL/CentOS"),
    ]),
    ("pnap-packages-universal", "Packages · Universal (snap, flatpak)",
     "Distribution-independent package formats.", [
        e("sudo snap install [package_name]", "Install a Snap package.", "Needs sudo.", "Universal"),
        e("sudo snap find [keyword]", "Search for a package in the Snap store.", None, "Universal"),
        e("sudo snap list", "List installed Snap packages.", None, "Universal"),
        e("flatpak install [package_name]", "Install a Flatpak package.", None, "Universal"),
        e("flatpak search [keyword]", "Search Flatpak repositories.", None, "Universal"),
        e("flatpak list", "List installed Flatpak packages.", None, "Universal"),
    ]),
    ("pnap-processes", "Processes",
     "View, inspect, and terminate processes and jobs.", [
        e("ps", "List active processes of the current terminal."),
        e("pstree", "Show processes in a tree-like diagram."),
        e("pmap", "Display a memory usage map of a process."),
        e("top", "See all running processes interactively."),
        e("htop", "Interactive color process viewer (if installed)."),
        e("kill [process_id]", "Terminate a process by PID.", "Use SIGTERM (default) before SIGKILL."),
        e("pkill [process_name]", "Terminate a process by name."),
        e("killall [label]", "Terminate all processes with a given label.", "Matches all processes with that name."),
        e("pgrep [keyword]", "List processes matching a keyword."),
        e("pidof [process_name]", "Show the PID of a process."),
        e("bg", "List and resume stopped jobs in the background."),
        e("fg", "Bring the most recently suspended job to the foreground."),
        e("fg [job]", "Bring a particular job to the foreground."),
        e("lsof", "List files opened by running processes."),
        e("trap '[commands]' [signal]", "Catch a system error signal in a Bash script."),
        e("wait", "Pause the terminal or script until a running process completes."),
        e("nohup [command] &", "Run a command in the background after logout."),
    ]),
    ("pnap-system", "System Management & Information",
     "Kernel, uptime, users, time, and shutdown control.", [
        e("uname -r", "Show the kernel release information."),
        e("uname -a", "Show full system information."),
        e("uptime", "Display uptime and load average."),
        e("hostname", "View the system hostname."),
        e("hostname -i", "Show the IP address of the system."),
        e("last reboot", "List system reboot history."),
        e("date", "See the current time and date."),
        e("timedatectl", "Query and change the system clock.", "Needs sudo to change."),
        e("cal", "Show the current calendar."),
        e("whoami", "See which user you are."),
        e("ulimit [flags] [limit]", "View or limit system resource amounts."),
        e("shutdown [hh:mm]", "Schedule a system shutdown.", "Destructive: stops the system at the scheduled time."),
        e("shutdown now", "Shut down the system immediately.", "DESTRUCTIVE: system goes down instantly."),
        e("modprobe [module_name]", "Add a new kernel module.", "Needs sudo."),
        e("dmesg", "Show bootup and kernel messages."),
    ]),
    ("pnap-disk-usage", "Disk Usage",
     "Check space, partitions, and mounted filesystems.", [
        e("df -h", "Check free and used space on mounted filesystems."),
        e("df -i", "Show free inodes on mounted filesystems."),
        e("fdisk -l", "Display disk partitions, sizes and types.", "Needs sudo."),
        e("du -ah", "See disk usage for all files and directories."),
        e("du -sh", "Show total disk usage of the current directory."),
        e("mount", "Show currently mounted file systems."),
        e("findmnt", "Display the target mount point for all filesystems."),
        e("mount [device_path] [mount_point]", "Mount a device.", "Needs sudo."),
    ]),
    ("pnap-ssh", "SSH & Remote Access",
     "Connect to and transfer files with remote hosts.", [
        e("ssh [user]@[remote_host]", "Connect to a remote host as a user via SSH."),
        e("ssh [host]", "Securely connect to a host on the default port 22."),
        e("ssh -p [port] [user]@[remote_host]", "Connect using a specific port."),
        e("ssh-keygen", "Generate an SSH key pair."),
        e("sudo service sshd start", "Start the SSH server daemon.", "Needs sudo."),
        e("scp [file_name] [user]@[remote_host]:[remote_path]", "Securely copy files between systems via SSH."),
        e("sftp [user]@[remote_host]", "Interactive encrypted file transfer over SSH."),
        e("telnet [host]", "Connect via Telnet on port 23.", "Not encrypted — avoid on untrusted networks."),
    ]),
    ("pnap-permissions", "File Permissions",
     "Control who can read, write, and execute files.", [
        e("chmod 777 [file_name]", "Give read+write+execute to everyone (rwxrwxrwx).", "Rarely justified — too permissive."),
        e("chmod 755 [file_name]", "Owner: rwx; group and others: r-x (typical for scripts/dirs)."),
        e("chmod 766 [file_name]", "Owner: rwx; group and others: rw-."),
        e("chown [user_name] [file_name]", "Change file ownership.", "Needs sudo for other's files."),
        e("chown [user]:[group] [file_name]", "Change the owner and group of a file.", "Needs sudo for other's files."),
    ]),
    ("pnap-network", "Networking",
     "Interfaces, connectivity, ports, and DNS.", [
        e("ip addr show", "List IP addresses and network interfaces."),
        e("ip address add [IP_address] dev eth0", "Assign an IP address to interface eth0.", "Needs sudo."),
        e("ifconfig", "Display IP addresses of all network interfaces (legacy)."),
        e("ping [remote_host]", "Ping a remote host to test connectivity."),
        e("netstat -pnltu", "See active listening ports and their programs."),
        e("netstat -tuln", "Show TCP and UDP listening ports."),
        e("whois [domain_name]", "Display registration information about a domain."),
        e("dig [domain_name]", "Show DNS information about a domain."),
        e("dig -x [IP_address]", "Do a reverse DNS lookup of an IP address."),
        e("host [domain_name]", "Perform an IP lookup for a domain."),
        e("hostname -I", "Show the local IP address."),
        e("nslookup [domain_name]", "Receive information about an internet domain."),
    ]),
    ("pnap-variables", "Shell Variables",
     "Create, export, and inspect shell/environment variables.", [
        e("let 'x=[value]'", "Assign an integer value to a variable (Bash arithmetic)."),
        e("export [variable_name]", "Export a shell variable to the environment of child processes."),
        e("declare [variable]=[value]", "Declare a variable with a value (Bash)."),
        e("set", "List all shell variables and functions."),
        e("unset [variable_name]", "Remove a variable."),
        e("echo $[variable_name]", "Display the value of a variable."),
    ]),
    ("pnap-shell-mgmt", "Shell Command Management",
     "Aliases, scheduling, manuals, and history.", [
        e("alias [alias-name]='[command]'", "Create a shorter alias for a long command."),
        e("watch -n [seconds] [command]", "Run a command repeatedly at a custom interval."),
        e("sleep [seconds] && [command]", "Postpone the execution of a command."),
        e("at [hh:mm]", "Create a job to run at a certain time (Ctrl+D to finish)."),
        e("man [command]", "Display the built-in manual for a command."),
        e("history", "Print the command history of the terminal."),
    ]),
    ("pnap-shortcuts", "Keyboard Shortcuts",
     "Essential terminal key combos every user should know.", [
        e("Ctrl+C", "Kill the process running in the terminal."),
        e("Ctrl+Z", "Stop the current process — resume with fg (foreground) or bg (background)."),
        e("Ctrl+W", "Cut one word before the cursor."),
        e("Ctrl+U", "Cut everything before the cursor on the line."),
        e("Ctrl+K", "Cut everything after the cursor on the line."),
        e("Ctrl+Y", "Paste the last cut text."),
        e("Ctrl+R", "Recall the last command matching the typed characters."),
        e("Ctrl+O", "Run the previously recalled command."),
        e("Ctrl+G", "Exit command history search without running a command."),
        e("clear", "Clear the terminal screen."),
        e("!!", "Run the last command again."),
        e("exit", "Log out of the current shell session."),
    ]),
]

def main():
    session = SessionLocal()
    try:
        # idempotent: replace previously imported pnap-* sheets
        removed = (
            session.query(CheatSheet)
            .filter(CheatSheet.key.like("pnap-%"))
            .delete(synchronize_session=False)
        )
        print(f"removed {removed} previously imported sheets")
        for key, title, topic_desc, entries in CATEGORIES:
            # find a topic name used by UI, "commands" groups them all
            sheet = CheatSheet(
                key=key,
                title=title,
                topic="commands",
                category="cheat-sheet",
                content=json.dumps({
                    "source": SOURCE,
                    "entries": entries,
                }),
                is_active=True,
            )
            session.add(sheet)
            print(f"added: {title} ({len(entries)} entries)")
        session.commit()
        print("Done.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
