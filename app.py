from flask import Flask, jsonify, render_template, request
from database import GradSchemeDB

#creates web server
app = Flask(__name__)

#creates route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/schemes")
def get_schemes():
    db = GradSchemeDB()
    #requests.args is a dictionary of URL query parameters
    industry = request.args.get("industry")
    if industry:
        schemes = db.get_schemes_by_industry(industry)
    else:
        schemes = db.get_schemes()
    db.close()
    return jsonify([dict(scheme)for scheme in schemes])

if __name__ == "__main__":
    app.run(debug=True)