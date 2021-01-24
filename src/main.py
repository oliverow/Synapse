from src.app import gui_app
from src.database import Client


def main():
    client = Client()
    app = gui_app(client)
    app.mainloop()

if __name__ == '__main__':
    main()