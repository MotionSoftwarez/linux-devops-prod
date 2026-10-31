"""Seed the Linux for DevOps curriculum database.

Run:  python scripts/seed.py
      (from the backend directory, with the virtualenv active)
"""
import json
import sys
import os

# Ensure the app package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.base import Base
from app.models.curriculum import (
    LearningPath,
    Module,
    Lesson,
    LearningObjective,
    CommandExample,
    Lab,
    LabScenario,
    CheatSheet,
    Assignment,
    Question,
)
from app.models.progress import Achievement
from app.models.user import User
from app.core.security import get_password_hash


def create_tables(db: Session):
    Base.metadata.create_all(bind=engine)


def add_paths(db: Session):
    paths = [
        {
            "key": "beginner",
            "title": "Linux Beginner",
            "description": "Become comfortable with the command line, filesystem, and basic operations.",
            "target_audience": "Complete beginners with little or no Linux knowledge.",
            "estimated_hours": 20,
            "order": 1,
        },
        {
            "key": "administrator",
            "title": "Linux Administrator",
            "description": "Manage users, services, packages, storage, and networking.",
            "target_audience": "Developers preparing for DevOps roles; support engineers.",
            "estimated_hours": 40,
            "order": 2,
        },
        {
            "key": "devops",
            "title": "DevOps Engineer",
            "description": "Automate operations, troubleshoot deployments, and operate Linux-hosted applications.",
            "target_audience": "Developers and sysadmins transitioning to DevOps.",
            "estimated_hours": 60,
            "order": 3,
        },
        {
            "key": "troubleshooter",
            "title": "Production Troubleshooter",
            "description": "Diagnose real-world system incidents systematically.",
            "target_audience": "SREs and support engineers handling production incidents.",
            "estimated_hours": 40,
            "order": 4,
        },
        {
            "key": "interview",
            "title": "Linux Interview Preparation",
            "description": "Practice commands, scenarios, and technical interview questions.",
            "target_audience": "Learners preparing for Linux, cloud, SRE, and DevOps interviews.",
            "estimated_hours": 25,
            "order": 5,
        },
        {
            "key": "advanced",
            "title": "Advanced Linux Engineer",
            "description": "Explore internals, performance, security, and production reliability.",
            "target_audience": "Experienced engineers wanting deep Linux expertise.",
            "estimated_hours": 60,
            "order": 6,
        },
    ]
    for p in paths:
        db.add(LearningPath(**p))
    db.commit()
    return {p["key"]: p for p in paths}


def add_modules(db: Session):
    """All 22 modules across 5 stages."""
    modules = [
        # STAGE 1 — Linux Foundations
        {"key": "m1_intro", "title": "Introduction to Linux and DevOps", "stage": "1",
         "order": 1, "estimated_hours": 3,
         "description": "What Linux is, kernel vs distribution, cloud/Containers/CI/CD, and basic terminal navigation."},
        {"key": "m2_terminal", "title": "Terminal Fundamentals", "stage": "1",
         "order": 2, "estimated_hours": 5,
         "description": "Shell prompts, command syntax, navigation, man pages, paths, wildcards, stdin/stdout/stderr."},
        {"key": "m3_files", "title": "Files and Directories", "stage": "1",
         "order": 3, "estimated_hours": 5,
         "description": "Filesystem hierarchy, touch/mkdir/cp/mv/rm, find, grep, safe deletion."},
        {"key": "m4_editing", "title": "Reading and Editing Files", "stage": "1",
         "order": 4, "estimated_hours": 5,
         "description": "cat/less/head/tail, nano/vim, log inspection, grep/sed/awk text processing."},
        # STAGE 2 — Core Linux Administration
        {"key": "m5_users", "title": "Users, Groups, and Permissions", "stage": "2",
         "order": 5, "estimated_hours": 6,
         "description": "Users/groups, chmod/chown/chgrp, sudo, least privilege, access troubleshooting."},
        {"key": "m6_packages", "title": "Package Management and Software Installation", "stage": "2",
         "order": 6, "estimated_hours": 5,
         "description": "APT/DPKG and RPM/DNF, repositories, dependencies, safe installation."},
        {"key": "m7_processes", "title": "Processes and Job Control", "stage": "2",
         "order": 7, "estimated_hours": 5,
         "description": "Processes, PIDs, signals, ps/top, background jobs, nohup/nice, safe termination."},
        {"key": "m8_systemd", "title": "Services and systemd", "stage": "2",
         "order": 8, "estimated_hours": 5,
         "description": "systemctl, journalctl, unit files, failed-service diagnosis, simulated web incident."},
        {"key": "m9_storage", "title": "Storage, Disks, and Filesystems", "stage": "2",
         "order": 9, "estimated_hours": 6,
         "description": "df/du/lsblk/mount, disk-full and inode incidents, fstab, swap, LVM concepts."},
        {"key": "m10_networking", "title": "Networking Fundamentals", "stage": "2",
         "order": 10, "estimated_hours": 6,
         "description": "IP/CIDR, DNS, ports, ip/ss/curl/dig, UFW firewall, SSH keys, connectivity diagnosis."},
        {"key": "m11_logs", "title": "Logs and System Troubleshooting", "stage": "2",
         "order": 11, "estimated_hours": 5,
         "description": "journalctl, /var/log, dmesg, log rotation, hypothesis-driven troubleshooting, simulated incident."},
        # STAGE 3 — Linux for Automation and DevOps
        {"key": "m12_bash", "title": "Bash Scripting", "stage": "3",
         "order": 12, "estimated_hours": 7,
         "description": "Variables, loops, conditions, functions, redirection, set -euo pipefail, bash -x debugging."},
        {"key": "m13_scheduling", "title": "Scheduling and Automation", "stage": "3",
         "order": 13, "estimated_hours": 5,
         "description": "Cron, at, systemd timers, idempotency, logging, scheduled-job troubleshooting."},
        {"key": "m14_ssh", "title": "SSH and Remote Administration", "stage": "3",
         "order": 14, "estimated_hours": 5,
         "description": "SSH keys, agents, scp/sftp, config, rsync, remote deployment."},
        {"key": "m15_git", "title": "Git and Linux-Based Development Workflows", "stage": "3",
         "order": 15, "estimated_hours": 5,
         "description": "Git fundamentals, branches/commits, terminal workflows, env vars, secrets handling."},
        {"key": "m16_webservers", "title": "Web Servers and Application Operations", "stage": "3",
         "order": 16, "estimated_hours": 6,
         "description": "Nginx install/inspect, virtual hosts, reverse proxy, logs, 403/404/500/502 diagnosis."},
        {"key": "m17_containers", "title": "Containers and Linux Internals", "stage": "3",
         "order": 17, "estimated_hours": 6,
         "description": "Namespaces, cgroups, Docker CLI, images/containers/volumes, container troubleshooting, K8s bridge."},
        # STAGE 4 — Advanced Linux Engineering
        {"key": "m18_advanced_shell", "title": "Advanced Shell and Text Processing", "stage": "4",
         "order": 18, "estimated_hours": 6,
         "description": "Advanced grep/awk/sed, regex, complex pipelines, large-log processing, unusual filenames."},
        {"key": "m19_security", "title": "Linux Security and Hardening", "stage": "4",
         "order": 19, "estimated_hours": 6,
         "description": "Least privilege, SSH hardening, firewall, patching, sudo policy, SELinux/AppArmor, audit logs."},
        {"key": "m20_performance", "title": "Performance and Resource Analysis", "stage": "4",
         "order": 20, "estimated_hours": 6,
         "description": "CPU/memory/disk I/O/network, load average, free/vmstat/iostat, lsof/strace, root-cause vs symptom."},
        {"key": "m21_boot", "title": "Boot, Kernel, and System Internals", "stage": "4",
         "order": 21, "estimated_hours": 6,
         "description": "Boot process, dmesg, /proc /sys /dev, kernel modules, signals, file descriptors, boot recovery."},
        {"key": "m22_capstone", "title": "Production Troubleshooting and Capstone", "stage": "5",
         "order": 22, "estimated_hours": 8,
         "description": "Structured incident response, multi-symptom simulations, RCA, post-incident report, final project."},
    ]
    for m in modules:
        db.add(Module(**m))
    db.commit()
    return {m["key"]: m for m in modules}


