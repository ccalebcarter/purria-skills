# Purria Skills

A collection of Claude Code skills for game development, specifically designed for **Farming in Purria** - a cozy gambling tycoon game.

## Overview

These skills provide specialized expertise for building games that combine:
- 🌾 Farming simulation mechanics
- 🎰 Casino/betting systems
- 🤖 Robot companions (Simulins)
- 🎨 Stylized game art

## Skills

### Game Design

| Skill | Description |
|-------|-------------|
| [casino-math-balancer](skills/casino-math-balancer) | RTP, odds, house edge, payout calculations |
| [game-concept-advisor](skills/game-concept-advisor) | Mechanic brainstorming, cross-domain inspiration |
| [game-systems-doc](skills/game-systems-doc) | GDD writing, feature specs, documentation |
| [fun-advisor](skills/fun-advisor) | Player psychology, engagement, fun evaluation |

### Development

| Skill | Description |
|-------|-------------|
| [drizzle-game-schema](skills/drizzle-game-schema) | Database schemas for games with Drizzle ORM |
| [zustand-game-patterns](skills/zustand-game-patterns) | State management, persistence, undo/redo |
| [react-game-ui](skills/react-game-ui) | Game UI components, animations, HUDs |
| [hexgrid-algorithms](skills/hexgrid-algorithms) | Hex math, pathfinding, coordinate systems |

### Assets & Art

| Skill | Description |
|-------|-------------|
| [gemini-image-generator](skills/gemini-image-generator) | AI image generation with Google Gemini |
| [game-assets-team](skills/game-assets-team) | Art direction, asset pipeline, style guides |

### Quality & Setup

| Skill | Description |
|-------|-------------|
| [testing-team](skills/testing-team) | QA, playtesting, unit/E2E testing |
| [purria-starter](skills/purria-starter) | Project setup, environment validation |

## MCP Servers

| Server | Description |
|--------|-------------|
| [recraft](mcp-servers/recraft) | Background removal and SVG vectorization |

## Asset Pipeline

The full asset creation workflow:

```
┌─────────────────────────────────────────────────────────────┐
│                    ASSET PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CONCEPT         2. GENERATE       3. PROCESS           │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│  │game-asset│  →   │  gemini  │  →   │ recraft  │          │
│  │  -team   │      │generator │      │   API    │          │
│  └──────────┘      └──────────┘      └──────────┘          │
│  Art brief         PNG output        Remove BG             │
│  Style guide       1-2 MB            Vectorize             │
│                                      → SVG                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### 1. Clone this repo

```bash
git clone https://github.com/ccalebcarter/purria-skills.git
```

### 2. Copy skills to Claude Code

```bash
# Copy all skills
cp -r purria-skills/skills/* ~/.claude/skills/

# Or symlink for easier updates
ln -s $(pwd)/purria-skills/skills/* ~/.claude/skills/
```

### 3. Set up API keys

```bash
# Add to your shell profile
export GEMINI_API_KEY="your-gemini-api-key"
export RECRAFT_API_KEY="your-recraft-api-key"
```

### 4. Set up Python environment (for image generation)

```bash
cd ~/.claude/skills/gemini-image-generator/scripts
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 5. Validate setup

```bash
python ~/.claude/skills/purria-starter/scripts/validate-setup.py
```

## Usage in Claude Code

Skills are invoked with `/skill-name`:

```
/casino-math-balancer
"Calculate RTP for a 5-reel slot machine..."

/game-concept-advisor
"Brainstorm mechanics for a fishing minigame..."

/fun-advisor
"Is this progression system fun or grindy?"

/gemini-image-generator
"Generate a Simulin robot character..."
```

## Tech Stack

These skills are designed for projects using:

- **Monorepo**: Turborepo + Bun
- **Frontend**: React 19 + TanStack Router + Vite
- **Backend**: Hono + tRPC
- **Database**: SQLite/Turso + Drizzle ORM
- **Auth**: better-auth
- **State**: Zustand + Immer
- **Styling**: Tailwind v4 + shadcn/ui
- **Testing**: Playwright
- **AI Images**: Google Gemini + Recraft

## Project: Farming in Purria

These skills were created for **Farming in Purria v3**, featuring:

- 🗓️ 42-day seasonal farming cycles
- 🃏 Video poker-inspired betting (Meta Pots)
- 🤖 Robot companions called Simulins
- 🏘️ Living valley with NPCs
- 🎨 Soft stylized 3D cartoon art style

## Contributing

1. Fork this repository
2. Create a new skill in `skills/your-skill-name/`
3. Add a `SKILL.md` (Claude reads this) and `README.md` (humans read this)
4. Submit a PR

### Skill Structure

```
skills/
└── your-skill-name/
    ├── SKILL.md      # Instructions for Claude
    ├── README.md     # Documentation for humans
    ├── scripts/      # Optional automation scripts
    └── references/   # Optional reference materials
```

## License

MIT - Use freely in your game projects.

---

Built with Claude Code for game developers who want AI-assisted game creation.
