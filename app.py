from flask import Flask, request, render_template
from sympy.parsing.latex import parse_latex as sympy_parse_latex
from sympy import pi, E, oo, I, Symbol

import sympy
import random
import os

app = Flask(__name__)

substitutions = {
        Symbol('pi'): pi,
        Symbol('e'): E,
        Symbol('oo'): oo,
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

                if ';' not in math_latex:
                    print('huh.')
                    try:
                        if isinstance(a := sympy.simplify(parse_latex(math_latex).doit()), sympy.Eq):
                            print(a)
                            output = sympy.latex([sympy.N(s) for s in sympy.solve(a)] if num else sympy.solve(a))
                        else:
                            print(a)
                            output = sympy.latex(a) if not num else sympy.latex(sympy.N(a))
                    except AttributeError:
                        print(p := parse_latex(math_latex))
                        if isinstance(p, sympy.Eq):
                            output = sympy.latex(sympy.solve(sympy.Eq(p.lhs.doit(), p.rhs.doit())))
                        else:
                            output = sympy.latex(sympy.solve(p))
                    print('huh...')

                else:
                    print('semicolons...')
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

                    output_raw = sympy.solve(eqs)
                    if num:
                        if isinstance(output_raw, dict):
                            print(output_raw)
                            for key in output_raw:
                                print(output_raw[key])
                                try:
                                    output_raw[key] = sympy.N(output_raw[key]) 
                                except:
                                    print('thats fine')
                        if isinstance(output_raw, list):
                            print(output_raw)
                            for o in output_raw:
                                for key in o:
                                    print(o[key])
                                    try:
                                        o[key] = sympy.N(o[key]) 
                                    except:
                                        print('thats fine')
                    output = sympy.latex(output_raw)
                    
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