# ---------------------------------------------------------------------------
# Module 1: Introduction to Linux and DevOps
# ---------------------------------------------------------------------------
def module1_lessons(db: Session, module: Module):
    lessons = [
        {
            "key": "m1l1_what_is_linux",
            "title": "What Is Linux?",
            "slug": "m1-what-is-linux",
            "order": 1,
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "summary": "Linux is a kernel; distributions package it into full operating systems. Understand the difference and why it matters in DevOps.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "Linux is an operating system kernel — the core that manages hardware, memory, processes, and devices. By itself, a kernel is not a complete operating system. A Linux distribution (distro) combines the kernel with GNU tools, a shell, package manager, and installer into a usable OS (e.g., Ubuntu, Debian, RHEL, Alpine)."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Most cloud servers, containers, CI/CD runners, and production services run Linux. As a DevOps engineer you will deploy, configure, and troubleshoot Linux every day."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Provisioning EC2 instances, building Docker images, writing CI/CD pipelines, configuring Kubernetes nodes, and monitoring production servers."},
                    {"type": "text", "title": "How does it work?",
                     "content": "The kernel sits between hardware and applications. User-space tools (shell, utilities) talk to the kernel through system calls. Distributions differ in package manager (apt vs dnf), init system (usually systemd), and release cycle."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Using the wrong package manager command for a distribution, assuming a command exists when it's installed by a different package, or confusing kernel version with distro version."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Check `/etc/os-release` to identify the distribution, use `uname -r` for the kernel version, and choose the correct package manager."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Run commands to identify OS and kernel, and answer a short quiz distinguishing kernel vs distribution."},
                ],
                "keyTerms": ["kernel", "distribution", "user space", "system call"],
            }),
            "completion_criteria": "View lesson + complete knowledge check.",
        },
        {
            "key": "m1l2_kernel_shell_terminal",
            "title": "Kernel, Shell, Terminal, and Filesystem",
            "slug": "m1-kernel-shell-terminal-filesystem",
            "order": 2,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "The relationship between kernel, shell, terminal emulator, and the Linux filesystem.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "The kernel manages hardware. The shell (e.g., bash) is a command interpreter that runs user commands. The terminal is the window/emulator that displays the shell and sends keystrokes. The filesystem organizes data in a tree rooted at `/`."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "You interact with Linux through the shell inside a terminal. Understanding the layers prevents confusion when commands behave differently across terminals or when using remote SSH."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Every time you open a terminal, connect via SSH, or write a shell script. You must know which layer is responsible for what behavior."},
                    {"type": "text", "title": "How does it work?",
                     "content": "Terminal emulator → sends keystrokes → Shell reads line → parses command → forks/execs program → kernel runs it → output returns to terminal."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Confusing the terminal with the shell, running commands in the wrong shell (bash vs zsh vs sh), or not realizing SSH gives you a shell on a remote machine."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Use `echo $SHELL` to see your shell, `ps -p $$` to see the current process, and `which` to locate commands."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Draw/identify the layers and run diagnostic commands showing shell and kernel info."},
                ],
            }),
            "completion_criteria": "View lesson + run diagnostic commands in terminal lab.",
        },
        {
            "key": "m1l3_linux_in_cloud_devops",
            "title": "Linux in Cloud, Containers, CI/CD, and Production",
            "slug": "m1-linux-cloud-containers-cicd",
            "order": 3,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "How Linux underpins cloud computing, containers, CI/CD, and production systems.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "Cloud providers offer virtual machines running Linux. Containers (Docker) share the host Linux kernel. CI/CD pipelines run jobs on Linux runners. Production microservices are typically Linux containers or VMs."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Nearly all DevOps tooling assumes Linux. Understanding the Linux foundation lets you debug containers, pipelines, and production services effectively."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Choosing a base image for Docker, writing GitHub Actions/GitLab CI jobs, deploying to EC2/GCP Compute Engine, and managing Kubernetes nodes."},
                    {"type": "text", "title": "How does it work?",
                     "content": "A VM virtualizes hardware and runs its own kernel. A container uses Linux namespaces and cgroups to isolate processes while sharing the host kernel — making containers lightweight and fast."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Assuming a command available on your Ubuntu dev machine exists in an Alpine container image, or using Linux-only paths in cross-platform scripts."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Check the base image (`cat /etc/os-release` inside container), use multi-stage builds, and test CI jobs on the same OS as production."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Explain VM vs container difference and identify where Linux appears in a sample CI/CD pipeline diagram."},
                ],
            }),
            "completion_criteria": "View lesson + knowledge check.",
        },
        {
            "key": "m1l4_learning_environments",
            "title": "Learning Environments: VMs, WSL, Remote Servers",
            "slug": "m1-learning-environments",
            "order": 4,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "Options for practicing Linux: virtual machines, WSL on Windows, and remote servers.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "You can learn Linux on a virtual machine (VirtualBox/VMware), WSL (Windows Subsystem for Linux) on Windows, or a remote cloud server accessed via SSH. Each has trade-offs in setup, performance, and isolation."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Your learning environment should be safe to break. A VM or WSL lets you experiment without risking your main computer; remote servers teach real SSH-based administration."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Daily — developers use WSL, teams manage remote servers, and everyone uses VMs/containers for testing."},
                    {"type": "text", "title": "How does it work?",
                     "content": "VM: hypervisor runs a full guest OS. WSL: a Linux kernel runs alongside Windows, integrating with the Windows filesystem. Remote: SSH connects your terminal to a shell on a distant machine."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "WSL file-permission oddities, VM network/NAT issues, or SSH connection timeouts to remote servers."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Check VM network settings, use `wsl --status`, verify SSH with `ssh -v`, and confirm firewall rules allow port 22."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Choose an environment for the course and verify access by running `uname -a` and `pwd`."},
                ],
            }),
            "completion_criteria": "View lesson + set up/verify learning environment.",
        },
        {
            "key": "m1l5_first_commands",
            "title": "Your First Commands and Terminal Navigation",
            "slug": "m1-first-commands-navigation",
            "order": 5,
            "difficulty": "beginner",
            "estimated_minutes": 25,
            "has_lab": True,
            "has_quiz": True,
            "summary": "Run your first commands: pwd, ls, cd, clear, history. Navigate the filesystem safely.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "A command is a program you run in the shell. Commands take arguments (what to act on) and options/flags (how to behave, usually starting with `-` or `--`). `pwd` prints your current directory, `ls` lists files, `cd` changes directory, `clear` clears the screen, and `history` shows past commands."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Navigation is the foundation of everything in Linux. You must know where you are and how to move before you can read files, edit config, or manage services."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Constantly — moving to application directories, checking log locations, verifying you're in the right place before running destructive commands."},
                    {"type": "text", "title": "How does it work?",
                     "content": "The shell maintains a current working directory. `cd` changes it; `ls` lists its contents; `pwd` reports the absolute path. Each command returns an exit code (0 = success)."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Typing a command that doesn't exist (`command not found`), `cd` to a missing directory (`No such file or directory`), or running as the wrong user (`Permission denied`)."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Use `which` or `type` to locate a command, `pwd` to confirm location, `ls` to verify existence, and read the error message carefully."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Navigate to a target directory, list its contents, and print the working path in the terminal lab."},
                ],
            }),
            "completion_criteria": "Complete terminal lab: navigate and report pwd.",
        },
    ]
    orm_lessons = []
    for l in lessons:
        orm_lessons.append(Lesson(module_id=module.id, **l))
    db.add_all(orm_lessons)
    db.commit()
    for ol in orm_lessons:
        db.refresh(ol)
    # Return ORM objects keyed by lesson key
    return {ol.key: ol for ol in orm_lessons}


