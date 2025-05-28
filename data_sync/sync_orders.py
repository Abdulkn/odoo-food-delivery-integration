import psycopg2
from odoorpc import ODOO

pg_conn = psycopg2.connect(
    dbname="food_delivery_db",
    user="user",
    password="password",
    host="localhost"
)
pg_cursor = pg_conn.cursor()

odoo = ODOO('odoo.example.com', port=8069)
odoo.login('delivery_db', 'admin', 'admin_password')

def sync_orders():
    pg_cursor.execute("""
        SELECT id, customer_id, restaurant_id, courier_id, 
               total_amount, distance, status, order_date
        FROM orders 
        WHERE synced_to_odoo = FALSE
    """)
    orders = pg_cursor.fetchall()

    for order in orders:
        # Calculate delivery fee
        distance = order[5]
        if distance < 5:
            fee = 2
        elif 5 <= distance < 7:
            fee = 3
        else:
            fee = 5

        # Create Odoo order
        odoo.env['sale.order'].create({
            'partner_id': order[1],  # customer_id
            'user_id': order[3],     # courier_id
            'date_order': order[7],  # order_date
            'amount_total': order[4] + fee,
            'delivery_fee': fee,
            'state': 'sale' if order[6] == 'Delivered' else 'cancel',
        })

        # Mark as synced
        pg_cursor.execute(
            "UPDATE orders SET synced_to_odoo = TRUE WHERE id = %s",
            (order[0],)
        )
    
    pg_conn.commit()

if __name__ == "__main__":
    sync_orders()
    pg_conn.close()
