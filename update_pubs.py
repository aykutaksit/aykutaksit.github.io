import bibtexparser
import html
import re

def clean_latex(text):
    if not text: return ""
    text = html.unescape(text)
    replacements = {
        r'\\&': '&', r'\{&\}': '&', r'\\_': '_', r'\\textless': '<',
        r'\\textgreater': '>', r'\\dots': '...', r'---': '—', r'--': '–',
        '{': '', '}': '', r'\\': '',
    }
    for latex, plain in replacements.items():
        text = text.replace(latex, plain)
    text = re.sub(r'\\([a-zA-Z])', r'\1', text)
    return text.strip()

def generate_html():
    try:
        with open('publications.bib', 'r', encoding='utf-8') as f:
            bib_database = bibtexparser.load(f)
    except Exception as e:
        print("Error reading bib file:", e)
        return

    # Deduplicate by Title
    seen_titles = set()
    unique_entries = []
    for entry in bib_database.entries:
        title = entry.get('title', '').lower().strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_entries.append(entry)

    # Sort descending
    entries = sorted(unique_entries, key=lambda x: str(x.get('year', '0')), reverse=True)

    # Build the HTML list
    html_output = '<ul class="divide-y divide-slate-800">\n'
    for entry in entries:
        title = clean_latex(entry.get('title', 'Unknown Title'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', 'Journal/Patent')))
        year = str(entry.get('year', 'N/A'))
        opacity = "opacity-100" if year == "2025" else "opacity-70" if year == "2024" else "opacity-50"

        html_output += f'''        <li class="p-6 flex gap-4 hover:bg-white/5 transition">
          <span class="year-badge self-start {opacity} font-bold text-xs py-1 px-3 rounded-full bg-sky-400/10 text-sky-400 border border-sky-400/20">{year}</span>
          <div>
            <p class="text-white font-medium mb-1">{title}</p>
            <p class="text-slate-500 text-sm italic">{journal}</p>
          </div>
        </li>\n'''
    html_output += '      </ul>'

    # Read the pristine template
    try:
        with open('publications_template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        print("Error reading template:", e)
        return

    # Swap the placeholder and save the final file
    final_html = template_content.replace('{{PUBLICATION_LIST_HERE}}', html_output)

    with open('publications.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Success: Generated a clean publications.html from the template.")

if __name__ == "__main__":
    generate_html()
