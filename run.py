import os

from ui.app import build_app


def main():
    app = build_app()
    app.queue()
    app.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("PORT", os.getenv("GRADIO_SERVER_PORT", "10000"))),
        show_error=True,
    )


if __name__ == "__main__":
    main()