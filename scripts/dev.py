#!/usr/bin/env python3
"""Dev local : reconstruit dist/ à chaque modification de src/ et sert le site sur http://localhost:8080.
Usage : python3 scripts/dev.py [port]        (sans Docker)
        python3 scripts/dev.py --watch-only  (dans le conteneur de dev : nginx sert dist/)
"""
import functools, http.server, os, socketserver, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SRC", os.path.join(HERE, "..", "src"))
DIST = os.environ.get("OUT", os.path.join(HERE, "..", "dist"))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
WATCH_ONLY = "--watch-only" in sys.argv
PORT = int(ARGS[0]) if ARGS else 8080


def snapshot():
    state = {}
    for root, _, files in os.walk(SRC):
        for f in files:
            p = os.path.join(root, f)
            try:
                state[p] = os.stat(p).st_mtime
            except FileNotFoundError:
                pass
    return state


def build():
    t = time.time()
    r = subprocess.run([sys.executable, os.path.join(SRC, "build.py")], capture_output=True, text=True)
    stamp = time.strftime("%H:%M:%S")
    if r.returncode == 0:
        print(f"[{stamp}] ✓ {r.stdout.strip()} ({time.time() - t:.1f} s)", flush=True)
    else:
        print(f"[{stamp}] ✗ erreur de build\n{r.stderr}", flush=True)


def watch():
    last = snapshot()
    while True:
        time.sleep(1)
        now = snapshot()
        if now != last:
            last = now
            build()


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    build()
    if WATCH_ONLY:
        print(f"Surveillance de {os.path.abspath(SRC)}", flush=True)
        watch()
    threading.Thread(target=watch, daemon=True).start()
    handler = functools.partial(NoCache, directory=DIST)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
        print(f"→ http://localhost:{PORT}  (Ctrl+C pour arrêter)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
