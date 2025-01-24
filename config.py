import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql-production-4178.up.railway.app'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'noeiMupVeGBGiMXowKzPfQMElrrvTDWK'),
    'database': os.getenv('DB_NAME', 'railway')
    'port': int(os.getenv('DB_PORT', 3306))
}
