from flask import Flask, render_template, request, redirect, url_for, flash, abort
from database import init_db, add_url, get_original_url, increment_clicks, get_url_stats
import validators


app = Flask(__name__)
app.secret_key = 'Indu@123'

# Initialize database
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        
        if not validators.url(original_url):
            flash('Please enter a valid URL (e.g., https://example.com)')
            return redirect(url_for('index'))
        
        short_code = add_url(original_url)
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = get_original_url(short_code)
    if original_url:
        increment_clicks(short_code)
        return redirect(original_url)
    else:
        abort(404)

@app.route('/stats/<short_code>')
def url_stats(short_code):
    stats = get_url_stats(short_code)
    if stats:
        return render_template('stats.html', stats=stats)
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)