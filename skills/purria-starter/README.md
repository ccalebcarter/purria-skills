# Purria Starter

Complete setup guide for new Farming in Purria project versions.

## Expertise

This skill provides:

- **Environment Setup**: Prerequisites, API keys, env files
- **Project Initialization**: Monorepo structure, dependencies
- **MCP Configuration**: Browser automation, tool connections
- **Skills Installation**: Setting up all Purria skills
- **Validation Scripts**: Automated setup checking
- **Troubleshooting**: Common issues and solutions

## When to Use

Invoke this skill when you need to:

- Start a new version/iteration of the project
- Set up development environment on a new machine
- Validate all systems are configured correctly
- Onboard new team members
- Troubleshoot configuration issues

## Quick Start

### 1. Prerequisites

```bash
# Check all prerequisites
bun --version    # 1.0+
node --version   # 20+
python --version # 3.8+
git --version    # 2.0+
```

### 2. Clone and Install

```bash
git clone <repo-url> fipcc003
cd fipcc003
bun install
```

### 3. Environment Setup

```bash
# Run the environment initializer
python scripts/init-env.py
```

Or manually create:

**apps/server/.env:**
```env
BETTER_AUTH_SECRET=<generate-32-char-secret>
BETTER_AUTH_URL=http://localhost:5172
CORS_ORIGIN=http://localhost:5173
DATABASE_URL=file:../../local.db
```

**apps/web/.env:**
```env
VITE_SERVER_URL=http://localhost:5172
```

### 4. API Keys

```bash
export GEMINI_API_KEY="your-gemini-key"
export RECRAFT_API_KEY="your-recraft-key"
```

### 5. Database

```bash
bun db:push
```

### 6. Validate

```bash
python scripts/validate-setup.py
```

### 7. Run

```bash
bun dev
# Open http://localhost:5173
```

## Scripts

| Script | Purpose |
|--------|---------|
| `validate-setup.py` | Check all 18 setup requirements |
| `init-env.py` | Create template .env files |
| `test-asset-pipeline.py` | Test Gemini → Recraft → SVG |

## Validation Checklist

The validator checks:

- [ ] Bun installed
- [ ] Node.js installed
- [ ] Python installed
- [ ] Git installed
- [ ] GEMINI_API_KEY set
- [ ] RECRAFT_API_KEY set
- [ ] Project structure valid
- [ ] Environment files exist
- [ ] Skills installed
- [ ] Python venv ready

## Tech Stack Reference

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

## Common Commands

```bash
bun dev              # Start all apps
bun run build        # Production build
bun check-types      # TypeScript check
bun db:push          # Apply schema
bun db:studio        # Open Drizzle Studio
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Check CORS_ORIGIN port |
| Auth fails | Check BETTER_AUTH_URL |
| DB errors | Run bun db:push |
| API key errors | Check environment variables |

## Integration

This skill works alongside:

- All other Purria skills
- MCP servers (claude-in-chrome)
- Gemini and Recraft APIs

## Usage in Claude Code

```
/purria-starter

"Set up a new Purria development environment..."
"Validate my current setup..."
"Troubleshoot authentication issues..."
```
