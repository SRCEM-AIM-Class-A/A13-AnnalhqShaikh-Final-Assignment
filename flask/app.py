from flask import Flask, request, render_template, url_for # Import render_template and url_for

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html') # Render index.html

# Form route
@app.route('/greet', methods=['GET', 'POST'])
def greet():
    error = None
    name = ''
    age = ''

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()

        # Basic validation
        if not name or not age.isdigit():
            error = "Please enter a valid name and a numeric age."
            # Re-render the form with the error message and submitted values
            return render_template('greet_form.html', error=error, name=name, age=age)

        # Render the result template on successful submission
        return render_template('greet_result.html', name=name, age=age)

    # Render the form template for GET requests
    return render_template('greet_form.html', error=error, name=name, age=age)

if __name__ == '__main__':
    app.run(debug=True)
