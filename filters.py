import json
from markupsafe import Markup

def register_filters(app):
    """Register custom Jinja2 filters"""
    
    @app.template_filter('tojsonfilter')
    def to_json_filter(obj):
        """Convert Python object to JSON string for use in templates"""
        return Markup(json.dumps(obj))
    
    @app.template_filter('safe_json')
    def safe_json_filter(obj):
        """Convert Python object to JSON string with HTML escaping"""
        return json.dumps(obj)
    
    @app.template_filter('format_datetime')
    def format_datetime_filter(dt, format='%Y-%m-%d %H:%M'):
        """Format datetime objects"""
        if dt is None:
            return ""
        return dt.strftime(format)
    
    @app.template_filter('format_percentage')
    def format_percentage_filter(value, decimals=1):
        """Format number as percentage"""
        if value is None:
            return "0%"
        return f"{value:.{decimals}f}%"