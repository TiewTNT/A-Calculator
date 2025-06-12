from flask import Flask, request, render_template
from sympy.parsing.latex import parse_latex as sympy_parse_latex
from sympy import pi, E, I, Symbol
import sympy
import random
import os

app = Flask(__name__)

substitutions = {
        Symbol('pi'): pi,
        Symbol('e'): E,
        Symbol('imaginaryI'): I
    }

def parse_latex(latex):
    return sympy_parse_latex(latex).subs(substitutions)

@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/', methods=['GET','POST'])
def index():
    math_latex = request.form.get('math')
    print(f"Received LaTeX: {math_latex}")
    if random.randint(0, 99) or not math_latex:
        num = False

        if math_latex != None:
            try:
                if math_latex.startswith('N;'):
                    num = True
                    math_latex = math_latex[2:]

                lines = math_latex.split(';')
                print(lines)
                print(len(lines))
                eqs = []
                neqs = []
                for m in lines:
                    print(m, 'm')
                    if isinstance(l := parse_latex(m), sympy.Eq):
                        eqs.append(sympy.N(l) if num else l)
                    else:
                        neqs.append(m)
                print(eqs)
                print(neqs)

                output_raw = sympy.solve(eqs)
                if eqs != []:
                    output = sympy.latex(output_raw)
                else:
                    output = ''
                    
                for n in neqs:
                    n2 = sympy.simplify(parse_latex(n).doit())
                    print(parse_latex(n))
                    print(n2, 'n2')
                    if num:
                        try:
                            n2 = sympy.N(n2)
                        except AttributeError:
                            n2 = n2
                    n2 = sympy.latex(n2)

                    if ';' in math_latex:
                        if '=' in n:
                            output = output + r' \\'+str(n) + r'\text{ is }' + str(n2)
                        else:
                            output = output + r' \\'+str(n) + '=' + str(n2)
                    else:
                        output = n2
                print(output)
            except Exception as e:
                output = r'\text{There was an error. ('+str(e)+r') Check your input: }' + str(math_latex)
                print(e)
        else:
            output = ''

        return render_template('index.html', output=output, input=(('N;'+math_latex) if num else math_latex) if math_latex != None else '')
    else:
        with open('./random_messages.txt', 'r') as f:
            random_list = [p.strip() for p in f.readlines() if p.strip()]
        output = random.choice(random_list)
        return render_template('random_text.html', output=output)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
