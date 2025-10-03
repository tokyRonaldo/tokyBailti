from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector

# ---connexion mysql
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # ⚠️ à adapter
        password="test",       # ⚠️ ton mot de passe MySQL
        database="toDoPy"
    )

class ProductApi(BaseHTTPRequestHandler):
    def _send_response(self,code,data=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers

        if(data):
            self.wfile.write(json.dumps(data, default=str).encode())

    def do_GET(self):
        if self.path == "/products":
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            self._send_response(200, rows)
        else:
            self._send_response(404, {"error": "Route non trouvée"})


    def do_POST(self):
        if self.path == "/products":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                (data["name"], data["price"], data["stock"])
            )
            conn.commit()
            product_id = cursor.lastrowid
            cursor.close()
            conn.close()

            self._send_response(201, {"id": product_id, **data})
        else:
            self._send_response(404, {"error": "Route non trouvée"})


    def do_PUT(self):
        if self.path.startswith("/products/"):
            product_id = self.path.split("/")[-1]
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s",
                (data["name"], data["price"], data["stock"], product_id)
            )
            conn.commit()
            cursor.close()
            conn.close()

            self._send_response(200, {"message": "Produit modifié"})
        else:
            self._send_response(404, {"error": "Route non trouvée"})


    def do_DELETE(self):
        if self.path.startswith("/products/"):
            product_id = self.path.split("/")[-1]

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
            conn.commit()
            cursor.close()
            conn.close()

            self._send_response(200, {"message": "Produit supprimé"})
        else:
            self._send_response(404, {"error": "Route non trouvée"})


# --- Lancer le serveur ---
if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), ProductAPI)
    print("🚀 Serveur lancé sur http://localhost:8000")
    server.serve_forever()
