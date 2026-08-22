import sys
import re
import argparse

def fix_trig_shorthands(text):
    """
    Replaces physics package trig shorthands like \cos[2](\theta) 
    with standard LaTeX \cos^2(\theta).
    """
    # Matches \sin, \cos, \tan, \csc, \sec, \cot, \sinh, \cosh, \tanh
    trig_pattern = r'\\(sin|cos|tan|csc|sec|cot|sinh|cosh|tanh)\[(.*?)\]'
    # Replaces with \sin^{2} (standard LaTeX)
    return re.sub(trig_pattern, r'\\\1^{\2}', text)

def fix_mqty_matrices(text):
    """
    Parses and replaces \mqty(...) with \begin{pmatrix}...\end{pmatrix}.
    Uses depth-tracking to perfectly handle nested parentheses inside the matrix.
    """
    # Map opening delimiters to their LaTeX environments and closing delimiters
    delimiters = {
        '(': ('pmatrix', ')'),
        '[': ('bmatrix', ']'),
        '{': ('Bmatrix', '}'),
        '|': ('vmatrix', '|')
    }
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        # Check if we've hit an \mqty macro
        if text[i:i+5] == '\\mqty':
            j = i + 5
            
            # Skip any spaces between \mqty and the delimiter
            while j < length and text[j].isspace():
                j += 1
                
            if j < length and text[j] in delimiters:
                open_delim = text[j]
                env_name, close_delim = delimiters[open_delim]
                
                # Start tracking depth to handle nested brackets/parentheses
                depth = 1
                k = j + 1
                inner_content = []
                
                while k < length and depth > 0:
                    char = text[k]
                    
                    # | is a special case since it is both an opening and closing bracket
                    if open_delim == '|' and char == '|':
                        depth -= 1
                    else:
                        if char == open_delim:
                            depth += 1
                        elif char == close_delim:
                            depth -= 1
                            
                    if depth > 0:
                        inner_content.append(char)
                    k += 1
                
                # If we successfully found the matching closing delimiter
                if depth == 0:
                    matrix_content = "".join(inner_content)
                    result.append(f"\\begin{{{env_name}}}{matrix_content}\\end{{{env_name}}}")
                    i = k
                    continue
                    
        # If no match or we are just reading normal text, append the character
        result.append(text[i])
        i += 1
        
    return "".join(result)

def process_tex_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"Processing '{input_path}'...")
        
        # Apply the fixes
        content = fix_trig_shorthands(content)
        content = fix_mqty_matrices(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Success! Cleaned TeX file saved to '{output_path}'.")
        
    except FileNotFoundError:
        print(f"Error: Could not find the file '{input_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Physics package macros to standard LaTeX for MathJax compatibility.")
    parser.add_argument("input", help="Path to the input .tex file")
    parser.add_argument("-o", "--output", help="Path to save the output .tex file (defaults to input_cleaned.tex)", default=None)
    
    args = parser.parse_args()
    
    out_path = args.output if args.output else args.input.replace(".tex", "_cleaned.tex")
    
    process_tex_file(args.input, out_path)
