import keys

import pkg_resources

from tropofy import main as tropofy_main, serve_app_cascade

apps_config = {
    'tropofy': {
        'api_url': 'https://api.tropofy.com',
        'auth_url': 'https://auth.tropofy.com',
    },
    'database': {
        'url': 'sqlite:///starter.db',
    },
    'apps': [
        {
            'module': 'te_starter',
            'classname': 'MyFirstApp',
            'config': {
                'key.public': keys.public,
                'key.private': keys.private,
            }
        }
    ]
}


tropofy_app = tropofy_main(apps_config)

if __name__ == "__main__":
    serve_app_cascade(tropofy_app, '0.0.0.0', 8080)
