"""
Upload each custom skill in skills/ via the Skills API and attach it to the right
specialist agent.

Idempotent: re-uses skills already uploaded (matched by display_title) and skips
already-attached skills, so the hackathon dev loop (re-run after edits) is safe.

Usage:
    python upload_skills.py
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from anthropic import Anthropic
from anthropic.lib import files_from_dir

load_dotenv()

# Map skill directory name -> specialist key that should get it.
SKILL_TO_SPECIALIST = {
    "asset-allocation-playbook": "portfolio",
    "risk-profiling": "risk",
    "financial-planning-playbook": "goals",
}


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY (export it or put it in .env) before running.")

    specialist_ids_path = Path(".specialist_ids.json")
    if not specialist_ids_path.exists():
        raise SystemExit("Run create_specialists.py first.")
    specialist_ids = json.loads(specialist_ids_path.read_text())

    client = Anthropic(
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    # The Skills API enforces unique display_title, so list existing custom skills
    # and reuse by title rather than re-uploading on a dev-loop re-run.
    print("Checking for existing skills...")
    existing_by_title: dict[str, str] = {}
    for page in client.beta.skills.list(source="custom"):
        existing_by_title[page.display_title] = page.id

    uploaded: dict[str, str] = {}

    for skill_name, specialist_key in SKILL_TO_SPECIALIST.items():
        skill_dir = Path("skills") / skill_name
        if not (skill_dir / "SKILL.md").exists():
            print(f"  Skipping {skill_name} — no SKILL.md found")
            continue

        display_title = skill_name.replace("-", " ").title()

        if display_title in existing_by_title:
            skill_id = existing_by_title[display_title]
            print(f"Reusing existing skill: {skill_name} ({skill_id})")
            uploaded[skill_name] = skill_id
        else:
            print(f"Uploading skill: {skill_name}...")
            skill = client.beta.skills.create(
                display_title=display_title,
                files=files_from_dir(str(skill_dir)),
            )
            uploaded[skill_name] = skill.id
            print(f"  -> {skill.id}")

        specialist_id = specialist_ids[specialist_key]
        skill_id = uploaded[skill_name]
        print(f"  attaching to specialist `{specialist_key}` ({specialist_id})...")

        current = client.beta.agents.retrieve(specialist_id)
        # NOTE: current.skills are pydantic models, not dicts — use getattr, not .get().
        already_attached = any(
            getattr(s, "skill_id", None) == skill_id for s in (current.skills or [])
        )
        if already_attached:
            print("  already attached ✓ (skipping)")
            continue

        # Serialize existing skill entries to dicts before re-submitting.
        existing = [
            {
                "type": s.type,
                "skill_id": s.skill_id,
                **({"version": getattr(s, "version", "latest")} if s.type == "custom" else {}),
            }
            for s in (current.skills or [])
        ]
        new_skills = existing + [
            {"type": "custom", "skill_id": skill_id, "version": "latest"}
        ]
        client.beta.agents.update(
            specialist_id,
            version=current.version,
            skills=new_skills,
        )
        print("  attached ✓")

    Path(".skill_ids.json").write_text(json.dumps(uploaded, indent=2))
    print(f"\nUploaded/attached {len(uploaded)} skills.")
    print("Next: python create_coordinator.py")


if __name__ == "__main__":
    main()
