#!/usr/bin/env python3
import requests
import yaml
from collections import defaultdict
from pathlib import Path

# Source YAML file
RAW_URL = "https://raw.githubusercontent.com/wega-team/ss14-wega/master/Resources/Changelog/ChangelogAWega.yml"
OUTPUT_FILE = "src/changelog.md"

HEADER = """# Ченджлог

История изменений и добавлений в сборке.

---

"""

# Emoji per change type
TYPES_TO_EMOJI = {
    "Add": "✨",
    "Fix": "🐛",
    "Tweak": "⚒️",
    "Remove": "❌",
}

def main():
    resp = requests.get(RAW_URL)
    resp.raise_for_status()
    data = yaml.safe_load(resp.text)

    entries_by_date = defaultdict(list)
    for entry in data.get("Entries", []):
        # Extract date (YYYY-MM-DD)
        date_str = entry["time"].split("T")[0].split(" ")[0]
        entries_by_date[date_str].append(entry)

    # Sort dates descending (newest first)
    sorted_dates = sorted(entries_by_date.keys(), reverse=True)

    md_blocks = []
    for date in sorted_dates:
        entries = entries_by_date[date]
        
        urls = []
        for e in entries:
            url = e.get("url")
            if url and url not in urls:
                urls.append(url)
        
        block = f'<details class="admonition admonish-changelog">\n'
        block += f'  <summary class="admonition-title"><p>📅 {date} - Обновления</p></summary>\n\n'
        
        if urls:
            block += '  <div class="changelog-meta">\n'
            for url in urls:
                block += f'     🔗 {url}\n'
            block += '  </div>\n\n'

        block += '   <details class="changelog-changes">\n'
        block += '    <summary>Развернуть</summary>\n'
        block += '    <ul>\n'
        
        for entry in entries:
            for change in entry["changes"]:
                emoji = TYPES_TO_EMOJI.get(change["type"], "")
                prefix = f"{emoji} " if emoji else ""
                block += f'      <li> {prefix}{change["message"]} </li>\n'
                
        block += '    </ul>\n'
        block += '  </details>\n'
        block += '</details>\n\n---\n\n'
        md_blocks.append(block)

    final_content = HEADER + "".join(md_blocks)

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(final_content)

if __name__ == "__main__":
    main()
  
