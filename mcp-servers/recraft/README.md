# Recraft API Integration

Image processing tools using the [Recraft.ai](https://recraft.ai) API for background removal and SVG vectorization.

## Overview

Recraft provides professional-grade image processing capabilities:

- **Background Removal**: Clean transparent cutouts for game sprites and UI elements
- **SVG Vectorization**: Convert raster images to scalable vector graphics

## Why Recraft?

| Feature | Benefit for Game Dev |
|---------|---------------------|
| Clean edge detection | Professional sprite cutouts |
| SVG output | Resolution-independent UI assets |
| Fast processing | Rapid iteration on game art |
| High quality | Production-ready assets |

## Setup

### 1. Get API Key

1. Visit [Recraft.ai](https://recraft.ai)
2. Create an account
3. Navigate to API settings
4. Generate an API key

### 2. Set Environment Variable

**Unix/macOS:**
```bash
export RECRAFT_API_KEY="your-api-key-here"
```

**Windows PowerShell:**
```powershell
$env:RECRAFT_API_KEY = "your-api-key-here"
```

**Permanent (add to shell profile):**
```bash
# ~/.bashrc, ~/.zshrc, or PowerShell $PROFILE
export RECRAFT_API_KEY="your-api-key-here"
```

### 3. Install Dependencies

```bash
pip install requests
```

## Usage

### Remove Background

Removes the background from an image, creating a transparent PNG.

```bash
python recraft_process.py \
  --action remove-bg \
  --input character.png \
  --output character-nobg.png
```

**Input:** Any image (PNG, JPG)
**Output:** PNG with transparent background

### Vectorize Image

Converts a raster image to SVG format for scalable UI.

```bash
python recraft_process.py \
  --action vectorize \
  --input icon-nobg.png \
  --output icon.svg
```

**Input:** PNG (ideally with transparent background)
**Output:** SVG vector file

## Asset Pipeline Integration

This tool is designed to work with the Gemini Image Generator in a full asset pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                    ASSET PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. GENERATE          2. REMOVE BG        3. VECTORIZE     │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐      │
│  │  Gemini  │   →    │ Recraft  │   →    │ Recraft  │      │
│  │   API    │        │   API    │        │   API    │      │
│  └──────────┘        └──────────┘        └──────────┘      │
│       ↓                   ↓                   ↓             │
│   concept.png      sprite-nobg.png       sprite.svg        │
│   (1-2 MB)          (300-800 KB)        (200-500 KB)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Full Pipeline Example

```bash
# Step 1: Generate with Gemini
python generate.py \
  --prompt "Cute robot companion, soft 3D cartoon style" \
  --reference style-guide.png \
  --output robot.png

# Step 2: Remove background
python recraft_process.py \
  --action remove-bg \
  --input robot.png \
  --output robot-nobg.png

# Step 3: Vectorize for UI
python recraft_process.py \
  --action vectorize \
  --input robot-nobg.png \
  --output robot.svg
```

## API Reference

### Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/images/removeBackground` | Background removal |
| `POST /v1/images/vectorize` | SVG conversion |

### Response Format

```json
{
  "image": {
    "url": "https://...",
    "width": 1024,
    "height": 1024
  }
}
```

## Best Practices

### For Background Removal

- Use images with clear subject/background separation
- Higher contrast edges produce cleaner results
- Works best with solid or simple backgrounds

### For Vectorization

- Remove background first for best results
- Simpler images vectorize more cleanly
- Icons and UI elements work better than complex scenes

### File Size Guidelines

| Asset Type | Recommended Size |
|------------|------------------|
| Icons | 256x256 - 512x512 |
| UI Elements | 512x512 - 1024x1024 |
| Characters | 1024x1024 - 2048x2048 |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check RECRAFT_API_KEY |
| 403 Forbidden | API key restrictions | Check account permissions |
| 413 Payload Too Large | Image too big | Resize to < 10MB |
| Empty response | Processing failed | Try simpler image |

## Cost Considerations

Recraft API has usage-based pricing. Check [recraft.ai/pricing](https://recraft.ai) for current rates.

**Tips to minimize costs:**
- Batch process during development
- Cache processed assets
- Only re-process when source changes

## Integration with Claude Code

This script is designed to be called from Claude Code during asset creation workflows. The `game-assets-team` and `gemini-image-generator` skills reference this tool.

```
# Claude Code can run:
python mcp-servers/recraft/recraft_process.py --action remove-bg ...
```

## License

MIT - Use freely in your game projects.
