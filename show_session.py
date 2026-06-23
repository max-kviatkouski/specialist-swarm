"""
Inspect a managed-agents session: list every agent thread and replay its output.

There is NO web console page for managed-agents sessions — the API is the source
of truth — so this IS the "session viewer". It shows the coordinator (primary)
thread plus every specialist thread the coordinator spawned, with each agent's
work. Great for the demo: "here is the whole multi-agent session."

Usage:
    python show_session.py                 # uses .last_session_id
    python show_session.py sesn_01ABC...   # a specific session id
    python show_session.py --full          # don't truncate agent messages
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from anthropic import Anthropic

load_dotenv()


def main() -> None:
    raw = sys.argv[1:]
    full = "--full" in raw
    rest = [a for a in raw if a != "--full"]

    if rest:
        session_id = rest[0].strip()
    else:
        p = Path(".last_session_id")
        if not p.exists():
            raise SystemExit("No session id given and .last_session_id not found.")
        session_id = p.read_text().strip()

    client = Anthropic(default_headers={"anthropic-beta": "managed-agents-2026-04-01"})

    s = client.beta.sessions.retrieve(session_id)
    print(f"Session {session_id}")
    print(f"  title:  {getattr(s, 'title', None)}")
    print(f"  status: {getattr(s, 'status', None)}")
    if getattr(s, "usage", None):
        print(f"  usage:  {s.usage}")
    print()

    threads = list(client.beta.sessions.threads.list(session_id))
    # Primary thread (parent_thread_id is None) first.
    threads.sort(key=lambda t: getattr(t, "parent_thread_id", None) is not None)

    print(f"{len(threads)} thread(s):")
    for t in threads:
        name = getattr(getattr(t, "agent", None), "name", "?")
        role = "PRIMARY/coordinator" if getattr(t, "parent_thread_id", None) is None else "specialist"
        print(f"  - [{role}] {name:34s} {getattr(t, 'status', '?'):9s} {t.id}")
    print()

    # A specialist's final answer is delivered to the coordinator as an
    # `agent.thread_message_received` event on the PRIMARY thread (not always as an
    # `agent.message` on its own thread). Collect those as a fallback per agent name.
    primary = next((t for t in threads if getattr(t, "parent_thread_id", None) is None), None)
    received: dict[str, list[str]] = {}
    if primary is not None:
        try:
            for ev in client.beta.sessions.threads.events.list(primary.id, session_id=session_id):
                if getattr(ev, "type", None) == "agent.thread_message_received":
                    frm = getattr(ev, "from_agent_name", None)
                    if frm:
                        for block in getattr(ev, "content", []) or []:
                            if getattr(block, "type", None) == "text":
                                received.setdefault(frm, []).append(block.text)
        except Exception:  # noqa: BLE001
            pass

    for t in threads:
        name = getattr(getattr(t, "agent", None), "name", "?")
        print("=" * 72)
        print(f"THREAD: {name}   ({t.id})")
        print("=" * 72)
        texts: list[str] = []
        try:
            for ev in client.beta.sessions.threads.events.list(t.id, session_id=session_id):
                if getattr(ev, "type", None) == "agent.message":
                    for block in getattr(ev, "content", []) or []:
                        if getattr(block, "type", None) == "text":
                            texts.append(block.text)
        except Exception as e:  # noqa: BLE001
            print(f"  (could not list events: {e})")
        body = "".join(texts).strip()
        if not body and name in received:
            body = "".join(received[name]).strip() + "\n  [↑ delivered to the coordinator]"
        body = body or "(no text output on this thread)"
        if not full and len(body) > 1400:
            body = body[:1400] + "\n... [truncated — run with --full]"
        print(body)
        print()


if __name__ == "__main__":
    main()
