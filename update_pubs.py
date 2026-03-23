import bibtexparser
import re
import html

def clean_latex(text):
    if not text: return ""
    # 1. Unescape HTML (fixes &amp; -> &)
    text = html.unescape(text)
    # 2. Fix LaTeX escapes (fixes \& -> &)
    replacements = {
        r'\\&': '&',
        r'\{&\}': '&',
        r'\\_': '_',
        r'\\textless': '<',
        r'\\textgreater': '>',
        r'\\dots': '...',
        r'---': '—',
        r'--': '–',
        '{': '',
        '}': '',
        r'\\': '',
    }
    for latex, plain in replacements.items():
        text = text.replace(latex, plain)
    # 3. Strip any remaining backslashes from single characters
    text = re.sub(r'\\([a-zA-Z])', r'\1', text)
    return text.strip()

def generate_html():
    # ENSURE FILE NAME MATCHES: This script looks for 'publications.bib'
    try:
        with open('publications.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
    except Exception as e:
        print(f"Error: Could not find or read 'publications.bib'. Details: {e}")
        return

    # Deduplicate by Title (case-insensitive)
    seen_titles = set()
    unique_entries = []
    for entry in bib_database.entries:
        title = entry.get('title', '').lower().strip()
        if title not in seen_titles and title != "":
            seen_titles.add(title)
            unique_entries.append(entry)

    # Sort by year descending
    entries = sorted(unique_entries, key=lambda x: x.get('year', '0'), reverse=True)

    # Build the HTML block
    html_output = '<ul class="divide-y divide-slate-800">\n'
    for entry in entries:
        title = clean_latex(entry.get('title', 'Unknown Title'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', 'Journal/Patent')))
        year = entry.get('year', 'N/A')
        opacity = "opacity-100" if year == "2025" else "opacity-70" if year == "2024" else "opacity-50"

        html_output += f"""        <li class="p-6 flex gap-4 hover:bg-white/5 transition">
          <span class="year-badge self-start {opacity} font-bold text-xs py-1 px-3 rounded-full bg-sky-400/10 text-sky-400 border border-sky-400/20">{year}</span>
          <div>
            <p class="text-white font-medium mb-1">{title}</p>
            <p class="text-slate-500 text-sm italic">{journal}</p>
          </div>
        </li>\n"""
    html_output += '      </ul>'

    # Inject into HTML
    with open('publications.html', 'r') as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    # regex: count=1 ensures we ONLY replace the first pair, stopping the duplication loop.
    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    
    if start_marker in content:
        new_content = pattern.sub(f"{start_marker}\n{html_output}\n{end_marker}", content, count=1)
        with open('publications.html', 'w') as f:
            f.write(new_content)
        print("Success: publications.html updated once.")
    else:
        print("Error: Markers not found. Ensure exists.")

if __name__ == "__main__":
    generate_html()
