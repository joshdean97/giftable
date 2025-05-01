from api import create_app

if __name__ == "__main__":
    app = create_app()
    # Run the app
    app.run(debug=True)
