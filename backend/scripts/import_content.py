"""
Import the authored lesson HTML files from C:\\Data\\node\\linotutor\\content
into the application database as 25 numbered chapters grouped into 5 stages.

Replaces the previously hand-authored module/lesson rows. Keeps learning paths,
cheat sheets, achievements, and users intact. Wipes lesson-related progress rows
(their lesson ids no longer exist).
"""
import json
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import SessionLocal  # noqa: E402
from app.models.curriculum import (  # noqa: E402
    Assignment,
    Lab,
    LabScenario,
    Lesson,
    Module,
    Question,
)
from app.models.progress import AssessmentAttempt, LabAttempt, UserProgress, Bookmark  # noqa: E402

CONTENT_DIR = r"C:\Data\node\linotutor\content"

STAGE_PATHS = {1: "beginner", 2: "administrator", 3: "devops", 4: "advanced", 5: "troubleshooter"}

STAGE_TITLES = {
    1: "Stage 1 — Linux Foundations",
    2: "Stage 2 — Linux Administration",
    3: "Stage 3 — Linux for DevOps",
    4: "Stage 4 — Advanced Linux Engineering",
    5: "Stage 5 — Production Capstone",
}

# (source_file, chapter_no, stage, title, summary, difficulty, minutes)
CHAPTERS = [
    ("1.html",  1, 1, "Introduction to Linux and DevOps",
     "What Linux is and why DevOps engineers use it. Kernel, shell, terminal, distributions, and your first five commands.",
     "beginner", 25),
    ("2.html",  2, 1, "Understanding the Linux Filesystem",
     "The filesystem tree, the directories every DevOps engineer should know, and absolute vs relative paths.",
     "beginner", 25),
    ("3.html",  3, 1, "Create, Copy, Move, and Delete Files",
     "mkdir, touch, cp, mv, and rm through a simulated project directory and a practical deployment exercise.",
     "beginner", 25),
    # 4.html is a duplicate re-export of chapter 3 and is intentionally skipped
    ("5.html",  4, 1, "Reading and Editing Files",
     "cat, less, head, tail, nano, and grep for reading configuration files and searching logs.",
     "beginner", 30),
    ("6.html",  5, 2, "Permissions and Ownership",
     "chmod, chown, chgrp, and umask — numeric permissions, the permission calculator, and fixing Permission denied.",
     "beginner", 30),
    ("7.html",  6, 2, "Users, Groups, and sudo",
     "whoami, getent, useradd, usermod, passwd, and using sudo safely.",
     "beginner", 25),
    ("8.html",  7, 2, "Processes and Jobs",
     "ps, top, pgrep, kill and signals, foreground vs background jobs, bg/fg, and nohup.",
     "intermediate", 30),
    ("9.html",  8, 2, "Networking Fundamentals",
     "ip, ping, curl, ss, DNS, hostname configuration, and diagnosing connection refused.",
     "intermediate", 30),
    ("10.html", 9, 2, "Package Management with apt",
     "The apt workflow, safe updates, repositories, dependencies, and installing DevOps tools.",
     "beginner", 25),
    ("11.html", 10, 2, "Services and systemd",
     "systemctl start/stop/enable, journalctl, failure states, unit files, and diagnosing startup failures.",
     "intermediate", 30),
    ("12.html", 11, 2, "Logging and Log Analysis",
     "/var/log, less/tail/grep on logs, journalctl, log rotation, and checking disk before logs fill it.",
     "intermediate", 30),
    ("13.html", 12, 2, "Disk Management and Storage Troubleshooting",
     "lsblk, df, du, filesystems, mount points, fstab, and inodes vs free space.",
     "intermediate", 30),
    ("14.html", 13, 2, "SSH and Secure Remote Access",
     "First SSH connection, host keys, public-key authentication, scp, ssh config, and SSH troubleshooting.",
     "intermediate", 30),
    ("15.html", 14, 2, "System Monitoring and Resource Management",
     "Quick health checks, CPU, load average, memory with free, vmstat, iostat, and resource-heavy processes.",
     "intermediate", 30),
    ("16.html", 15, 3, "Bash Scripting Fundamentals",
     "First script, shell variables, quoting, command substitution, exit codes, if/elif/else, loops, and functions.",
     "intermediate", 40),
    ("17.html", 16, 3, "Cron Jobs and Scheduled Automation",
     "Cron syntax, common schedules, crontabs, environment differences, flock, and troubleshooting cron.",
     "intermediate", 30),
    ("18.html", 17, 3, "Environment Variables, Configuration and Secrets",
     "Exported variables, PATH, config file locations, .env patterns, secrets handling, cron and systemd config.",
     "intermediate", 30),
    ("22.html", 18, 3, "Git Essentials on Linux",
     "Repositories, commits, the typical Git workflow, undoing mistakes, branches, and remotes.",
     "beginner", 25),
    ("23.html", 19, 3, "Containers and Docker Foundations",
     "Containers vs VMs, installing Docker, your first container, managing and inspecting containers, images.",
     "intermediate", 25),
    ("24.html", 20, 3, "Web Servers (Nginx)",
     "Install Nginx, serve a static site, manage the service, reverse proxy basics, UFW access, and 404 debugging.",
     "intermediate", 25),
    ("19.html", 21, 4, "Security Fundamentals and Hardening",
     "Least privilege, protecting files and secrets, SSH hardening, UFW firewall, updates, and auth monitoring.",
     "advanced", 35),
    ("20.html", 22, 4, "Troubleshooting Linux Servers Systematically",
     "The troubleshooting mindset, incident triage workflow, and service, network, resource, disk, permission checks.",
     "advanced", 35),
    ("21.html", 23, 4, "Advanced Bash Automation and Production Scripts",
     "Exit codes, set -Eeuo pipefail, arguments, logging, traps, temp files, idempotency, flock, cron and systemd.",
     "advanced", 40),
    ("25.html", 24, 4, "Kernel, Boot Process and Troubleshooting",
     "Boot process, kernel and versions, systemd as init, boot logs, GRUB, boot targets, unbootable systems.",
     "advanced", 30),
    ("26.html", 25, 5, "Production Capstone: Incident Response",
     "Investigate a broken application, triage workflows, step-by-step root-cause analysis, restore service.",
     "advanced", 45),
]

