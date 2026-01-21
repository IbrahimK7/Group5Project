from dotenv import load_dotenv
load_dotenv()   # <-- MUST be first

from utils import create_app
from flask import redirect

app = create_app()


def index():
    return redirect('/login')

app.add_url_rule('/', 'index', index)

# debug: show registered routes
print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)
