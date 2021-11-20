from cgi import FieldStorage, test
from http.server import HTTPServer, SimpleHTTPRequestHandler
import MySQLdb

def database(postdata):
    conn = MySQLdb.connect(
    user='root',
    passwd='',
    host='localhost',
    db='test_db',
    charset='utf8'
    ) 
    cursor = conn.cursor()
    sql=('INSERT INTO test (title, content) values (%s,%s)')
    cursor.execute(sql,postdata)
    cursor.execute('select * from test;')
    for row in cursor:
        print(row)
    conn.commit()
    # 接続を閉じる
    conn.close

with open('index.html', 'r',encoding="utf-8") as f:
    index_file = f.read()

with open('result.html', 'r',encoding="utf-8") as f:
    result_file = f.read()

class OriginalHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.end_headers()

        html = index_file.format(
            header = '投稿画面',
            title = 'ブログのタイトル',
            content = 'ブログの内容'
        )
        self.wfile.write(html.encode('UTF-8'))
        return None


    def do_POST(self):

        form = FieldStorage(
            fp = self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})

        title_form = form['titlefield'].value
        content_form = form['contentfield'].value


        self.send_response(200)
        self.end_headers()

        html = result_file.format(
            header = '投稿結果',
            title_message = 'タイトル：',
            content_message = '投稿内容：',
            title = title_form, 
            content = content_form,
            link = '/index.html',
        )
        postdata = [title_form,content_form]
        self.wfile.write(html.encode('utf-8'))
        database(postdata)
        return None

def run(server_class=HTTPServer, handler_class=OriginalHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()