def module1_objectives_examples(db: Session, lessons: dict):
    """Objectives and command examples for Module 1 lessons."""
    # Lesson: What is Linux
    l = lessons["m1l1_what_is_linux"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Explain the difference between the Linux kernel and a Linux distribution.", order=1),
        LearningObjective(lesson_id=l.id, text="Name three common Linux distributions and their typical use cases.", order=2),
        LearningObjective(lesson_id=l.id, text="Identify where Linux appears in cloud, containers, and CI/CD.", order=3),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="cat /etc/os-release", description="Show distribution name and version.", expected_output='NAME="Ubuntu"\nVERSION="22.04 LTS"\n...', order=1),
        CommandExample(lesson_id=l.id, command="uname -r", description="Show the running kernel version.", expected_output="5.15.0-XX-generic", order=2),
    ])

    # Lesson: Kernel/Shell/Terminal/Filesystem
    l = lessons["m1l2_kernel_shell_terminal"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Distinguish the kernel, shell, terminal, and filesystem.", order=1),
        LearningObjective(lesson_id=l.id, text="Use echo $SHELL and ps -p $$ to identify your shell.", order=2),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="echo $SHELL", description="Print the current shell program.", expected_output="/bin/bash", order=1),
        CommandExample(lesson_id=l.id, command="ps -p $$", description="Show the current shell process.", expected_output="  PID TTY      STAT TIME COMMAND\n12345 pts/0    Ss   0:00 bash", order=2),
    ])

    # Lesson: Linux in cloud/devops
    l = lessons["m1l3_linux_in_cloud_devops"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Explain how Linux underpins cloud, containers, and CI/CD.", order=1),
        LearningObjective(lesson_id=l.id, text="Contrast virtual machines with containers.", order=2),
    ])

    # Lesson: Learning environments
    l = lessons["m1l4_learning_environments"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Compare VMs, WSL, and remote servers as learning environments.", order=1),
        LearningObjective(lesson_id=l.id, text="Verify access to your chosen environment.", order=2),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="uname -a", description="Show system and kernel information.", expected_output="Linux ubuntu 5.15.0-XX-generic #... GNU/Linux", order=1),
        CommandExample(lesson_id=l.id, command="pwd", description="Print the current working directory.", expected_output="/home/learner", order=2),
    ])

    # Lesson: First commands
    l = lessons["m1l5_first_commands"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Run pwd, ls, cd, clear, history correctly.", order=1),
        LearningObjective(lesson_id=l.id, text="Interpret common errors: command not found, No such file, Permission denied.", order=2),
        LearningObjective(lesson_id=l.id, text="Navigate to a directory and confirm location with pwd.", order=3),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="pwd", description="Print working directory.", expected_output="/home/learner", order=1),
        CommandExample(lesson_id=l.id, command="ls", description="List files in current directory.", expected_output="Documents  Downloads  Music  ...", order=2),
        CommandExample(lesson_id=l.id, command="cd /etc && pwd", description="Change to /etc and confirm.", expected_output="/etc", order=3),
        CommandExample(lesson_id=l.id, command="clear", description="Clear the terminal screen.", expected_output="(screen cleared)", order=4),
        CommandExample(lesson_id=l.id, command="history", description="Show recently run commands.", expected_output="1  pwd\n2  ls\n3  cd /etc", order=5),
    ])

    # Quiz for first commands
    db.add_all([
        Assignment(lesson_id=l.id, level="foundation", title="Knowledge Check: First Commands",
                   instructions="Answer these questions about basic terminal navigation.", points=10, order=1),
    ])
    db.commit()
    return lessons


