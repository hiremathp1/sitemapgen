#########################################################################
#  P N Hiremath -- 7, December of 2020                               #
#                                                                       #
#########################################################################
#  Description: Makes it easier to generate linkedin oauth2 token.      #
#                                                                       #
#########################################################################

import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Linkedin oauth2 token generator')

parser.add_argument('--port', action="store", default=3000, required=False, help="Port to listen on")
parser.add_argument('--id', action="store", default='', required=True, help="Linkedin app id")
parser.add_argument('--secret', action="store", default='', required=True, help="Linkedin app secret")

arg = parser.parse_args()

PORT=int(arg.port)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.code=''

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(
            self.path).encode('utf-8'))
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        if not self.code:
            code = query_components["code"]
            logging.info(f"Obtaining acess token from code {code}.....")
            webbrowser.open(f"https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&client_id={arg.id}&client_secret={arg.secret}&code={code}&redirect_uri=http://localhost:{PORT}")
        else:
            token = query_components["auth_token"]
            print("TOKEN:", token)
            self.server.running = False


def run(server_class=HTTPServer, handler_class=S, port=PORT):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    scope="rw_organization_admin"
    scope="r_liteprofile"
    webbrowser.open(f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={arg.id}&scope={scope}&state=123456&redirect_uri=http://localhost:{PORT}")
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    run()
