import bibtexparser
import html
import re

def clean_latex(text):
    if not text: return ""
    text = html.unescape(text)
    replacements = {
        r'\\&': '&', r'\{&\}': '&', r'\\_': '_', r'\\textless': '<',
        r'\\textgreater': '>', r'\\dots': '...', r'---': '—', r'--': '–',
        '{': '', '}': '', r'\\': '', '\n': ' '
    }
    for latex, plain in replacements.items():
        text = text.replace(latex, plain)
    text = re.sub(r'\\([a-zA-Z])', r'\1', text)
    return text.strip()

def format_authors(author_string):
    if not author_string: return ""
    # Swap BibTeX's "and" for a standard comma
    authors = author_string.replace(' and ', ', ')
    # Highlight your last name so it stands out in the list
    authors = re.sub(r'(Aksit)', r'<span class="text-slate-200 font-semibold">\1</span>', authors)
    return authors

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

    # Build the HTML list with High-Density layout
    html_output = '<ul class="divide-y divide-slate-800/50">\n'
    for entry in entries:
        title = clean_latex(entry.get('title', 'Unknown Title'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', 'Journal / Patent')))
        raw_authors = clean_latex(entry.get('author', ''))
        authors = format_authors(raw_authors)
        year = str(entry.get('year', 'N/A'))
        
        opacity = "opacity-100" if year == "2025" else "opacity-80" if year == "2024" else "opacity-60"

        # Tighter padding (py-4 px-5) and smaller text (text-sm, text-xs)
        html_output += f'''        <li class="py-4 px-5 flex flex-col sm:flex-row gap-3 hover:bg-white/5 transition">
          <div class="flex-shrink-0 pt-0.5">
            <span class="year-badge {opacity} font-bold text-[0.65rem] py-1 px-2.5 rounded-full bg-sky-400/10 text-sky-400 border border-sky-400/20">{year}</span>
          </div>
          <div>
            <p class="text-slate-200 font-medium text-sm leading-snug mb-1">{title}</p>
            <p class="text-slate-400 text-xs mb-1">{authors}</p>
            <p class="text-sky-400/70 text-xs italic">{journal}</p>
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
        
    print("Success: Generated high-density publications.html with authors.")

if __name__ == "__main__":
    generate_html()