def module1_case_studies_and_labs(db: Session, module: Module, lessons: dict):
    """Lab + case study for the first-commands lesson."""
    l = lessons["m1l5_first_commands"]
    lab = Lab(
        lesson_id=l.id,
        title="Navigate to a Target Directory",
        objective="Navigate into /var/log, list its contents, and report your working directory.",
        completion_criteria=json.dumps({
            "checks": [
                {"id": "c1", "type": "command_run", "command": "cd /var/log", "message": "Changed directory to /var/log"},
                {"id": "c2", "type": "command_run", "command": "ls", "message": "Listed directory contents"},
                {"id": "c3", "type": "command_run", "command": "pwd", "message": "Printed working directory"},
            ]
        }),
        initial_state=json.dumps({"cwd": "/home/learner"}),
        safe_commands=json.dumps(["pwd", "ls", "cd", "clear", "history"]),
    )
    db.add(lab)
    db.commit()

    # Case study: first commands in context
    db.add(LabScenario(
        lab_id=lab.id,
        key="m1-cs-first-commands",
        title="Finding the Right Log Directory",
        context="A junior developer needs to check application logs but isn't sure where they live.",
        symptoms="The developer is in their home directory and doesn't know how to reach /var/log.",
        evidence="Terminal starts at /home/learner. Logs are conventionally under /var/log.",
        root_cause="Not knowing how to navigate the filesystem using cd, ls, and pwd.",
        solution="Use cd /var/log, then ls to list logs, then pwd to confirm location.",
        verification="pwd returns /var/log and ls shows log files.",
        prevention="Practice navigation until it is muscle memory; use pwd before destructive commands.",
        is_guided=True,
        order=1,
    ))
    db.commit()


