"""Run module. This is the file that is invoked to start up a development server."""
from water_garden.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)