#!/usr/bin/env bash
# create_sdlc_pipeline.sh
# macOS-compatible script to create SDLC pipeline project structure
#
# Usage:
#   ./create_sdlc_pipeline.sh            # creates ./sdlc-pipeline
#   ./create_sdlc_pipeline.sh myproj     # creates ./myproj
#   ./create_sdlc_pipeline.sh -g         # create ./sdlc-pipeline and init git
#   ./create_sdlc_pipeline.sh -n name -g # create ./name and init git
#
# Flags:
#   -n NAME    Specify project root name (default: sdlc-pipeline)
#   -g         Initialize a git repo and make initial commit
#   -h         Show help

set -euo pipefail

# defaults
ROOT_NAME="sdlc-pipeline"
INIT_GIT=false

while getopts ":n:gh" opt; do
  case ${opt} in
    n )
      ROOT_NAME="$OPTARG"
      ;;
    g )
      INIT_GIT=true
      ;;
    h )
      echo "Usage: $0 [-n project_name] [-g] [-h]"
      exit 0
      ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Stage directories
STAGES=(
  "1-planning"
  "2-requirements"
  "3-design"
  "4-implementation"
  "5-testing"
  "6-deployment"
  "7-maintenance"
)

SHARED_SUBS=(
  "standards"
  "utilities"
  "examples"
)

TEMPLATES_SUBDIRS=("templates" "prompts" "outputs")

ROOT_DIR="${PWD}/${ROOT_NAME}"

if [ -d "${ROOT_DIR}" ]; then
  echo "Warning: directory '${ROOT_DIR}' already exists."
  read -p "Do you want to continue and add missing files inside it? [y/N]: " yn
  case "$yn" in
    [Yy]* ) echo "Proceeding...";;
    * ) echo "Aborted."; exit 1;;
  esac
fi

echo "Creating root directory: ${ROOT_DIR}"
mkdir -p "${ROOT_DIR}"

# Create style README in root
cat > "${ROOT_DIR}/README.md" <<EOF
# ${ROOT_NAME}

This repository contains a GenAI-powered SDLC prompt pipeline structure.
Folders for each SDLC stage include templates, prompts, and outputs.

Structure generated on: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

# create .gitignore
cat > "${ROOT_DIR}/.gitignore" <<'EOF'
# General ignores
.DS_Store
node_modules/
venv/
__pycache__/
*.log
EOF

# Make each stage with standard subfolders and placeholder files
for stage in "${STAGES[@]}"; do
  stage_dir="${ROOT_DIR}/${stage}"
  echo "  - creating ${stage_dir}"
  for sub in "${TEMPLATES_SUBDIRS[@]}"; do
    dir="${stage_dir}/${sub}"
    mkdir -p "${dir}"
    # add .gitkeep to preserve empty directories in git
    touch "${dir}/.gitkeep"

    # add a small placeholder README to templates & prompts but not outputs (outputs keep .gitkeep)
    if [ "${sub}" = "templates" ]; then
      cat > "${dir}/README.md" <<EOF
# Templates for ${stage}

Place standardized templates for ${stage} here. Example files:
- template_${stage}.md
EOF
    elif [ "${sub}" = "prompts" ]; then
      cat > "${dir}/README.md" <<EOF
# Prompts for ${stage}

Place GenAI prompt templates for ${stage} here. Example files:
- prompt_${stage}.txt
EOF
    fi
  done
done

# Create shared folder and subfolders
shared_dir="${ROOT_DIR}/shared"
mkdir -p "${shared_dir}"
echo "  - creating ${shared_dir}"
for s in "${SHARED_SUBS[@]}"; do
  mkdir -p "${shared_dir}/${s}"
  touch "${shared_dir}/${s}/.gitkeep"
  cat > "${shared_dir}/${s}/README.md" <<EOF
# ${s}

Shared resources for the SDLC pipeline.
EOF
done

# Add helpful example prompt & template files for a couple of stages (lightweight)
cat > "${ROOT_DIR}/1-planning/templates/project_plan_template.md" <<'EOF'
# Project Plan Template

## Project Overview
- Name:
- Objective:
- Stakeholders:

## Scope
- In scope:
- Out of scope:

## Schedule & Milestones
- Phase 1:
- Phase 2:

## Resources
- Roles:
- Estimated effort:
EOF

cat > "${ROOT_DIR}/1-planning/prompts/planning_prompt.txt" <<'EOF'
# Planning prompt (GenAI)

Given the following project brief:
<<PASTE_BRIEF_HERE>>

Produce:
1. Project Charter (bulleted)
2. High-level milestones and timeline
3. Resource plan (roles & headcount)
Format the output as structured markdown.
EOF

cat > "${ROOT_DIR}/2-requirements/prompts/requirements_gathering_prompt.txt" <<'EOF'
# Requirements prompt (GenAI)

Input: Project Charter and high-level goals.

Produce:
- Functional requirements (as enumerated items)
- Non-functional requirements (performance, security, compliance)
- Acceptance criteria per requirement
Return: Structured JSON and markdown.
EOF

# Make a top-level examples file
cat > "${ROOT_DIR}/shared/examples/example_readme.md" <<EOF
# Examples

Place example prompts, example outputs, and sample artifacts here for quick reference.
EOF

# Set permissive permissions for directories
chmod -R u+rwX,go+rX "${ROOT_DIR}"

# Optionally initialize git
if [ "${INIT_GIT}" = true ]; then
  if command -v git >/dev/null 2>&1; then
    echo "Initializing git repository in ${ROOT_DIR}"
    pushd "${ROOT_DIR}" >/dev/null
    git init
    git add .
    git commit -m "chore: initialize sdlc-pipeline structure"
    popd >/dev/null
  else
    echo "git not found in PATH; skipping git init."
  fi
fi

echo "Done. Created project structure at: ${ROOT_DIR}"