# ---------------------------------------------------------------------------
# Module 2: Terminal Fundamentals
# ---------------------------------------------------------------------------
def module2_lessons(db: Session, module: Module):
    lessons = [
        {
            "key": "m2l1_shell_prompt_syntax",
            "title": "Shell Prompts and Command Syntax",
            "slug": "m2-shell-prompt-command-syntax",
            "order": 1,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "Read the shell prompt, understand command syntax (command, arguments, options, flags), and quoting.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "The shell prompt shows context (user, host, working directory) before accepting input. A command line has: command (the program), arguments (what it acts on), and options/flags (modify behavior, e.g. `ls -l`). Quoting (`' '`, `" "`, backslash) controls how the shell interprets special characters and spaces."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Misreading a prompt can lead to running commands in the wrong directory or as the wrong user. Incorrect quoting breaks commands with filenames containing spaces."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Every command invocation — writing scripts, editing configs, passing arguments to deployment tools."},
                    {"type": "text", "title": "How does it work?",
                     "content": "Shell parses the line: finds the command, splits arguments, expands wildcards/variables, applies quoting rules, then executes."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Forgetting quotes around `My File.txt`, mixing up `-l` (long list) vs `-a` (all files), or running a command as root unintentionally."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Read the prompt before typing, use `type`/`which` to confirm the command, and add quotes around paths with spaces."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Construct commands with arguments and flags, quote a filename with spaces, and read the prompt context."},
                ],
            }),
            "completion_criteria": "View lesson + complete knowledge check.",
        },
        {
            "key": "m2l2_man_help_type_which",
            "title": "Getting Help: man, help, type, which",
            "slug": "m2-getting-help-man-help-type-which",
            "order": 2,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "Use man pages, built-in help, type, and which to understand commands.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "`man` shows the full manual page for a command. `help` shows built-in shell command help. `type` tells you whether a command is a shell builtin, alias, or external program. `which` locates the executable file on disk."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "You cannot memorize every flag. Knowing how to read documentation is the skill that makes you self-sufficient."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Before using an unfamiliar flag, when a command behaves unexpectedly, or when locating where a tool is installed."},
                    {"type": "text", "title": "How does it work?",
                     "content": "`man ls` opens the ls manual in a pager. `type cd` says `cd is a shell builtin`. `which ls` says `/bin/ls`. Press `q` to quit a man page."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "man not installed (`man: command not found` on minimal containers), or `which` not finding a shell builtin (builtins aren't files on disk)."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Use `help` for builtins, `type` to classify, and install `man` (`apt install man`) if missing."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Use man/help/type/which on several commands and explain the difference between builtin and external."},
                ],
            }),
            "completion_criteria": "View lesson + run help commands in terminal lab.",
        },
        {
            "key": "m2l3_absolute_relative_paths",
            "title": "Absolute and Relative Paths",
            "slug": "m2-absolute-relative-paths",
            "order": 3,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "Absolute paths start from `/`; relative paths start from your current directory. `.` and `..` navigation.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "An absolute path begins with `/` (the root) and works from anywhere, e.g. `/etc/hosts`. A relative path is resolved from your current working directory, e.g. `../config/app.conf`. `.` means current directory; `..` means parent directory."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Scripts and commands using relative paths break when run from a different directory. Absolute paths are safer in automation and cron jobs."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Referencing config files in scripts, setting log paths, and writing cron jobs that run from arbitrary directories."},
                    {"type": "text", "title": "How does it work?",
                     "content": "The shell resolves `.` and `..` against `$PWD`. Absolute paths are used as-is by the kernel."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Using a relative path in a cron job (runs from `$HOME`), or `cd ..` from root `/` (stays at `/`)."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Print `pwd` before using relative paths, convert to absolute with `realpath`, and test scripts from multiple directories."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Convert relative paths to absolute and navigate using `.` and `..` in the terminal lab."},
                ],
            }),
            "completion_criteria": "View lesson + path navigation lab.",
        },
        {
            "key": "m2l4_wildcards_expansion",
            "title": "Wildcards and Filename Expansion",
            "slug": "m2-wildcards-filename-expansion",
            "order": 4,
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "summary": "Use `*`, `?`, and character sets `[]` to match multiple filenames.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "Wildcards let you match groups of files: `*` matches any characters, `?` matches one character, `[abc]` matches one character from the set. The shell expands them before the command runs."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Operate on many files at once instead of typing each name — essential for log rotation, backups, and cleanup."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Deleting rotated logs (`rm access.log.*`), listing config backups (`ls *.bak`), or targeting image files."},
                    {"type": "text", "title": "How does it work?",
                     "content": "`echo *.log` expands to all `.log` files in the current directory before `echo` runs."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "`rm *` deletes everything (dangerous!), wildcards don't match hidden files (starting with `.`) by default, and too many matches cause `Argument list too long`."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Preview with `echo` before `rm`, use `ls -a` for hidden files, and use `find` for very large file sets."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "List files matching patterns and safely remove a set of log files in the lab."},
                ],
            }),
            "completion_criteria": "View lesson + wildcard practice lab.",
        },
        {
            "key": "m2l5_stdin_stdout_stderr",
            "title": "Standard Input, Output, and Error",
            "slug": "m2-stdin-stdout-stderr",
            "order": 5,
            "difficulty": "beginner",
            "estimated_minutes": 25,
            "has_lab": True,
            "has_quiz": True,
            "summary": "Understand stdin (0), stdout (1), stderr (2), and how redirection separates normal output from errors.",
            "content": json.dumps({
                "sections": [
                    {"type": "text", "title": "What is this concept?",
                     "content": "Every process has three standard streams: stdin (0, input), stdout (1, normal output), and stderr (2, error messages). By default all three connect to your terminal. You can redirect them with `>`, `>>`, `<`, `2>`, and `2>&1`."},
                    {"type": "text", "title": "Why does it matter?",
                     "content": "Separating errors from output lets you log successes and failures differently, and chain commands safely."},
                    {"type": "text", "title": "When will a DevOps engineer use it?",
                     "content": "Capturing command output to logs, suppressing errors in scripts, debugging failing deployments, and building pipelines."},
                    {"type": "text", "title": "How does it work?",
                     "content": "`cmd > out.txt` sends stdout to a file. `cmd 2> err.txt` sends errors separately. `cmd > out.txt 2>&1` merges both into one file."},
                    {"type": "text", "title": "How can it fail?",
                     "content": "Accidentally overwriting a file with `>` instead of appending with `>>`, or merging stderr when you only wanted stdout."},
                    {"type": "text", "title": "How do we diagnose and fix?",
                     "content": "Run without redirection to see both streams, use `2>` to isolate errors, and verify with `cat` after redirecting."},
                    {"type": "text", "title": "How can the learner prove they understand?",
                     "content": "Redirect stdout and stderr to separate files and confirm each contains the expected content in the lab."},
                ],
            }),
            "completion_criteria": "Complete terminal lab: redirect stdout and stderr separately.",
        },
    ]
    orm_lessons = []
    for l in lessons:
        orm_lessons.append(Lesson(module_id=module.id, **l))
    db.add_all(orm_lessons)
    db.commit()
    for ol in orm_lessons:
        db.refresh(ol)
    return {ol.key: ol for ol in orm_lessons}


