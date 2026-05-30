# cyberknight-diagram-renderer

Architecture diagram generator powered by Nano Banana Pro via OpenRouter.
Produces flat, modern UI-style PNGs from Markdown source files.

## Prerequisites

- **Python 3.10+**
- **uv** — The fast Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **OpenRouter API key** — Get one at https://openrouter.ai/settings/keys

## Installation

```bash
git clone git@github.com:Cyberknight-Websites/cyberknight-diagram-renderer.git
cd cyberknight-diagram-renderer
uv tool install --editable .
```

This makes `cyberknight-diagram-render` globally available on your system.

To upgrade after pulling changes:

```bash
uv tool install --editable . --force
```

## Usage

```bash
# Set your API key
export OPENROUTER_API_KEY="sk-or-v1-..."

# Render a diagram from Markdown
cyberknight-diagram-render architecture.md

# Override size and output path
cyberknight-diagram-render --size 4K --output diagram.png spec.md

# Save the assembled prompt for debugging
cyberknight-diagram-render --save-prompt spec.md
```

PNG is written alongside the source `.md` file by default (e.g. `architecture.png`).

## Markdown input format

The `.md` file is both **documentation** and **the prompt**.  
You describe the diagram in natural prose — zones, colors, services, layout — and
the tool wraps it with a hardcoded visual style specification before sending it
to the image generation model.

### Example: `architecture-overview.md`

```markdown
# Cyberknight Architecture Overview

Three horizontal rows on a very light gray background.

## Row 1 — Cloudflare Edge

Full-width zone. Border: #F38020. Fill: #FFF5EB.
Label: "CLOUDFLARE EDGE — zone: cyberknight-websites.com"

Contains four equally spaced cards:
- "DNS — cyberknight-websites.com" — icon: cloudflare
- "cyberknight-sites-worker" — icon: worker
- "cyberknight-cdn-worker" — icon: worker
- "cyberknight-secure (Tunnel)" — icon: cloudflare

## Row 2 — izumi server and AWS

### izumi (Debian 13)

Large zone. Border: #4B5563. Fill: #F4F4F4.
Label: "izumi (Debian 13)"

Top row inside izumi:
- "NGINX" — icon: nginx
- "Webhooks"
- "VPN Access" — icon: shield

Below that, four Docker containers as vertical stacks:

**Secure Webapp**
1. supervisord (PID 1)
2. Waitress + Flask — icon: python
3. cloudflared — icon: cloudflare

**Secure Webapp (test)**
1. supervisord (PID 1)
2. Waitress + Flask — icon: python

**Council Builder**
1. Sync Data Script — icon: ruby
2. Jekyll — icon: jekyll

**Website Builder**
1. Python + Claude Agent SDK — icon: python
2. Jekyll — icon: jekyll
3. Chromium — icon: chrome

### AWS — us-east-1

Zone. Border: #232F3E. Fill: #FFF8E5.
Label: "AWS — us-east-1"

Grid of four cards:
- cyberknight-public-files — icon: cylinder
- cyberknight-private-files — icon: cylinder
- cyberknight-websites — icon: cylinder
- cyberknight-downtime-checker-lambda — icon: lambda

Below that, three side-by-side sub-zones:
- CODE STORAGE — containing GitHub — icon: github
- SECRET STORAGE — containing Doppler — icon: doppler
- EMAIL — containing Postmark — icon: envelope

## Row 3 — Azure and LLM Providers

### AZURE

Zone. Border: #0078D4. Fill: #E6F2FA.
Label: "AZURE"

Cards:
- Azure Cosmos DB — icon: globe
- Azure Communication — icon: envelope
- Azure AI Vision — icon: eye
- Azure Blob Storage — icon: cylinder

### LLM PROVIDERS

Zone. Border: #6D28D9. Fill: #FAF5FF.
Label: "LLM PROVIDERS"

Cards:
- OpenAI — icon: openai
- Anthropic — icon: anthropic
- Google — icon: google
```

### What you control in the `.md` file

| You write | The tool handles |
|---|---|
| Zone names, labels, service names | Typography (size, weight, placement) |
| Hex colors for borders and fills | Box styling (radius, stroke width, padding, gaps) |
| Structure: rows, zones, grids, stacks | Layout mechanics (alignment, margins, spacing) |
| Icon hints (`icon: python`) | Icon style (flat, 24px, left-aligned, color rules) |
| Natural prose descriptions | Visual guard rails (no photorealism, no watermarks) |

## CLI options

| Flag | Default | Description |
|---|---|---|
| `--title` | H1 or filename | Diagram title |
| `--aspect-ratio` | `16:9` | Output aspect ratio |
| `--size` | `2K` | Resolution: `1K`, `2K`, or `4K` |
| `--output` | `<stem>.png` | Output PNG path |
| `--model` | `google/gemini-3-pro-image-preview` | OpenRouter model ID |
| `--save-prompt` | — | Write assembled prompt to `<stem>.prompt.txt` |
| `--quiet` | — | Suppress non-error output |

## Development

```bash
uv sync
uv run cyberknight-diagram-render examples/architecture-overview.md
```

## License

MIT — see [LICENSE](LICENSE).
