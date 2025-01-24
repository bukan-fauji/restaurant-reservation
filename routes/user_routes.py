from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from models.db import connect_db
import json

user_bp = Blueprint('user_bp', __name__)

# REGISTER USER
@user_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: 123456
    responses:
      201:
        description: Registrasi berhasil!
      400:
        description: Username sudah digunakan atau data tidak lengkap!
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username dan password diperlukan!'}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Cek apakah username sudah ada
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'message': 'Username sudah digunakan!'}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Simpan ke database
    cursor.execute("INSERT INTO user (username, password, role) VALUES (%s, %s, 'customer')", 
                   (username, hashed_password))
    conn.commit()

    return jsonify({'message': 'Registrasi berhasil!'}), 201

# LOGIN USER
@user_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: 123456
    responses:
      200:
        description: Login berhasil!
        schema:
          type: object
          properties:
            message:
              type: string
              example: Login berhasil!
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR..."
      401:
        description: Username atau password salah!
"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Ambil user dari database
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'message': 'Username atau password salah!'}), 401

    # Buat token JWT
    access_token = create_access_token(identity=json.dumps({'id': user['id'], 'role': user['role']}))
    
    return jsonify({'message': 'Login berhasil!', 'access_token': access_token}), 200

# ROUTE PROTECTED (Hanya bisa diakses user yang login)
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Get user profile
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: Data user berhasil diambil
        schema:
          type: object
          properties:
            message:
              type: string
              example: Data user
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                role:
                  type: string
                  example: customer
      401:
        description: Unauthorized, token tidak valid atau tidak ditemukan
"""
    current_user = json.loads(get_jwt_identity())
    return jsonify({'message': 'Data user', 'user': current_user}), 200