def module2_objectives_examples(db: Session, lessons: dict):
    l = lessons["m2l1_shell_prompt_syntax"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Read the shell prompt and identify user, host, and directory.", order=1),
        LearningObjective(lesson_id=l.id, text="Distinguish command, argument, option, and flag.", order=2),
        LearningObjective(lesson_id=l.id, text="Use quotes to handle filenames with spaces.", order=3),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="ls -l /etc", description="Long listing of /etc.", expected_output="total 123\n-rw-r--r-- 1 root root ... hosts", order=1),
        CommandExample(lesson_id=l.id, command="ls 'My File.txt'", description="List a file with a space in its name.", expected_output="My File.txt", order=2),
    ])

    l = lessons["m2l2_man_help_type_which"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Use man to read a command's full documentation.", order=1),
        LearningObjective(lesson_id=l.id, text="Use type and which to classify and locate commands.", order=2),
        LearningObjective(lesson_id=l.id, text="Use help for shell builtins.", order=3),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="type cd", description="Classify the cd command.", expected_output="cd is a shell builtin", order=1),
        CommandExample(lesson_id=l.id, command="which ls", description="Locate the ls executable.", expected_output="/bin/ls", order=2),
        CommandExample(lesson_id=l.id, command="man ls", description="Open the ls manual (press q to quit).", expected_output="(manual page opens)", order=3),
    ])

    l = lessons["m2l3_absolute_relative_paths"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Distinguish absolute and relative paths.", order=1),
        LearningObjective(lesson_id=l.id, text="Use . and .. for navigation.", order=2),
        LearningObjective(lesson_id=l.id, text="Convert a relative path to absolute with realpath.", order=3),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="cd /etc && pwd", description="Absolute path navigation.", expected_output="/etc", order=1),
        CommandExample(lesson_id=l.id, command="cd .. && pwd", description="Move to parent directory.", expected_output="/", order=2),
        CommandExample(lesson_id=l.id, command="realpath ../hosts", description="Resolve relative path to absolute.", expected_output="/etc/hosts", order=3),
    ])

    l = lessons["m2l4_wildcards_expansion"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Use *, ?, and [] wildcards.", order=1),
        LearningObjective(lesson_id=l.id, text="Preview expansion with echo before destructive commands.", order=2),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="ls *.log", description="List all .log files.", expected_output="access.log  error.log", order=1),
        CommandExample(lesson_id=l.id, command="echo access.log.*", description="Preview rotated log matches.", expected_output="access.log.1  access.log.2", order=2),
    ])

    l = lessons["m2l5_stdin_stdout_stderr"]
    db.add_all([
        LearningObjective(lesson_id=l.id, text="Identify stdin(0), stdout(1), stderr(2).", order=1),
        LearningObjective(lesson_id=l.id, text="Redirect stdout and stderr to separate files.", order=2),
        LearningObjective(lesson_id=l.id, text="Use >> to append instead of overwrite.", order=3),
    ])
    db.add_all([
        CommandExample(lesson_id=l.id, command="ls > output.txt 2> errors.txt", description="Separate output and errors.", expected_output="(nothing on screen; files written)", order=1),
        CommandExample(lesson_id=l.id, command="ls /nonexistent 2> err.txt", description="Capture an error to a file.", expected_output="cat err.txt -> No such file or directory", order=2),
        CommandExample(lesson_id=l.id, command="echo 'line' >> log.txt", description="Append to a file.", expected_output="(appended to log.txt)", order=3),
    ])
    db.commit()
    return lessons


def module2_labs_and_case_studies(db: Session, module: Module, lessons: dict):
    """Lab for stdin/stdout/stderr lesson; case study for wildcard cleanup."""
    l = lessons["m2l5_stdin_stdout_stderr"]
    lab = Lab(
        lesson_id=l.id,
        title="Separate Output and Errors",
        objective="Run a command that produces output and an error, redirecting stdout to result.txt and stderr to errors.txt, then confirm each file's contents.",
        completion_criteria=json.dumps({
            "checks": [
                {"id": "c1", "type": "command_run", "command": "ls", "message": "Ran a listing command"},
                {"id": "c2", "type": "file_exists", "path": "result.txt", "message": "result.txt exists"},
                {"id": "c3", "type": "file_exists", "path": "errors.txt", "message": "errors.txt exists"},
                {"id": "c4", "type": "command_run", "command": "cat result.txt", "message": "Displayed result.txt"},
                {"id": "c5", "type": "command_run", "command": "cat errors.txt", "message": "Displayed errors.txt"},
            ]
        }),
        initial_state=json.dumps({"cwd": "/home/learner", "files": {}}),
        safe_commands=json.dumps(["ls", "cat", "echo", "pwd", "2>", ">", ">>"]),
    )
    db.add(lab)
    db.commit()

    # Case study: wildcard cleanup
    l2 = lessons["m2l4_wildcards_expansion"]
    # Attach a lab to wildcard lesson too
    lab2 = Lab(
        lesson_id=l2.id,
        title="Clean Rotated Logs Safely",
        objective="Preview then remove rotated log files matching access.log.* without deleting access.log itself.",
        completion_criteria=json.dumps({
            "checks": [
                {"id": "c1", "type": "command_run", "command": "echo", "message": "Previewed matches with echo"},
                {"id": "c2", "type": "command_run", "command": "rm", "message": "Removed rotated logs"},
            ]
        }),
        initial_state=json.dumps({"cwd": "/var/log", "files": {"access.log": True, "access.log.1": True, "access.log.2": True}}),
        safe_commands=json.dumps(["ls", "echo", "rm", "pwd"]),
    )
    db.add(lab2)
    db.commit()

    db.add(LabScenario(
        lab_id=lab2.id,
        key="m2-cs-wildcard-cleanup",
        title="Rotated Log Cleanup",
        context="A web server produces rotated logs access.log.1, access.log.2, ... You must remove old rotations but keep the current access.log.",
        symptoms="The /var/log directory is cluttered with old rotated logs.",
        evidence="Files: access.log, access.log.1, access.log.2. Goal: keep access.log, remove the rest.",
        root_cause="Not previewing the wildcard expansion before deleting.",
        solution="Run echo access.log.* to preview, then rm access.log.* to delete only rotated files.",
        verification="ls shows only access.log remains.",
        prevention="Always preview with echo/ls before rm with wildcards.",
        is_guided=True,
        order=1,
    ))
    db.commit()


