import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql://root:noeiMupVeGBGiMXowKzPfQMElrrvTDWK@monorail.proxy.rlwy.net:28653/railway'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'noeiMupVeGBGiMXowKzPfQMElrrvTDWK'),
    'database': os.getenv('DB_NAME', 'railway')
}
