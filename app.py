from flask import Flask
from routes.company_routes import company_bp
from routes.ad_routes import ad_bp
from routes.analytics_routes import analytics_bp
from routes.llm_routes import llm_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(company_bp)
app.register_blueprint(ad_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(llm_bp)

if __name__ == "__main__":
    app.run(debug=True)
