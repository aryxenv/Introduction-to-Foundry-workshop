"""
Simple web server for the voice-enabled chatbot interface
Serves the web interface and provides access to the API
"""
import os
import sys
from pathlib import Path
import http.server
import socketserver
from functools import partial


def run_server(port=8080, directory=None):
    """
    Run a simple HTTP server for the web interface
    
    Args:
        port: Port to run server on (default: 8080)
        directory: Directory to serve (default: ../web)
    """
    if directory is None:
        directory = Path(__file__).parent.parent / "web"
    
    directory = Path(directory).resolve()
    
    if not directory.exists():
        print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)
    
    print("🌐 Starting web server...")
    print(f"   Directory: {directory}")
    print(f"   Port: {port}")
    print(f"\n✅ Server running at http://localhost:{port}")
    print("\nPress Ctrl+C to stop")
    print("-" * 50)
    
    # Change to the web directory
    os.chdir(directory)
    
    # Create handler
    Handler = partial(http.server.SimpleHTTPRequestHandler)
    
    # Start server
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping server...")
            httpd.shutdown()
            print("✅ Server stopped")


def main():
    """Run the web server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Serve the voice chatbot web interface")
    parser.add_argument("--port", type=int, default=8080, help="Port to run server on")
    parser.add_argument("--dir", type=str, help="Directory to serve (default: ../web)")
    
    args = parser.parse_args()
    
    run_server(port=args.port, directory=args.dir)


if __name__ == "__main__":
    main()
