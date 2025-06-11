from flask import Flask, request, render_template
from sympy.parsing.latex import parse_latex as sympy_parse_latex
from sympy import pi, E, oo, Symbol

import sympy
import random

app = Flask(__name__)

substitutions = {
        Symbol('pi'): pi,
        Symbol('e'): E,
        Symbol('oo'): oo
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

                if ';' not in math_latex:
                    if isinstance(a := sympy.simplify(parse_latex(math_latex).doit()), sympy.Eq):
                        output = sympy.latex(sympy.solve(a))
                    else:
                        output = sympy.latex(a) if not num else sympy.latex(sympy.N(a))
                    print('huh.')
                    print(a)
                else:
                    lines = math_latex.split(';')
                    print(lines)
                    print(len(lines))
                    eqs = []
                    neqs = []
                    for m in lines:
                        print(m)
                        if isinstance(l := parse_latex(m), sympy.Eq):
                            eqs.append(l)
                        else:
                            neqs.append(m)
                    print(eqs)
                    print(neqs)

                    output = sympy.latex(sympy.solve(eqs))
                    for n in neqs:
                        n2 = sympy.latex(sympy.simplify(parse_latex(n).doit()))
                        if '=' in n:
                            output = output + r' \\'+str(n) + r'\text{ is }' + str(n2)
                        else:
                            output = output + r' \\'+str(n) + '=' + str(n2)
                    print(output)
            except Exception as e:
                output = r'\text{There was an error. Check your input: }' + str(math_latex)
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
    app.run(debug=True)
