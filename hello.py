from http.server import HTTPServer, SimpleHTTPRequestHandler

with open('index.html', 'r')as f:
    index_file = f.read()

class OriginalHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.end_headers()

        html = index_file.format(
            title = 'ブログのタイトル',
            content = 'ブログの内容'
        )
        self.wfile.write(html.encode('utf-8'))
        return None

def run(server_class=HTTPServer, handler_class=OriginalHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()