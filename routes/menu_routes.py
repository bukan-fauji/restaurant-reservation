from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.db import connect_db

menu_bp = Blueprint('menu_bp', __name__)

# Ambil semua menu
@menu_bp.route('/', methods=['GET'])
def get_menus():
    """
    Get all menu items
    ---
    tags:
      - Menu
    responses:
      200:
        description: Daftar menu yang tersedia
        schema:
          type: object
          properties:
            menus:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Nasi Goreng"
                  price:
                    type: number
                    example: 25000
                  description:
                    type: string
                    example: "Nasi goreng spesial dengan ayam"
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM menu")
    menus = cursor.fetchall()
    
    return jsonify({'menus': menus}), 200

# Tambah menu (hanya admin)
@menu_bp.route('/', methods=['POST'])
@jwt_required()
def add_menu():
    """
    Add a new menu item
    ---
    tags:
      - Menu
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Bearer token for authentication"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Ayam Bakar"
            price:
              type: number
              example: 35000
            description:
              type: string
              example: "Ayam bakar dengan bumbu khas"
    responses:
      201:
        description: Menu berhasil ditambahkan!
      400:
        description: Data tidak lengkap atau token tidak valid.
    """
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    if not name or not price:
        return jsonify({'message': 'Nama dan harga harus diisi!'}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO menu (name, price, description) VALUES (%s, %s, %s)", 
                   (name, price, description))
    conn.commit()

    return jsonify({'message': 'Menu berhasil ditambahkan!'}), 201

# Edit menu (hanya admin)
@menu_bp.route('/<int:menu_id>', methods=['PUT'])
@jwt_required()
def update_menu(menu_id):
    """
    Update a menu item
    ---
    tags:
      - Menu
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Bearer token for authentication"
      - name: menu_id
        in: path
        type: integer
        required: true
        description: "ID menu yang ingin diperbarui"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Nasi Goreng Special"
            price:
              type: number
              example: 30000
            description:
              type: string
              example: "Nasi goreng dengan topping telur dan ayam"
    responses:
      200:
        description: Menu berhasil diperbarui!
      400:
        description: Data tidak valid atau token tidak valid.
      404:
        description: Menu tidak ditemukan.
    """
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE menu SET name = %s, price = %s, description = %s WHERE id = %s",
                   (name, price, description, menu_id))
    conn.commit()

    return jsonify({'message': 'Menu berhasil diperbarui!'}), 200

# Hapus menu (hanya admin)
@menu_bp.route('/<int:menu_id>', methods=['DELETE'])
@jwt_required()
def delete_menu(menu_id):
    """
    Delete a menu item
    ---
    tags:
      - Menu
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Bearer token for authentication"
      - name: menu_id
        in: path
        type: integer
        required: true
        description: "ID menu yang ingin dihapus"
    responses:
      200:
        description: Menu berhasil dihapus!
      404:
        description: Menu tidak ditemukan.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM menu WHERE id = %s", (menu_id,))
    conn.commit()

    return jsonify({'message': 'Menu berhasil dihapus!'}), 200

