import bibtexparser
import re

def clean_latex(text):
    # Fixes the "abc notation" and LaTeX escapes
    replacements = {
        '\\&': '&',
        '\\_': '_',
        '{': '',
        '}': '',
        '\\textless': '<',
        '\\textgreater': '>',
        '\\\'e': 'é',
        '\\\"u': 'ü',
    }
    for latex, plain in replacements.items():
        text = text.replace(latex, plain)
    return text

def generate_html():
    with open('publications.bib') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    # Sort by year descending
    entries = sorted(bib_database.entries, key=lambda x: x.get('year', '0'), reverse=True)

    html_output = '<ul class="divide-y divide-slate-800">'
    
    for entry in entries:
        title = clean_latex(entry.get('title', 'Unknown Title'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', '')))
        year = entry.get('year', 'N/A')
        
        # Determine opacity based on recency
        opacity = "opacity-100" if year == "2025" else "opacity-70" if year == "2024" else "opacity-50"

        html_output += f"""
        <li class="p-6 flex gap-4 border-b border-slate-800/50 hover:bg-white/5 transition">
          <span class="year-badge self-start {opacity} font-bold text-xs py-1 px-3 rounded-full bg-sky-400/10 text-sky-400 border border-sky-400/20">{year}</span>
          <div>
            <p class="text-white font-medium mb-1">{title}</p>
            <p class="text-slate-500 text-sm italic">{journal}</p>
          </div>
        </li>"""
    
    html_output += '</ul>'

    # Inject into publications.html
    with open('publications.html', 'r') as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    new_content = pattern.sub(f"{start_marker}\n{html_output}\n{end_marker}", content)

    with open('publications.html', 'w') as f:
        f.write(new_content)

if __name__ == "__main__":
    generate_html()
