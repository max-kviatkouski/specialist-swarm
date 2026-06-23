#!/usr/bin/env bash
# One-command demo runner for the AI Wealth Advisory Swarm.
#   ./run_demo.sh [path/to/client.md]
# Loads ANTHROPIC_API_KEY from .env (value never printed), runs the full pipeline,
# and leaves deliverables in outputs/.
set -euo pipefail
cd "$(dirname "$0")"

# Load .env without echoing secrets.
if [ -f .env ]; then set -a; . ./.env; set +a; fi
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "ERROR: ANTHROPIC_API_KEY is not set. Copy .env.sample to .env and add your key." >&2
  exit 1
fi

CLIENT="${1:-synthetic-data/clients/client-mid-career-family.md}"

echo "==> Installing dependencies"
pip install -q -r requirements.txt

echo "==> 1/5 create specialists"; python create_specialists.py
echo "==> 2/5 upload + attach skills"; python upload_skills.py
echo "==> 3/5 create coordinator"; python create_coordinator.py
echo "==> 4/5 setup environment"; python setup_environment.py
echo "==> 5/5 run advisory for: $CLIENT"; python run_advisory.py "$CLIENT"

echo
echo "Deliverables:"
ls -la outputs/ 2>/dev/null || echo "  (none — check the session URL above)"
echo
echo "  open outputs/financial_plan.pptx"
echo "  python evals/validate_plan.py outputs/financial_plan.json"
