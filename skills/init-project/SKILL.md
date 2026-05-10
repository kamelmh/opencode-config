---
name: init-project
description: Initialize or refine project setup — global JOC config, project .opencode/, hierarchical docs, context capture, and agent routing in one pass. Replaces /joc-setup, /deepinit, and /init-project-config.
level: 3
---

# Init Project

Unified project initialization. Detects, scaffolds, documents, and refines an OpenCode JOC project in one pass. Works for both first-time setup and iterative re-runs.

## When to Use

- First time setting up JOC in a project
- Adding JOC to an existing codebase
- Refreshing config after major changes (refactors, new deps, team growth)
- Running `/init-project` again to capture new context and refine docs
- Replacing `/joc-setup`, `/deepinit`, or `/init-project-config`

## Architecture

| Phase | Agent/Skill | Purpose |
|-------|-------------|---------|
| 0 - Global Verify | self | Ensure `~/.config/opencode/` is healthy |
| 1 - Detection | `explore` | Scan project files, detect language/framework |
| 2 - Planning | `planner` | Generate initialization plan from detection |
| 3 - Scaffolding | `executor` | Create `.opencode/` structure, opencode.jsonc, AGENTS.md |
| 4 - Docs | `deepinit` | Hierarchical AGENTS.md across codebase |
| 5 - Context Capture | `remember` + `wiki` | Promote session knowledge, scan state artifacts |
| 6 - Routing | `architect` | Optimize agent selection for detected stack |
| 7 - Verification | `verifier` | Validate completeness, references, config |

## Flag Parsing

| Flag | Effect | Phases |
|------|--------|--------|
| `--minimal` | Essential files only | 0-3 |
| `--full` | Everything including context and routing | 0-7 |
| `--refresh` | Merge mode, preserve manual edits | 0-7 (merge) |
| `--force` | Skip "already exists" checks | 0-7 |
| `--language <lang>` | Force language, skip Phase 1 detection | 0-7 |
| `--docs` | Docs phase only (equivalent to old `/deepinit`) | 4 |
| `--no-docs` | Skip Phase 4 | 0-3, 5-7 |
| `--skip-detection` | Use generic defaults | 0-7 |
| `--help` | Show help and stop | — |

Default (no flags): Phases 0-4 (full scaffold + docs, no context/routing).

## Help Text

```
Init Project - Set up or refine JOC for this project

USAGE:
   /init-project               Auto-detect, scaffold, and document
   /init-project --minimal     Essential files only (no docs)
   /init-project --full        Everything: config, docs, context, routing
   /init-project --refresh     Update existing (preserve manual edits)
   /init-project --force       Overwrite without prompts
   /init-project --language rust   Force language, skip detection
   /init-project --docs        Re-run docs hierarchy only
   /init-project --no-docs     Skip docs hierarchy
   /init-project --help        Show this help

PHASES:
   0 - Verify global JOC installation
   1 - Detect language, framework, build tools
   2 - Plan configuration based on detection
   3 - Scaffold .opencode/ (config, agents, rules, state)
   4 - Generate hierarchical AGENTS.md documentation
   5 - Capture context from session and state files
   6 - Optimize agent routing for this stack
   7 - Validate everything works

IDempOTENT: Re-running only updates what changed. Manual edits preserved.
```

## Pre-Flight

Before starting any phases, determine scope:

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OPENCODE_DIR="$PROJECT_ROOT/.opencode"
GLOBAL_DIR="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"

# Determine if this is first-run or re-run
if [ -d "$OPENCODE_DIR" ] && [ -f "$OPENCODE_DIR/opencode.jsonc" ]; then
  IS_RERUN="true"
  echo "Existing .opencode/ configuration found — running in refresh mode"
else
  IS_RERUN="false"
  echo "No .opencode/ found — running initial setup"
fi

# Check global health
if [ -f "$GLOBAL_DIR/AGENTS.md" ] && [ -f "$GLOBAL_DIR/opencode.jsonc" ]; then
  GLOBAL_HEALTHY="true"
else
  GLOBAL_HEALTHY="false"
  echo "WARNING: Global JOC config incomplete or missing"
fi
```

If `IS_RERUN=true` and no `--force` or `--refresh` flag was passed, ask:

**Question:** "This project already has `.opencode/` configured. What would you like to do?"

**Options:**
1. **Refresh** - Update configuration and docs, preserve manual edits
2. **Full re-init** - Re-run all phases from scratch (`--force`)
3. **Docs only** - Regenerate AGENTS.md documentation only (`--docs`)
4. **Cancel** - Exit without changes

## Phase 0: Verify Global JOC

**Skip if:** `GLOBAL_HEALTHY=true` or `--force` flag

### Check Global Structure

```bash
GLOBAL_DIR="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"

