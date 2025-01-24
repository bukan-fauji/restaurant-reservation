from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import connect_db

order_bp = Blueprint('order_bp', __name__)

# Buat pesanan makanan berdasarkan reservasi
@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """
    Create a food order
    ---
    tags:
      - Order
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            reservation_id:
              type: integer
              example: 1
            menu_id:
              type: integer
              example: 2
            quantity:
              type: integer
              example: 3
    responses:
      201:
        description: Pesanan berhasil dibuat!
      400:
        description: Reservasi dan menu harus diisi!
      401:
        description: Unauthorized, token tidak valid atau tidak ditemukan
"""
    current_user = get_jwt_identity()
    data = request.json

    reservation_id = data.get('reservation_id')
    menu_id = data.get('menu_id')
    quantity = data.get('quantity', 1)

    if not reservation_id or not menu_id:
        return jsonify({'message': 'Reservasi dan menu harus diisi!'}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO order_restaurant (reservation_id, menu_id, quantity) VALUES (%s, %s, %s)", 
                   (reservation_id, menu_id, quantity))
    conn.commit()

    return jsonify({'message': 'Pesanan berhasil dibuat!'}), 201

# Lihat semua pesanan dari reservasi tertentu
@order_bp.route('/<int:reservation_id>', methods=['GET'])
@jwt_required()
def get_orders(reservation_id):
    """
    Get orders by reservation ID
    ---
    tags:
      - Order
    security:
      - Bearer: []
    parameters:
      - name: reservation_id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Daftar pesanan berhasil diambil
        schema:
          type: object
          properties:
            orders:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  reservation_id:
                    type: integer
                    example: 1
                  menu_id:
                    type: integer
                    example: 2
                  quantity:
                    type: integer
                    example: 3
      401:
        description: Unauthorized, token tidak valid atau tidak ditemukan
"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM order_restaurant WHERE reservation_id = %s", (reservation_id,))
    orders = cursor.fetchall()

    return jsonify({'orders': orders}), 200

# Hapus pesanan
@order_bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    """
    Delete an order
    ---
    tags:
      - Order
    security:
      - Bearer: []
    parameters:
      - name: order_id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Pesanan berhasil dihapus!
      401:
        description: Unauthorized, token tidak valid atau tidak ditemukan
"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM order_restaurant WHERE id = %s", (order_id,))
    conn.commit()

    return jsonify({'message': 'Pesanan berhasil dihapus!'}), 200

