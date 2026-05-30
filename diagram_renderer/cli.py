"""CLI entry point for the Cyberknight Diagram Renderer.

Usage:
    cyberknight-diagram-render architecture.md
    cyberknight-diagram-render --size 4K --output diagram.png spec.md
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path

import requests

from diagram_renderer.style_guard import wrap


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyberknight-diagram-render",
        description="Render architecture diagrams via Nano Banana Pro / OpenRouter",
    )
    parser.add_argument("input", help="Path to the Markdown source file")
    parser.add_argument(
        "--title",
        default=None,
        help="Diagram title (defaults to H1 text or filename stem)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        choices=["1:1", "4:3", "16:9", "21:9", "9:16", "3:4"],
        help="Output aspect ratio (default: 16:9)",
    )
    parser.add_argument(
        "--size",
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Output resolution size (default: 2K)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output PNG path (default: <input-stem>.png)",
    )
    parser.add_argument(
        "--model",
        default="google/gemini-3-pro-image-preview",
        help="OpenRouter model ID (default: google/gemini-3-pro-image-preview)",
    )
    parser.add_argument(
        "--save-prompt",
        action="store_true",
        help="Also write the assembled prompt to <stem>.prompt.txt",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output",
    )
    return parser


def _resolve_title(input_path: Path, user_title: str | None) -> str:
    if user_title:
        return user_title
    # Try to extract H1 from the Markdown file
    text = input_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return input_path.stem.replace("-", " ").replace("_", " ").title()


def _resolve_output(input_path: Path, user_output: str | None) -> Path:
    if user_output:
        return Path(user_output)
    return input_path.with_suffix(".png")


def _call_openrouter(
    prompt: str,
    model: str,
    aspect_ratio: str,
    size: str,
    title: str,
) -> list[bytes]:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY environment variable is not set.\n"
            "Get a key at https://openrouter.ai/settings/keys"
        )

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": aspect_ratio,
            "image_size": size,
        },
    }

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://cyberknight-websites.com",
            "X-Title": title,
        },
        json=payload,
        timeout=180,
    )

    if resp.status_code != 200:
        raise RuntimeError(
            f"OpenRouter returned HTTP {resp.status_code}: {resp.text[:500]}"
        )

    data = resp.json()
    choices = data.get("choices", [])
    if not choices:
        error = data.get("error", "unknown")
        raise RuntimeError(f"OpenRouter returned no choices. Error: {error}")

    message = choices[0].get("message", {})
    images = message.get("images", [])
    if not images:
        raise RuntimeError("No images in OpenRouter response.")

    pngs: list[bytes] = []
    for img in images:
        url = img.get("image_url", {}).get("url", "")
        if url.startswith("data:image"):
            b64 = url.split(",", 1)[1]
            pngs.append(base64.b64decode(b64))
        else:
            raise RuntimeError(f"Unexpected image URL format: {url[:80]}...")

    return pngs


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    title = _resolve_title(input_path, args.title)
    output_path = _resolve_output(input_path, args.output)

    user_markdown = input_path.read_text(encoding="utf-8")
    full_prompt = wrap(user_markdown)

    if args.save_prompt:
        prompt_path = output_path.with_suffix(".prompt.txt")
        prompt_path.write_text(full_prompt, encoding="utf-8")
        if not args.quiet:
            print(f"Prompt saved to {prompt_path}")

    if not args.quiet:
        print(f"Rendering diagram: {title}")
        print(f"Model: {args.model}")
        print(f"Size: {args.size}  Aspect ratio: {args.aspect_ratio}")

    try:
        pngs = _call_openrouter(
            prompt=full_prompt,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            size=args.size,
            title=title,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    for i, png_data in enumerate(pngs):
        if i == 0 and len(pngs) == 1:
            out = output_path
        else:
            suffix = f"-{i + 1}" if len(pngs) > 1 else ""
            out = output_path.with_stem(output_path.stem + suffix)
        out.write_bytes(png_data)
        if not args.quiet:
            print(f"MEDIA: {out}")


if __name__ == "__main__":
    main()