echo "Checking global JOC installation..."

# Verify essential files
for f in AGENTS.md opencode.jsonc; do
  if [ -f "$GLOBAL_DIR/$f" ]; then
    echo "  ✓ $f"
  else
    echo "  ✗ $f MISSING"
  fi
done

# Verify essential directories
for d in skills commands agents plugins rules; do
  if [ -d "$GLOBAL_DIR/$d" ]; then
    COUNT=$(ls "$GLOBAL_DIR/$d" 2>/dev/null | wc -l)
    echo "  ✓ $d/ ($COUNT items)"
  else
    echo "  ✗ $d/ MISSING"
  fi
done

# Count skill capacity
SKILL_COUNT=$(ls -d "$GLOBAL_DIR/skills"/*/ 2>/dev/null | wc -l)
AGENT_COUNT=$(ls "$GLOBAL_DIR/agents"/*.md 2>/dev/null | wc -l)
COMMAND_COUNT=$(ls "$GLOBAL_DIR/commands"/*.md 2>/dev/null | wc -l)
echo ""
echo "Global capacity: $SKILL_COUNT skills, $AGENT_COUNT agents, $COMMAND_COUNT commands"
```

### Fix Missing Pieces

If any essential directories or files are missing, create them:

```bash
GLOBAL_DIR="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"

# Create missing directories
for d in skills commands agents plugins rules tools templates docs state; do
  mkdir -p "$GLOBAL_DIR/$d"
done

# Create minimal opencode.jsonc if missing
if [ ! -f "$GLOBAL_DIR/opencode.jsonc" ]; then
  cat > "$GLOBAL_DIR/opencode.jsonc" << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {},
  "instructions": [
    "AGENTS.md"
  ],
  "skills": {
    "paths": [
      "./.opencode/skills",
      "./skills"
    ]
  }
}
EOF
  echo "Created minimal opencode.jsonc"
fi

# Create minimal AGENTS.md if missing — do NOT overwrite existing
if [ ! -f "$GLOBAL_DIR/AGENTS.md" ]; then
  cat > "$GLOBAL_DIR/AGENTS.md" << 'EOF'
# OpenCode JOC

> Joint Operations Center - Multi-agent orchestration for OpenCode

## Quick Reference

Run `/init-project` to set up project configuration.
EOF
  echo "Created minimal AGENTS.md"
fi
```

If global JOC is missing essential pieces AND the user has no `.opencode/` project config, warn that global setup is incomplete and offer to continue anyway (local project config still works with a partial global install).

## Phase 1: Detection

**Skip if:** `--language` or `--skip-detection` flag

Delegate to `explore` agent. Scan project root for:

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Language detection
[ -f "package.json" ] && echo "TypeScript/JavaScript detected"
[ -f "tsconfig.json" ] && echo "TypeScript confirmed"
[ -f "pyproject.toml" ] && echo "Python detected"
[ -f "requirements.txt" ] && echo "Python (pip) detected"
[ -f "Cargo.toml" ] && echo "Rust detected"
[ -f "go.mod" ] && echo "Go detected"
[ -f "pom.xml" ] && echo "Java (Maven) detected"
[ -f "build.gradle" ] || [ -f "build.gradle.kts" ] && echo "Java (Gradle) detected"
[ -f "Gemfile" ] && echo "Ruby detected"

# Framework detection
grep -q '"next"' package.json 2>/dev/null && echo "Next.js detected"
grep -q '"react"' package.json 2>/dev/null && echo "React detected"
grep -q '"vue"' package.json 2>/dev/null && echo "Vue detected"
grep -q '"@angular/core"' package.json 2>/dev/null && echo "Angular detected"
grep -q '"fastapi"' pyproject.toml 2>/dev/null && echo "FastAPI detected"
grep -q '"django"' pyproject.toml 2>/dev/null && echo "Django detected"

# Build tools
[ -f "Makefile" ] && echo "Make detected"
[ -f "Dockerfile" ] && echo "Docker detected"
[ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] && echo "Docker Compose detected"

# Package manager
[ -f "pnpm-lock.yaml" ] && echo "pnpm detected"
[ -f "yarn.lock" ] && echo "yarn detected"
[ -f "bun.lockb" ] && echo "bun detected"
[ -f "package-lock.json" ] && echo "npm detected"
[ -f "uv.lock" ] && echo "uv detected"
[ -f "Pipfile.lock" ] && echo "pipenv detected"

# Key directories
echo "Directory structure:"
find "$PROJECT_ROOT" -maxdepth 2 -type d \
  ! -path '*/node_modules/*' ! -path '*/.git/*' ! -path '*/__pycache__/*' \
  ! -path '*/dist/*' ! -path '*/.next/*' ! -path '*/.venv/*' \
  | head -40
```

**Output:** Detection result object with language, framework, package manager, build system, key directories.

## Phase 2: Planning

**Skip if:** `--skip-detection` flag (use defaults)

Delegate to `planner` agent. Generate plan from detection result:

1. Determine which `.opencode/` files to create
2. Select language-appropriate rules templates
3. Plan AGENTS.md hierarchy scope
4. Identify agents to customize
5. Plan MCP servers to suggest

**Output:** Plan document with file list, rule selections, agent customizations.

## Phase 3: Scaffolding

Delegate to `executor` agent. Create the project structure:

### Directory Structure

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OPENCODE_DIR="$PROJECT_ROOT/.opencode"
STATE_DIR="$OPENCODE_DIR/state"

# Create directories
mkdir -p "$OPENCODE_DIR"
mkdir -p "$OPENCODE_DIR/agents"
mkdir -p "$OPENCODE_DIR/skills"
mkdir -p "$OPENCODE_DIR/commands"
mkdir -p "$OPENCODE_DIR/tools"
mkdir -p "$OPENCODE_DIR/rules"
mkdir -p "$OPENCODE_DIR/templates"
mkdir -p "$STATE_DIR"
mkdir -p "$STATE_DIR/state"
mkdir -p "$STATE_DIR/plans"
mkdir -p "$STATE_DIR/logs"
mkdir -p "$STATE_DIR/artifacts"
mkdir -p "$STATE_DIR/skills"
```

### .opencode/opencode.jsonc

Create project config extending global config. Key fields depend on detection:

- `instructions` — project-specific instruction files
- `skills.paths` — add `./.opencode/skills`
- `permission` — project-specific permissions
- `mcp` — project-specific MCP servers

### .opencode/AGENTS.md

Generate project-specific instructions:

```markdown
# {Project Name}

> {One-line description from detection}

## Architecture

{Detected architecture summary — language, framework, patterns}

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `src/` | {description} |

## Development

### Setup
{Package manager install and dev commands}

### Testing
{Test framework and commands}

### Build
{Build commands}

### Lint
{Lint commands, if detected}

## Conventions

{Language-specific conventions from rules/}

## For AI Agents

{Special instructions for agents working in this project}
```

### Rules

Create language-appropriate rules in `.opencode/rules/`:

| Detected Language | Rules Created |
|-------------------|---------------|
| TypeScript/JavaScript | `naming.md`, `patterns.md`, `conventions.md` |
| Python | `naming.md`, `patterns.md`, `conventions.md` |
| Rust | `naming.md`, `patterns.md`, `conventions.md` |
| Go | `naming.md`, `patterns.md` |
| Other | `conventions.md` only |

Rules content should be specific to the detected framework and patterns, not generic boilerplate.

### .gitignore Update

```bash
# Append to .gitignore if not already present
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

if [ -f "$PROJECT_ROOT/.gitignore" ]; then
  grep -q '.opencode/state/' "$PROJECT_ROOT/.gitignore" 2>/dev/null || {
    echo -e "\n# OpenCode JOC\n.opencode/state/\n.opencode/*.log" >> "$PROJECT_ROOT/.gitignore"
    echo "Updated .gitignore"
  }
else
  echo ".opencode/state/\n.opencode/*.log" > "$PROJECT_ROOT/.gitignore"
  echo "Created .gitignore"
fi
```

### Re-Run (IS_RERUN=true or --refresh)

When re-running on an existing project:

1. **Read existing** — parse current `.opencode/opencode.jsonc` and `AGENTS.md`
2. **Diff structure** — compare current directory tree vs what AGENTS.md describes
3. **Preserve manual edits** — keep `<!-- MANUAL -->` blocks in AGENTS.md files
4. **Update generated sections** — refresh file tables, directories, dependencies
5. **Add new detections** — add newly found files/dirs, mark removed ones
6. **Merge configs** — add new fields to opencode.jsonc, don't remove user-set values

## Phase 4: Documentation (Deepinit)

**Skip if:** `--minimal` or `--no-docs` flag

Delegate to `deepinit` skill. Generate hierarchical AGENTS.md files:

### Core Rules

1. Root AGENTS.md has **no parent tag**
2. All other AGENTS.md files include `<!-- Parent: {relative_path_to_parent}/AGENTS.md -->`
3. Process depth levels sequentially (parents before children)
4. Same-level directories process in parallel
5. Preserve `<!-- MANUAL: ... -->` sections in existing files
6. Skip empty directories (no files, no subdirectories)
7. Skip `node_modules/`, `.git/`, `dist/`, `build/`, `__pycache__/`, `.venv/`, `coverage/`

### Template

Each AGENTS.md follows this structure:

```markdown
<!-- Parent: {path} -->
<!-- Generated: {date} | Updated: {date} -->

# {Directory Name}

## Purpose
{One-paragraph description}

## Key Files
| File | Description |
|------|-------------|
| `file.ext` | Brief purpose |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `subdir/` | Description (see `subdir/AGENTS.md`) |

## For AI Agents

### Working In This Directory
{Special instructions}

### Common Patterns
{Code patterns used here}

## Dependencies
### Internal
{Internal deps}
### External
{External packages}

<!-- MANUAL: Preserved on regeneration -->
```

### Re-Run Behavior

When AGENTS.md files already exist:

1. Read and parse existing content
2. Identify auto-generated vs manual sections
3. Detect structural changes (new/removed files)
4. Update auto-generated content only
5. Preserve all manual annotations
6. Update timestamps

### Validation

After generation, verify:
- All parent references resolve to existing files
- No orphaned AGENTS.md files
- All significant directories have AGENTS.md
- Timestamps are current

## Phase 5: Context Capture

**Skip if:** Not `--full` mode

Promote accumulated knowledge into durable documentation:

### 5.1: Scan State Artifacts

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE_DIR="$PROJECT_ROOT/.opencode/state"

# Check for useful state artifacts
find "$STATE_DIR" -name "*.json" -o -name "*.md" 2>/dev/null | head -20

# Check for session logs with useful context
ls -la "$STATE_DIR/logs/" 2>/dev/null

# Check for existing plans
ls -la "$STATE_DIR/plans/" 2>/dev/null
```

### 5.2: Promote Insights

Invoke the `remember` skill to classify session knowledge:

1. **Project memory** (`project-memory.json`) — durable facts about this project
   - Build commands, test commands, key file locations
   - Architecture decisions, dependency relationships
   - Common pitfalls and solutions discovered

2. **Notepad** (`notepad.md`) — high-signal context for immediate use
   - Current task, recent decisions, active patterns

3. **AGENTS.md additions** — facts that belong in instruction files
   - Conventions, gotchas, project-specific patterns

### 5.3: Evaluate State Files

Review `.opencode/state/` for:

| File/Dir | Action |
|----------|--------|
| `plans/*.json` | Extract actionable decisions → project memory |
| `logs/*.log` | Scan for recurring errors → add to known issues |
| `skills/*/SKILL.md` | Review for relevance, promote to project skills |
| `artifacts/*` | Surface useful outputs, archive stale ones |

## Phase 6: Routing Optimization

**Skip if:** Not `--full` mode

Optimize agent routing based on project stack:

### 6.1: Stack-Appropriate Defaults

Based on detection results, configure `.opencode/opencode.jsonc` agent preferences:

| Stack | Recommended Primary Agents |
|-------|---------------------------|
| TypeScript/React | `executor`, `designer`, `test-engineer` |
| Python/FastAPI | `executor`, `scientist`, `test-engineer` |
| Rust | `executor`, `code-reviewer`, `verifier` |
| Go | `executor`, `architect`, `test-engineer` |
| Full-stack | `executor`, `architect`, `designer`, `test-engineer` |

### 6.2: Custom Agent Hints

Add project-specific agent hints to `.opencode/AGENTS.md`:

```markdown
## Agent Routing

For this {language}/{framework} project:
- **Implementation** → `executor` (default for coding tasks)
- **UI changes** → `designer` (React component work)
- **Bug investigation** → `debugger` (traces, stack analysis)
- **Architecture decisions** → `architect` (system design)
- **Security review** → `security-reviewer` (auth, input validation)
- **Testing** → `test-engineer` (test strategy, coverage)
```

### 6.3: MCP Server Suggestions

Based on project type, suggest MCP servers:

| Project Type | Suggested MCP |
|-------------|---------------|
| Any with GitHub | `context7` (already configured) |
| Web/REST API | REST client MCP |
| Database project | Database MCP |
| Infrastructure as Code | Terraform/cloud MCP |

## Phase 7: Verification

Delegate to `verifier` agent. Validate:

1. **Config loads** — `.opencode/opencode.jsonc` is valid JSON with comments
2. **AGENTS.md present** — root and key directories have AGENTS.md
3. **Parent refs resolve** — all `<!-- Parent: -->` paths point to existing files
4. **Rules valid** — `.opencode/rules/*.md` files exist and are non-empty
5. **State dirs exist** — all subdirectories of `.opencode/state/` created
6. **Gitignore updated** — `.opencode/state/` is gitignored
7. **Instructions referenced** — all files in `instructions` array exist

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OPENCODE_DIR="$PROJECT_ROOT/.opencode"

echo "=== Verification Report ==="

# Config validity
if python3 -c "import json,commentjson; commentjson.load(open('$OPENCODE_DIR/opencode.jsonc'))" 2>/dev/null || \
   node -e "const fs=require('fs'); JSON.parse(fs.readFileSync('$OPENCODE_DIR/opencode.jsonc','utf-8').replace(/\/\/.*$/gm,'').replace(/\/\*[\s\S]*?\*\//g,'')); console.log('valid')" 2>/dev/null; then
  echo "  ✓ opencode.jsonc is valid"
else
  echo "  ✗ opencode.jsonc has syntax errors"
fi

# AGENTS.md hierarchy
ROOT_AGENTS="$PROJECT_ROOT/AGENTS.md"
if [ -f "$ROOT_AGENTS" ]; then
  echo "  ✓ Root AGENTS.md exists"
else
  echo "  ✗ Root AGENTS.md missing"
fi

COUNT=$(find "$PROJECT_ROOT" -name "AGENTS.md" -type f ! -path '*/node_modules/*' ! -path '*/.git/*' | wc -l)
echo "  ℹ $COUNT AGENTS.md files across codebase"

# Parent refs
BROKEN=$(find "$PROJECT_ROOT" -name "AGENTS.md" -type f ! -path '*/node_modules/*' ! -path '*/.git/*' -exec grep -l '<!-- Parent:' {} \; | while read f; do
  PARENT=$(grep -o '<!-- Parent: [^ ]* -->' "$f" | sed 's/<!-- Parent: //;s/ -->//')
  TARGET="$(dirname "$f")/$PARENT"
  if [ ! -f "$TARGET" ]; then
    echo "$f → $PARENT (BROKEN)"
  fi
done)

if [ -z "$BROKEN" ]; then
  echo "  ✓ All parent references valid"
else
  echo "  ✗ Broken parent refs:"
  echo "$BROKEN"
fi

# State dirs
for d in state plans logs artifacts skills; do
  if [ -d "$OPENCODE_DIR/state/$d" ]; then
    echo "  ✓ state/$d/"
  else
    echo "  ✗ state/$d/ missing"
  fi
done

# Gitignore
if grep -q '.opencode/state/' "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
  echo "  ✓ .gitignore includes .opencode/state/"
else
  echo "  ⚠ .gitignore missing .opencode/state/"
fi

echo "=== Verification Complete ==="
```

## Output

After all phases complete, display:

```
✓ Project initialized: {project_name}

Detected:
  Language:   {language}
  Framework:  {framework}
  Package:    {pkg_manager}
  Build:      {build_system}

Created/Updated:
  .opencode/opencode.jsonc     {status}
  .opencode/AGENTS.md          {status}
  .opencode/rules/*.md         {count} files
  .opencode/state/             {status}
  AGENTS.md hierarchy          {count} files across codebase
  .gitignore                   {status}

{If --full mode:}
  Project memory              {status}
  Agent routing                {status}
  MCP suggestions              {status}

Next steps:
  1. Review .opencode/AGENTS.md and customize for your project
  2. Run /init-project --refresh after major changes
  3. Commit .opencode/ to version control
```

## Idempotency

This command is **safe to re-run**. It:

- Preserves `<!-- MANUAL -->` blocks in AGENTS.md files
- Merges new fields into opencode.jsonc without removing user values
- Only adds new AGENTS.md files, updates existing ones in-place
- Detects and respects existing configuration
- Never deletes user-created project skills, agents, or commands
- Archives stale state artifacts instead of deleting them

## Resume on Failure

If a phase fails, save checkpoint:

```bash
mkdir -p "$OPENCODE_DIR/state"
echo "{\"lastCompletedPhase\":$COMPLETED_PHASE,\"timestamp\":\"$(date -Iseconds)\"}" > "$OPENCODE_DIR/state/init-checkpoint.json"
```

Resume with `/init-project --force` or `/init-project --refresh`.

## Related

- `deepinit` skill — Standalone docs generation (called by Phase 4)
- `remember` skill — Context promotion (called by Phase 5)
- `wiki` skill — Persistent knowledge base (used by Phase 5)
- `mcp-setup` skill — MCP server configuration
- `joc-doctor` skill — Diagnose installation issues