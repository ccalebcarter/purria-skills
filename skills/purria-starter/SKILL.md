# Purria Starter

Complete setup guide for new Farming in Purria project versions. Use this skill when starting a fresh build, onboarding to the project, or validating that all systems are configured correctly.

## When to Use

- Starting a new version/iteration of Farming in Purria
- Setting up development environment on a new machine
- Validating all dependencies, APIs, and MCP servers are working
- Troubleshooting configuration issues
- Onboarding new team members

## Quick Start Checklist

Run through this checklist to validate your setup:

```
[ ] Prerequisites installed (Bun, Node, Python, Git)
[ ] Repository cloned and dependencies installed
[ ] Environment variables configured
[ ] MCP servers connected (claude-in-chrome)
[ ] API keys set (GEMINI_API_KEY, RECRAFT_API_KEY)
[ ] Database initialized
[ ] Dev servers running
[ ] Asset pipeline validated
```

---

## Phase 1: Prerequisites

### Required Software

| Software | Version | Check Command | Install |
|----------|---------|---------------|---------|
| Bun | 1.0+ | `bun --version` | [bun.sh](https://bun.sh) |
| Node.js | 20+ | `node --version` | [nodejs.org](https://nodejs.org) |
| Python | 3.8+ | `python --version` | [python.org](https://python.org) |
| Git | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com) |

### Verify Prerequisites

```bash
# Run all checks
bun --version && node --version && python --version && git --version
```

---

## Phase 2: Project Setup

### Clone and Install

```bash
# Clone repository (replace with actual repo URL)
git clone <repo-url> fipcc003
cd fipcc003

# Install dependencies
bun install
```

### Project Structure

```
fipcc003/
├── apps/
│   ├── web/           # React frontend (port 5173)
│   └── server/        # Hono API server (port 5172)
├── packages/
│   ├── api/           # tRPC routers
│   ├── auth/          # better-auth config
│   ├── db/            # Drizzle schema
│   ├── config/        # Shared TypeScript config
│   └── env/           # Environment validation
├── .claude/           # Claude Code settings
├── CLAUDE.md          # Project instructions
└── reports/           # Sprint reports
```

---

## Phase 3: Environment Configuration

### Server Environment (`apps/server/.env`)

```env
# Authentication (generate with: openssl rand -base64 32)
BETTER_AUTH_SECRET=<your-32+-character-secret>
BETTER_AUTH_URL=http://localhost:5172

# CORS
CORS_ORIGIN=http://localhost:5173

# Database
DATABASE_URL=file:../../local.db
```

### Web Environment (`apps/web/.env`)

```env
VITE_SERVER_URL=http://localhost:5172
```

### Global API Keys (Shell Profile)

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or PowerShell `$PROFILE`):

```bash
# Google AI Studio - for image generation
export GEMINI_API_KEY="your-gemini-api-key"

# Recraft.ai - for background removal and vectorization
export RECRAFT_API_KEY="your-recraft-api-key"
```

**Get API Keys:**
- Gemini: [Google AI Studio](https://aistudio.google.com/apikey)
- Recraft: [Recraft.ai](https://recraft.ai)

---

## Phase 4: MCP Server Configuration

### Claude in Chrome (Browser Automation)

The `claude-in-chrome` MCP enables browser automation for testing and validation.

**Setup:**
1. Install the Claude in Chrome extension from Chrome Web Store
2. The MCP server auto-connects when Claude Code is running
3. Verify with: `tabs_context_mcp` tool should return available tabs

**Capabilities:**
- Screenshot capture
- Page navigation
- Form interaction
- DOM reading
- JavaScript execution
- Network request monitoring

### Claude Code Settings (`.claude/settings.json`)

```json
{
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "Glob(*)",
      "Grep(*)",
      "mcp__claude-in-chrome__*"
    ]
  }
}
```

---

## Phase 5: Skills Installation

### Required Skills

These skills should be in `~/.claude/skills/`:

| Skill | Purpose | Setup |
|-------|---------|-------|
| `gemini-image-generator` | AI image generation | Python venv + GEMINI_API_KEY |
| `purria-starter` | This skill - project setup | Already installed |

### Game Development Skills (Built-in)

These are invoked via `/skill-name` in Claude Code:

| Skill | When to Use |
|-------|-------------|
| `drizzle-game-schema` | Database schema design |
| `zustand-game-patterns` | State management |
| `hexgrid-algorithms` | Hex grid math/rendering |
| `react-game-ui` | Game UI components |
| `casino-math-balancer` | Betting/odds calculations |
| `game-concept-advisor` | Mechanic brainstorming |
| `fun-advisor` | Evaluating if features are fun |
| `testing-team` | QA and testing |
| `game-assets-team` | Complete asset pipeline |

### Gemini Image Generator Setup

```bash
cd ~/.claude/skills/gemini-image-generator/scripts

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (Unix)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Phase 6: Database Initialization

### Initialize Database

```bash
cd fipcc003

# Push schema to database
bun db:push

# Verify with Drizzle Studio
bun db:studio
```

### Database Commands

| Command | Purpose |
|---------|---------|
| `bun db:push` | Apply schema changes |
| `bun db:studio` | Open Drizzle Studio GUI |
| `bun db:generate` | Generate migrations |
| `bun db:migrate` | Run migrations |

---

## Phase 7: Development Servers

### Start All Services

```bash
# Start both web and server
bun dev

# Or individually:
bun dev:web     # Frontend on :5173
bun dev:server  # Backend on :5172
```

### Verify Services

| Service | URL | What to Check |
|---------|-----|---------------|
| Frontend | http://localhost:5173 | Page loads, no console errors |
| Backend | http://localhost:5172 | API responds |
| tRPC | http://localhost:5172/trpc | tRPC panel (if enabled) |
| Auth | http://localhost:5172/api/auth | Auth endpoints |

---

## Phase 8: Asset Pipeline Validation

### Full Pipeline Test

The asset pipeline creates scalable vector UI assets:

```
Gemini Generate → Recraft Remove BG → Recraft Vectorize → SVG Asset
```

### Test Commands

```bash
# Set API keys first
export GEMINI_API_KEY="your-key"
export RECRAFT_API_KEY="your-key"

# Step 1: Generate image
python ~/.claude/skills/gemini-image-generator/scripts/generate.py \
  --prompt "A cute friendly robot companion, soft stylized 3D cartoon" \
  --reference ~/Downloads/sampleart.png \
  --output test-asset.png

# Step 2: Remove background
python ~/.claude/skills/gemini-image-generator/scripts/recraft_process.py \
  --action remove-bg \
  --input test-asset.png \
  --output test-asset-nobg.png

# Step 3: Vectorize
python ~/.claude/skills/gemini-image-generator/scripts/recraft_process.py \
  --action vectorize \
  --input test-asset-nobg.png \
  --output test-asset.svg
```

### Expected Output

| File | Size Range | Format |
|------|------------|--------|
| `test-asset.png` | 500KB - 2MB | Raster with background |
| `test-asset-nobg.png` | 300KB - 1MB | Transparent PNG |
| `test-asset.svg` | 200KB - 500KB | Scalable vector |

---

## Phase 9: Build Verification

### Type Checking

```bash
bun check-types
```

### Production Build

```bash
bun run build
```

### E2E Tests

```bash
cd apps/web
bunx playwright test
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS errors | Mismatched ports | Check `CORS_ORIGIN` matches web port |
| Auth fails | Wrong URL | Verify `BETTER_AUTH_URL` is server port |
| DB errors | Schema out of sync | Run `bun db:push` |
| Type errors | Missing types | Run `bun check-types` to see all |
| API key errors | Not set | Check `echo $GEMINI_API_KEY` |
| MCP not connected | Extension issue | Restart Chrome, check extension |

### Port Conflicts

If default ports are in use:

```bash
# Check what's using a port
# Windows
netstat -ano | findstr :5173

# Unix
lsof -i :5173
```

### Reset Database

```bash
# Delete and recreate
rm local.db
bun db:push
```

---

## Validation Checklist

Run this final checklist to confirm everything works:

```bash
# 1. Prerequisites
bun --version && node --version && python --version

# 2. Dependencies
cd fipcc003 && bun install

# 3. Environment
cat apps/server/.env | head -3
cat apps/web/.env

# 4. API Keys
echo "Gemini: ${#GEMINI_API_KEY} chars"
echo "Recraft: ${#RECRAFT_API_KEY} chars"

# 5. Database
bun db:push

# 6. Type Check
bun check-types

# 7. Build
bun run build

# 8. Dev Server
bun dev
```

### Browser Validation (Manual)

1. Open http://localhost:5173
2. Check browser console for errors
3. Test authentication flow
4. Verify API calls work

---

## Project Configuration Reference

### Tech Stack

| Layer | Technology |
|-------|------------|
| Monorepo | Turborepo + Bun |
| Frontend | React 19 + TanStack Router + Vite |
| Backend | Hono + tRPC |
| Database | SQLite/Turso + Drizzle ORM |
| Auth | better-auth |
| State | Zustand + Immer |
| Styling | Tailwind v4 + shadcn/ui |
| Testing | Playwright |
| Images | Gemini AI + Recraft |

### Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project instructions for Claude |
| `turbo.json` | Turborepo pipeline config |
| `packages/db/src/schema/` | Database schemas |
| `packages/api/src/routers/` | API endpoints |
| `apps/web/src/routes/` | Frontend pages |
| `apps/web/src/stores/` | Zustand stores |

---

## Next Steps After Setup

1. **Read CLAUDE.md** - Understand project conventions
2. **Review existing schemas** - `packages/db/src/schema/`
3. **Check current routes** - `apps/web/src/routes/`
4. **Run the game** - `bun dev` and open http://localhost:5173
5. **Generate test assets** - Use the asset pipeline

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2025-01-10 | Initial skill creation |
