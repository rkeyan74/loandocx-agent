from pathlib import Path
import threading

HIT_FILE = Path("page_hits.txt")
HIT_LOCK = threading.Lock()


def get_page_hits():
    with HIT_LOCK:
        try:
            hits = int(HIT_FILE.read_text().strip())
        except (FileNotFoundError, ValueError):
            hits = 0

        hits += 1
        HIT_FILE.write_text(str(hits))

    return f"**Page Hits: {hits:,}**"
