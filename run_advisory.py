"""
Run the Wealth Advisory swarm against a client ticket.

Inlines the client profile into the user message, opens a session against the
coordinator, streams the events (watch the specialist subset fan out — this is the
demo), then downloads the deliverables (financial_plan.json + financial_plan.pptx).

Usage:
    python run_advisory.py                                   # default client
    python run_advisory.py synthetic-data/clients/client-young-accumulator.md
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from anthropic import Anthropic

load_dotenv()

DEFAULT_CLIENT = Path("synthetic-data/clients/client-mid-career-family.md")
OUTPUT_DIR = Path("outputs")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY (export it or put it in .env) before running.")

    if not Path(".coordinator_id").exists() or not Path(".environment_id").exists():
        raise SystemExit(
            "Missing .coordinator_id or .environment_id. Run create_specialists.py, "
            "upload_skills.py, create_coordinator.py, then setup_environment.py first."
        )

    client_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CLIENT
    if not client_path.exists():
        raise SystemExit(f"Client file not found: {client_path}")

    coordinator_id = Path(".coordinator_id").read_text().strip()
    environment_id = Path(".environment_id").read_text().strip()

    client = Anthropic(
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    print(f"Loading client ticket: {client_path.name}")
    context = f"=====  CLIENT TICKET: {client_path.name}  =====\n{client_path.read_text()}"

    session = client.beta.sessions.create(
        agent=coordinator_id,
        environment_id=environment_id,
        title=f"Wealth Advisory — {client_path.stem}",
    )
    Path(".last_session_id").write_text(session.id)
    print(f"Session: {session.id}\n")

    user_message = (
        "A new client ticket has arrived. Run the standard advisory process:\n"
        "1. Classify the ticketType.\n"
        "2. Delegate to ONLY the right specialist subset (per your routing table), in parallel.\n"
        "3. Synthesise, then get the Compliance Reviewer's verdict and honour it.\n"
        "4. Write financial_plan.json and produce financial_plan.pptx.\n\n"
        f"{context}"
    )

    print("=== EVENT STREAM (watch the subset fan out) ===\n")
    final_text: list[str] = []
    running_threads: set = set()
    had_running = False
    saw_message = False

    def thread_id_of(ev):
        for attr in ("session_thread_id", "thread_id", "id"):
            v = getattr(ev, attr, None)
            if v:
                return v
        return None

    with client.beta.sessions.events.stream(session.id) as stream:
        client.beta.sessions.events.send(
            session.id,
            events=[{"type": "user.message", "content": [{"type": "text", "text": user_message}]}],
        )
        for event in stream:
            t = event.type
            tid = thread_id_of(event)

            if t == "session.thread_created":
                print(f"  [thread spawned]   {getattr(event, 'agent_name', '?')}", flush=True)
            elif t == "session.thread_status_running":
                if tid:
                    running_threads.add(tid)
                    had_running = True
                print(f"  [thread running]   {getattr(event, 'agent_name', '?')}", flush=True)
            elif t in ("session.thread_status_idle", "session.thread_status_terminated"):
                if tid:
                    running_threads.discard(tid)
                # Terminal: the swarm is done when every thread that ran has gone
                # idle and the coordinator has produced its final message. (Per the
                # API docs the terminal signal is per-thread session.thread_status_idle
                # with stop_reason end_turn — NOT a session.status_idle event.)
                if had_running and not running_threads and saw_message:
                    print("\n\n[swarm finished]")
                    break
            elif t == "agent.thread_message_sent":
                print(f"  [delegate ->]      {getattr(event, 'to_agent_name', '?')}", flush=True)
            elif t == "agent.thread_message_received":
                print(f"  [reply <-]         {getattr(event, 'from_agent_name', '?')}", flush=True)
            elif t == "agent.message":
                saw_message = True
                for block in event.content:
                    if getattr(block, "type", None) == "text":
                        final_text.append(block.text)
                        print(block.text, end="", flush=True)
            elif t == "agent.tool_use":
                print(f"\n  [tool: {getattr(event, 'name', '?')}]", flush=True)

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "coordinator-transcript.txt").write_text("".join(final_text))

    # Files lag the idle signal by ~1-3s while they index — retry a few times.
    print("\nDownloading deliverables...")
    files = []
    for attempt in range(4):
        listing = client.beta.files.list(scope_id=session.id, betas=["managed-agents-2026-04-01"])
        files = list(listing.data)
        if files:
            break
        time.sleep(2)

    for f in files:
        out_path = OUTPUT_DIR / f.filename
        print(f"  {f.filename}  ->  {out_path}")
        client.beta.files.download(f.id).write_to_file(str(out_path))

    if not files:
        print("  (no files found yet — they can lag a few seconds)")
    print(f"\nSession id: {session.id}")
    print(f"Inspect every agent thread with:\n  python show_session.py {session.id}")


if __name__ == "__main__":
    main()
