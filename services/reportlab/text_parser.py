"""
Text parser for structured PDF content.

Parses multi-line section texts into hierarchical components
for proper ReportLab rendering.
"""
import re

class TextParser:
    """Parses structured text into hierarchical components."""
    
    @staticmethod
    def parse_section(text):
        """
        Parses section text into structured components.
        
        Args:
            text (str): Multi-line section text with hierarchy
        
        Returns:
            list of dicts: [
                {'type': 'main_title', 'text': '1. INVESTIGACIÓN'},
                {'type': 'paragraph', 'text': 'Sólo artículos...'},
                {'type': 'subsection', 'text': '1.1 Publicaciones...'},
                {'type': 'subsubsection', 'text': '    2.1.1 Doctorado'},
                ...
            ]
        
        Component types:
            - main_title: Main section (1., 2., 3., etc.)
            - subsection: Subsection (1.1, 1.2, 2.1, etc.)
            - subsubsection: Sub-subsection (2.1.1, 2.1.2, etc.)
            - paragraph: Normal text paragraph
        """
        lines = text.strip().split('\n')
        components = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Main title: "1. Investigación" or "2. Docencia" (capitalized, not all caps)
            # Pattern: digit(s) + dot + space + text starting with uppercase
            if re.match(r'^\d+\.\s+[A-ZÁÉÍÓÚÑ]', stripped):
                components.append({'type': 'main_title', 'text': stripped})
            
            # Sub-subsection: "2.1.1 Text" or indented "    2.1.1 Text"
            # Pattern: optional spaces + digit.digit.digit + space + text
            elif re.match(r'^\s*\d+\.\d+\.\d+\s+', line):
                components.append({'type': 'subsubsection', 'text': stripped})
            
            # Subsection: "1.1 Text" or "2.3 Text"
            # Pattern: digit.digit + space + text
            elif re.match(r'^\d+\.\d+\s+', stripped):
                components.append({'type': 'subsection', 'text': stripped})
            
            # Normal paragraph (everything else)
            else:
                components.append({'type': 'paragraph', 'text': stripped})
        
        return components