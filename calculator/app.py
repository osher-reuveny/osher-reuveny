from flask import Flask, render_template, request
from .utils import eval_expr

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression = ''
    error = None
    if request.method == 'POST':
        expression = request.form.get('expression', '')
        try:
            result = eval_expr(expression)
        except Exception as exc:
            error = str(exc)
    return render_template('index.html', result=result, expression=expression, error=error)


if __name__ == '__main__':
    app.run(debug=True)