# ---------------------------------------------------------------------------
# Assignments & questions for Module 1 & 2
# ---------------------------------------------------------------------------
def add_assignments_and_questions(db: Session, lessons: dict):
    # Module 1 lesson 5 quiz
    l = lessons["m1l5_first_commands"]
    a = Assignment(lesson_id=l.id, level="foundation", title="Knowledge Check: First Commands",
                   instructions="Answer these questions about basic terminal navigation.", points=10, order=1)
    db.add(a); db.commit(); db.refresh(a)
    db.add_all([
        Question(assignment_id=a.id, type="multiple_choice", prompt="Which command prints your current working directory?",
                 options=json.dumps(["ls","pwd","cd","clear"]), correct_answer=json.dumps("pwd"), explanation="pwd = print working directory.", points=2, order=1),
        Question(assignment_id=a.id, type="multiple_choice", prompt="Which command lists files in the current directory?",
                 options=json.dumps(["cd","ls","pwd","man"]), correct_answer=json.dumps("ls"), explanation="ls lists directory contents.", points=2, order=2),
        Question(assignment_id=a.id, type="multiple_choice", prompt="Which command changes directory?",
                 options=json.dumps(["ls","pwd","cd","clear"]), correct_answer=json.dumps("cd"), explanation="cd changes the working directory.", points=2, order=3),
        Question(assignment_id=a.id, type="multiple_choice", prompt="What does `clear` do?",
                 options=json.dumps(["Lists files","Changes directory","Clears the screen","Shows history"]), correct_answer=json.dumps("Clears the screen"), explanation="clear clears the terminal display.", points=2, order=4),
        Question(assignment_id=a.id, type="command_completion", prompt="Type the command to print your working directory.",
                 options=None, correct_answer=json.dumps("pwd"), explanation="pwd prints the current working directory path.", points=2, order=5),
    ])

    # Module 2 lesson 5 quiz
    l = lessons["m2l5_stdin_stdout_stderr"]
    a = Assignment(lesson_id=l.id, level="foundation", title="Knowledge Check: stdin/stdout/stderr",
                   instructions="Answer these questions about standard streams and redirection.", points=10, order=1)
    db.add(a); db.commit(); db.refresh(a)
    db.add_all([
        Question(assignment_id=a.id, type="multiple_choice", prompt="Which file descriptor is standard output?",
                 options=json.dumps(["0","1","2","3"]), correct_answer=json.dumps("1"), explanation="stdout is file descriptor 1.", points=2, order=1),
        Question(assignment_id=a.id, type="multiple_choice", prompt="Which redirect sends errors to a file?",
                 options=json.dumps([">","2>","<","2>&1"]), correct_answer=json.dumps("2>"), explanation="2> redirects stderr (fd 2) to a file.", points=2, order=2),
        Question(assignment_id=a.id, type="multiple_choice", prompt="What does >> do compared to >?",
                 options=json.dumps(["Overwrites","Appends","Reads input","Deletes"]), correct_answer=json.dumps("Appends"), explanation=">> appends to a file instead of overwriting.", points=2, order=3),
        Question(assignment_id=a.id, type="command_completion", prompt="Write the redirect that sends both stdout and stderr to output.txt.",
                 options=None, correct_answer=json.dumps("> output.txt 2>&1"), explanation="> sends stdout; 2>&1 merges stderr into stdout.", points=2, order=4),
        Question(assignment_id=a.id, type="output_interpretation", prompt="If `ls /nonexistent 2> err.txt` runs, what appears on the terminal?",
                 options=json.dumps(["Nothing","The error message","The directory listing","A syntax error"]), correct_answer=json.dumps("Nothing"), explanation="stdout is empty and stderr is redirected to err.txt, so the terminal shows nothing.", points=2, order=5),
    ])

    # Module 2 lesson 4 (wildcards) practical assignment
    l = lessons["m2l4_wildcards_expansion"]
    a = Assignment(lesson_id=l.id, level="practical", title="Wildcard Log Cleanup",
                   instructions="Use wildcards to list and remove rotated logs safely. Preview first with echo.", points=15, order=1)
    db.add(a); db.commit(); db.refresh(a)
    db.add_all([
        Question(assignment_id=a.id, type="command_completion", prompt="Preview all files matching access.log.* without deleting them.",
                 options=None, correct_answer=json.dumps("echo access.log.*"), explanation="echo shows the expansion so you can verify before rm.", points=3, order=1),
        Question(assignment_id=a.id, type="command_completion", prompt="Remove all rotated logs matching access.log.*.",
                 options=None, correct_answer=json.dumps("rm access.log.*"), explanation="rm deletes the expanded list of rotated log files.", points=3, order=2),
        Question(assignment_id=a.id, type="multiple_choice", prompt="Why should you preview with echo before rm with wildcards?",
                 options=json.dumps(["It's faster","To verify which files will be deleted","To compress them","To rename them"]), correct_answer=json.dumps("To verify which files will be deleted"), explanation="Prevents accidental deletion of the wrong files.", points=3, order=3),
    ])
    db.commit()