slugify_re = re.compile(r"[^a-z0-9]+")

def kebab(title: str) -> str:
    return slugify_re.sub("-", title.lower()).strip("-")[:60]

# Paragraph text (after strip) that is interactive-widget debris to remove
JUNK = (
    re.compile(r"^\d+( of \d+)+$"),
    re.compile(r"^\d+/\d+$"),
    re.compile(r"^\d+(\.\d+)?%$"),
    re.compile(r"^0\s*/\s*\d+$"),
    re.compile(r"^(Next| Previous|Prev|Submit|Start Lesson \d+|Copy command reference)$"),
    re.compile(r"^Assignment progress$"),
    re.compile(r"^Your progress$"),
    re.compile(r"^Progress tracker$"),
    re.compile(r"^Lab progress$"),
    re.compile(r"^Hands-on checklist$"),
)

def clean_html(body_html: str) -> str:
    soup = BeautifulSoup(body_html, "html.parser")

    # drop any script/style leftovers
    for t in soup.find_all(["script", "style"]):
        t.decompose()

    # remove standalone image-citation / external link paragraphs
    for p in soup.find_all("p"):
        links = p.find_all("a")
        if links and len(str(p).replace(str(NavigableString("")), "").split("<a")) <= 2:
            texts = [a.get_text(strip=True) for a in links]
            joined = p.get_text(strip=True)
            hrefs = " ".join(a.get("href", "") for a in links)
            # paragraph is essentially just link(s): citation debris
            if joined and (joined.replace(" ", "") == "".join(texts).replace(" ", "")):
                if "images.openai.com" in hrefs or "utm_source=chatgpt.com" in hrefs or "images." in hrefs:
                    p.decompose()
                    continue
        text = p.get_text(" ", strip=True)
        if text and any(j.match(text) for j in JUNK):
            p.decompose()

    # remove empty paragraphs
    for p in soup.find_all("p"):
        if not p.get_text(strip=True) and not p.find(["img", "code", "pre"]):
            p.decompose()

    # strip all external <a> wrappers around citations, keep text
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.startswith("http"):
            # keep the visible text but drop hyperlink behaviour for citations
            a.replace_with(a.get_text())

    return str(soup)

def extract_container_html(path: str) -> str:
    raw = open(path, encoding="utf-8", errors="replace").read()
    start = raw.find('<div class="export-container"')
    if start == -1:
        start = raw.find("<h2")
    body = raw[start:] if start != -1 else raw
    return clean_html(body)

def main():
    session = SessionLocal()
    try:
        # ---- wipe lesson-cascade data ----
        for tbl in (Question, Assignment, LabScenario, Lab):
            tbl_rows = session.query(tbl).delete(synchronize_session=False)
            print(f"cleared {tbl_rows} rows from {tbl.__tablename__}")
        for tbl in (UserProgress, AssessmentAttempt, Bookmark, LabAttempt):
            rows = session.query(tbl).delete(synchronize_session=False)
            print(f"cleared {rows} rows from {tbl.__tablename__}")

        lesson_rows = session.query(Lesson).delete(synchronize_session=False)
        print(f"cleared {lesson_rows} old lessons")
        modules_deleted = session.query(Module).delete(synchronize_session=False)
        print(f"cleared {modules_deleted} old modules")

        from app.models.curriculum import LearningPath
        paths = {p.key: p for p in session.query(LearningPath).all()}

        created_modules = 0
        created_lessons = 0
        for chapter in CHAPTERS:
            src, no, stage, title, summary, diff, minutes = chapter
            path_src = os.path.join(CONTENT_DIR, src)
            if not os.path.exists(path_src):
                print(f"!! missing source file: {path_src}")
                continue
            html = extract_container_html(path_src)
            slug = f"ch{no:02d}-{kebab(title)}"

            path_key = STAGE_PATHS[stage]
            module = Module(
                key=f"chapter-{no:02d}",
                title=f"Chapter {no}: {title}",
                description=STAGE_TITLES[stage],
                stage=str(stage),
                order=no,
                estimated_hours=max(1, minutes // 60),
                prerequisites=json.dumps([f"chapter-{no-1:02d}"] if no > 1 else []),
                is_active=True,
                path_id=path_key in paths and paths[path_key].id or None,
            )
            lesson = Lesson(
                module=module,
                key=f"ch{no:02d}",
                title=title,
                slug=slug,
                order=1,
                difficulty=diff,
                estimated_minutes=minutes,
                summary=summary,
                content=json.dumps({
                    "sections": [{"type": "html", "title": title, "content": html}]
                }),
                prerequisites=None,
                has_lab=False,
                has_quiz=False,
                completion_criteria=json.dumps({"read": True}),
                is_active=True,
            )
            session.add(module)
            session.add(lesson)
            created_modules += 1
            created_lessons += 1
            print(f"chapter {no:2d}: {title:55s} -> {slug} ({len(html)//1024} KB html)")

        session.commit()
        print(f"\nDone. Created {created_modules} modules, {created_lessons} lessons.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
