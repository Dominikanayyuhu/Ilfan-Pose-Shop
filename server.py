import http.server
import socketserver
import os

# Railway дает нам порт через переменную окружения PORT
PORT = int(os.environ.get("PORT", 8080))

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущен на порту {PORT}")
    httpd.serve_forever()
