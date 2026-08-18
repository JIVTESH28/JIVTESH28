#!/usr/bin/env python3
"""Fetch docarmor PyPI download stats and update README.md with live badges."""

import json
import re
import urllib.request
from datetime import datetime, timezone, timedelta


def fetch_pypistats():
    """Fetch download stats from pypistats.org API."""
    url = "https://pypistats.org/api/packages/docarmor/recent"
    req = urllib.request.Request(url, headers={"User-Agent": "docarmor-readme-bot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return {
                "last_day": data["data"]["last_day"],
                "last_week": data["data"]["last_week"],
                "last_month": data["data"]["last_month"],
            }
    except Exception as e:
        print(f"Warning: pypistats API failed: {e}")
        return None


def fetch_pepy_total():
    """Fetch total download count from pepy.tech HTML (no API key needed)."""
    url = "https://pepy.tech/projects/docarmor"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode()
            # Extract from meta title: "docarmor · 863 downloads on PyPI"
            match = re.search(r'docarmor\s*·\s*([\d,]+)\s*downloads', html)
            if match:
                return int(match.group(1).replace(",", ""))
    except Exception as e:
        print(f"Warning: pepy.tech fetch failed: {e}")
    return None


def format_number(n):
    """Format number with comma separators."""
    if n is None:
        return "N/A"
    return f"{n:,}"


def build_stats_section(pypistats, total_downloads):
    """Build the markdown stats section."""
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist).strftime("%B %d, %Y at %I:%M %p IST")

    last_day = format_number(pypistats["last_day"]) if pypistats else "N/A"
    last_week = format_number(pypistats["last_week"]) if pypistats else "N/A"
    last_month = format_number(pypistats["last_month"]) if pypistats else "N/A"
    total = format_number(total_downloads)

    # URL-encoded badge values
    b_total = total.replace(",", "%2C")
    b_month = last_month.replace(",", "%2C")
    b_week = last_week.replace(",", "%2C")
    b_day = last_day.replace(",", "%2C")

    section = f"""## 📦 DocArmor — Live PyPI Stats

<div align="center">

<a href="https://pypi.org/project/docarmor/">
  <img src="https://img.shields.io/pypi/v/docarmor?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI&color=3775A9" alt="PyPI Version"/>
</a>
<a href="https://pepy.tech/projects/docarmor">
  <img src="https://img.shields.io/badge/Total%20Downloads-{b_total}-00C853?style=for-the-badge&logo=python&logoColor=white" alt="Total Downloads"/>
</a>
<a href="https://pypistats.org/packages/docarmor">
  <img src="https://img.shields.io/badge/Monthly-{b_month}-FF6D00?style=for-the-badge&logo=download&logoColor=white" alt="Monthly Downloads"/>
</a>
<a href="https://pypistats.org/packages/docarmor">
  <img src="https://img.shields.io/badge/Weekly-{b_week}-AA00FF?style=for-the-badge&logo=download&logoColor=white" alt="Weekly Downloads"/>
</a>
<a href="https://pypistats.org/packages/docarmor">
  <img src="https://img.shields.io/badge/Daily-{b_day}-2979FF?style=for-the-badge&logo=download&logoColor=white" alt="Daily Downloads"/>
</a>

</div>

<div align="center">

| 📊 Metric | 📈 Count |
|:---:|:---:|
| 🏆 **All-Time Downloads** | **{total}** |
| 📅 **Last 30 Days** | **{last_month}** |
| 📆 **Last 7 Days** | **{last_week}** |
| 🕐 **Last 24 Hours** | **{last_day}** |

<sub>🤖 Auto-updated on {now} via GitHub Actions</sub>

</div>

<div align="center">
  <a href="https://github.com/JIVTESH28/docarmor"><img src="https://img.shields.io/badge/GitHub-Source_Code-181717?style=for-the-badge&logo=github" alt="GitHub"/></a>
  <a href="https://pypi.org/project/docarmor/"><img src="https://img.shields.io/badge/Install-pip_install_docarmor-3775A9?style=for-the-badge&logo=pypi&logoColor=white" alt="Install"/></a>
  <a href="https://pepy.tech/projects/docarmor"><img src="https://img.shields.io/badge/Analytics-pepy.tech-00C853?style=for-the-badge&logo=python&logoColor=white" alt="Analytics"/></a>
</div>"""

    return section


def main():
    print("🔄 Fetching docarmor download stats...")

    pypistats = fetch_pypistats()
    if pypistats:
        print(f"  ✅ PyPI Stats: day={pypistats['last_day']}, week={pypistats['last_week']}, month={pypistats['last_month']}")
    else:
        print("  ⚠️ PyPI Stats unavailable")

    total = fetch_pepy_total()
    if total:
        print(f"  ✅ Total downloads: {total}")
    else:
        print("  ⚠️ Total downloads unavailable")

    stats_section = build_stats_section(pypistats, total)

    # Read current README
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace between markers, or append if markers don't exist
    start_marker = "<!-- DOCARMOR-STATS:START -->"
    end_marker = "<!-- DOCARMOR-STATS:END -->"

    new_block = f"{start_marker}\n{stats_section}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        content = pattern.sub(new_block, content)
        print("  ✅ Updated existing stats section")
    else:
        # Find a good place to insert — before Tech Arsenal section or at end
        insert_patterns = [
            r"(## .*Tech Arsenal)",
            r"(## .*Current Missions)",
        ]
        inserted = False
        for pat in insert_patterns:
            match = re.search(pat, content)
            if match:
                insert_pos = match.start()
                content = content[:insert_pos] + new_block + "\n\n" + content[insert_pos:]
                inserted = True
                print(f"  ✅ Inserted stats section before '{match.group(1)}'")
                break
        if not inserted:
            # Insert after the About Me closing table tag
            table_end = content.rfind("</table>")
            if table_end != -1:
                insert_pos = table_end + len("</table>")
                content = content[:insert_pos] + "\n\n" + new_block + "\n" + content[insert_pos:]
                print("  ✅ Inserted stats section after About Me table")
            else:
                content += "\n\n" + new_block + "\n"
                print("  ✅ Appended stats section at end")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("\n🎉 README.md updated successfully!")


if __name__ == "__main__":
    main()
