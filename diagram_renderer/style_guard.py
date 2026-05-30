"""Hardcoded visual language specification injected around user Markdown."""

from __future__ import annotations

PREAMBLE = """\
Create a clean, flat, modern UI-style system architecture diagram.

The following user-provided description defines the diagram content,
structure, colors, and layout. You MUST follow it EXACTLY.

=== GLOBAL STYLE RULES (override nothing above) ===
- The diagram MUST be a flat 2D infographic. NEVER photorealistic,
  3D, isometric, skeuomorphic, or cinematic.
- Background of the entire canvas: #FAFBFC.
- ALL text MUST be crisp sans-serif, fully legible, correctly spelled.
- NO watermarks, signatures, decorative flourishes, drop shadows,
  lens flares, or gradients.

=== BOX SPECIFICATION (applies to every card / box / item) ===
- Every box is a rounded rectangle with 8px corner radius.
- Every box has a 2px solid stroke in the color of its parent zone's
  border, unless the user specifies a different box border color.
- Box fill is white unless the user specifies otherwise.
- Inside each box:
  - A small flat icon (24×24px equivalent) is placed at the LEFT edge,
    vertically centered, with 12px padding from the left border.
  - The title text is placed to the RIGHT of the icon, vertically
    centered, in bold 14px weight, with 10px gap between icon and text.
  - If the box has no icon, the title text is left-aligned with
    12px padding from the left border.
- Box minimum height: 56px. Minimum internal padding: 12px all sides.
- Equal horizontal and vertical gap between adjacent boxes: 16px.

=== ZONE SPECIFICATION ===
- Every zone is a rounded rectangle with 14px border radius.
- Zone border is 3px solid in the color provided by the user.
- Zone fill is the pale tint provided by the user.
- Zone label is rendered as a pill/badge at the TOP-LEFT corner:
  - Pill shape (fully rounded ends, like a capsule).
  - Fill: the zone's border color.
  - Text: white, bold, 12px sans-serif.
  - Padding: 6px 16px.
  - The pill slightly overlaps the zone border (half inside, half outside).

=== CONTAINER SPECIFICATION (nested boxes, e.g. Docker containers) ===
- A container is a rounded rectangle with 10px radius.
- It has a thick 3px border in the user's specified color.
- It has a pale fill in the user's specified color.
- Container title is at top-left in bold, with a small icon beside it.
- Inside the container, child boxes are stacked vertically with 12px gaps.
  Each child follows the BOX SPECIFICATION above.

=== LAYOUT SPECIFICATION ===
- The diagram is organized into rows as described by the user.
- Within a row, zones are laid out left-to-right with equal spacing.
- Within a zone, cards are laid out according to the user's description
  (horizontal flow, vertical stack, or grid).
- The entire composition is centered on the canvas with comfortable
  margins (minimum 40px from all edges).
- All elements are aligned to an invisible 8px grid.

=== ICON SPECIFICATION ===
- Icons are simple, flat, single-color vector-style marks.
- Icon color matches the box border color unless the user specifies
  a brand color (e.g., Google multicolor "G", Chrome circle).
- Icons are never photorealistic or 3D.

=== USER DESCRIPTION ===
"""

POSTAMBLE = """\
=== END USER DESCRIPTION ===

REMEMBER: Follow the user's colors, layout, zone names, and service
names EXACTLY. Apply the GLOBAL STYLE RULES, BOX SPEC, ZONE SPEC,
CONTAINER SPEC, LAYOUT SPEC, and ICON SPEC only where the user has
not specified a conflicting preference.
"""


def wrap(user_markdown: str) -> str:
    """Wrap raw user Markdown with the hardcoded style guard."""
    return f"{PREAMBLE}{user_markdown}\n{POSTAMBLE}"