# ---------------------------------------------------------------------------
# Cheat sheets (initial library)
# ---------------------------------------------------------------------------
def add_cheat_sheets(db: Session):
    sheets = [
        {
            "key": "essential-commands",
            "title": "Essential Linux Commands",
            "topic": "navigation",
            "category": "foundation",
            "content": json.dumps({
                "entries": [
                    {"cmd": "pwd", "syntax": "pwd", "what": "Print working directory.", "opts": [], "example": "pwd", "output": "/home/learner", "mistake": "Forgetting where you are before destructive commands.", "safety": "Safe.", "distro": "All"},
                    {"cmd": "ls", "syntax": "ls [options] [path]", "what": "List directory contents.", "opts": ["-l long","-a all including hidden","-h human sizes"], "example": "ls -lah /etc", "output": "-rw-r--r-- ...", "mistake": "Assuming ls shows hidden files by default (it doesn't).", "safety": "Safe.", "distro": "All"},
                    {"cmd": "cd", "syntax": "cd [path]", "what": "Change directory.", "opts": [".. parent","- previous"], "example": "cd /var/log", "output": "(directory changed)", "mistake": "cd to a nonexistent path -> No such file or directory.", "safety": "Safe.", "distro": "All"},
                    {"cmd": "clear", "syntax": "clear", "what": "Clear the terminal screen.", "opts": [], "example": "clear", "output": "(screen cleared)", "mistake": "None.", "safety": "Safe.", "distro": "All"},
                    {"cmd": "history", "syntax": "history [n]", "what": "Show command history.", "opts": [], "example": "history 10", "output": "1  pwd\n2  ls ...", "mistake": "None.", "safety": "Safe.", "distro": "All"},
                ]
            }),
        },
        {
            "key": "redirection",
            "title": "Redirection and Pipes",
            "topic": "shell",
            "category": "foundation",
            "content": json.dumps({
                "entries": [
                    {"cmd": ">", "syntax": "cmd > file", "what": "Redirect stdout to file (overwrite).", "opts": [], "example": "ls > list.txt", "output": "(file written)", "mistake": "Accidentally overwriting an existing file.", "safety": "Overwrites without warning.", "distro": "All"},
                    {"cmd": ">>", "syntax": "cmd >> file", "what": "Redirect stdout to file (append).", "opts": [], "example": "echo 'line' >> log.txt", "output": "(appended)", "mistake": "None.", "safety": "Safe (append only).", "distro": "All"},
                    {"cmd": "2>", "syntax": "cmd 2> file", "what": "Redirect stderr to file.", "opts": [], "example": "ls /no 2> err.txt", "output": "(error written to err.txt)", "mistake": "Confusing 2> with >.", "safety": "Safe.", "distro": "All"},
                    {"cmd": "2>&1", "syntax": "cmd > file 2>&1", "what": "Merge stderr into stdout.", "opts": [], "example": "cmd > out.txt 2>&1", "output": "(everything in out.txt)", "mistake": "Order matters: > file 2>&1, not 2>&1 > file.", "safety": "Safe.", "distro": "All"},
                    {"cmd": "|", "syntax": "cmd1 | cmd2", "what": "Pipe stdout of cmd1 into stdin of cmd2.", "opts": [], "example": "ls | grep log", "output": "access.log\nerror.log", "mistake": "Piping stderr instead of stdout.", "safety": "Safe.", "distro": "All"},
                ]
            }),
        },
        {
            "key": "wildcards",
            "title": "Wildcards and Filename Expansion",
            "topic": "navigation",
            "category": "foundation",
            "content": json.dumps({
                "entries": [
                    {"cmd": "*", "syntax": "cmd *pattern*", "what": "Match any number of characters.", "opts": [], "example": "ls *.log", "output": "access.log  error.log", "mistake": "rm * deletes everything.", "safety": "Destructive with rm — preview first.", "distro": "All"},
                    {"cmd": "?", "syntax": "cmd ?", "what": "Match exactly one character.", "opts": [], "example": "ls file?.txt", "output": "file1.txt  file2.txt", "mistake": "None.", "safety": "Safe.", "distro": "All"},
                    {"cmd": "[]", "syntax": "cmd [set]", "what": "Match one character from the set.", "opts": [], "example": "ls [abc]*", "output": "apple.txt  banana.txt", "mistake": "None.", "safety": "Safe.", "distro": "All"},
                ]
            }),
        },
        {
            "key": "help-docs",
            "title": "Help and Documentation",
            "topic": "shell",
            "category": "foundation",
            "content": json.dumps({
                "entries": [
                    {"cmd": "man", "syntax": "man [command]", "what": "Show the manual page for a command.", "opts": [], "example": "man ls", "output": "(manual page; press q to quit)", "mistake": "man not installed on minimal systems.", "safety": "Safe.", "distro": "Most (install man package if missing)"},
                    {"cmd": "help", "syntax": "help [builtin]", "what": "Help for shell builtins.", "opts": [], "example": "help cd", "output": "cd: cd [-L|[-P [-e]] [-@] [dir]]", "mistake": "Using help on external commands (use man instead).", "safety": "Safe.", "distro": "bash"},
                    {"cmd": "type", "syntax": "type [command]", "what": "Classify a command (builtin/alias/external).", "opts": [], "example": "type cd", "output": "cd is a shell builtin", "mistake": "None.", "safety": "Safe.", "distro": "bash"},
                    {"cmd": "which", "syntax": "which [command]", "what": "Locate the executable file on disk.", "opts": [], "example": "which ls", "output": "/bin/ls", "mistake": "which doesn't find shell builtins.", "safety": "Safe.", "distro": "All"},
                ]
            }),
        },
    ]
    for s in sheets:
        db.add(CheatSheet(**s))
    db.commit()


# ---------------------------------------------------------------------------
# Achievements
# ---------------------------------------------------------------------------
def add_achievements(db: Session):
    ach = [
        {"key": "first_steps", "title": "First Steps", "description": "Complete your first lesson.", "badge_icon": "flag", "is_active": True},
        {"key": "navigator", "title": "Navigator", "description": "Complete Module 1: Introduction to Linux.", "badge_icon": "compass", "is_active": True},
        {"key": "terminal_master", "title": "Terminal Master", "description": "Complete Module 2: Terminal Fundamentals.", "badge_icon": "terminal", "is_active": True},
    ]
    for a in ach:
        db.add(Achievement(**a))
    db.commit()


# ---------------------------------------------------------------------------
# Demo user
# ---------------------------------------------------------------------------
def add_demo_user(db: Session):
    if not db.query(User).filter(User.username == "demo").first():
        db.add(User(
            email="demo@linotutor.local",
            username="demo",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo Learner",
            learning_goal="beginner",
        ))
        db.commit()


def run():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "linotutor.db")
    # Fresh dev database: remove existing sqlite file for idempotent seeding
    if os.path.exists(db_path):
        os.remove(db_path)

    db: Session = SessionLocal()
    try:
        create_tables(db)
        add_paths(db)
        modules = add_modules(db)

        m1 = db.query(Module).filter(Module.key == "m1_intro").first()
        m2 = db.query(Module).filter(Module.key == "m2_terminal").first()
        lessons1 = module1_lessons(db, m1)
        module1_objectives_examples(db, lessons1)
        module1_case_studies_and_labs(db, m1, lessons1)

        lessons2 = module2_lessons(db, m2)
        module2_objectives_examples(db, lessons2)
        module2_labs_and_case_studies(db, m2, lessons2)

        all_lessons = {**lessons1, **lessons2}
        add_assignments_and_questions(db, all_lessons)
        add_cheat_sheets(db)
        add_achievements(db)
        add_demo_user(db)

        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
