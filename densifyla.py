from app import app


if __name__ == '__main__':
    # run email debug server with 'python -m smtpd -n -c DebuggingServer localhost:3333'
    app.run()

