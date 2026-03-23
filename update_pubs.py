import bibtexparser
import re
import html

def clean_latex(text):
    if not text: return ""
    # Standardize HTML entities first
    text = html.unescape(text)
    # Common LaTeX to Plain Text mapping
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
    # Remove any lingering backslashes before characters
    text = re.sub(r'\\([a-zA-Z])', r'\1', text)
    return text.strip()

def generate_html():
    try:
        with open('publications.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
    except Exception as e:
        print(f"Error reading .bib file: {e}")
        return

    # Deduplicate by Title
    seen_titles = set()
    unique_entries = []
    for entry in bib_database.entries:
        title = entry.get('title', '').lower().strip()
        if title not in seen_titles and title != "":
            seen_titles.add(title)
            unique_entries.append(entry)

    # Sort by year descending
    entries = sorted(unique_entries, key=lambda x: x.get('year', '0'), reverse=True)

    # Start the list
    html_output = '<ul class="divide-y divide-slate-800">\n'
    
    for entry in entries:
        title = clean_latex(entry.get('title', 'Unknown Title'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', 'Journal/Patent')))
        year = entry.get('year', 'N/A')
        
        # Recency Styling
        opacity = "opacity-100" if year == "2025" else "opacity-70" if year == "2024" else "opacity-50"

        html_output += f"""        <li class="p-6 flex gap-4 hover:bg-white/5 transition">
          <span class="year-badge self-start {opacity} font-bold text-xs py-1 px-3 rounded-full bg-sky-400/10 text-sky-400 border border-sky-400/20">{year}</span>
          <div>
            <p class="text-white font-medium mb-1">{title}</p>
            <p class="text-slate-500 text-sm italic">{journal}</p>
          </div>
        </li>\n"""
    
    html_output += '      </ul>'

    # Read current publications.html
    with open('publications.html', 'r') as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    # Surgical replacement: Finds everything between the FIRST start and the LAST end
    # to prevent duplication if markers were accidentally doubled.
    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    
    if start_marker in content:
        new_content = pattern.sub(f"{start_marker}\n{html_output}\n{end_marker}", content)
        with open('publications.html', 'w') as f:
            f.write(new_content)
        print("Publications updated successfully.")
    else:
        print("Error: Markers not found in publications.html")

if __name__ == "__main__":
    generate_html()
