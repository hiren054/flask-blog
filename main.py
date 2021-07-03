from website import create_app
import os

PORT = os.environ['PORT'] if os.environ['PORT'] is not None else 5000

app = create_app()


if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=PORT,debug=True)