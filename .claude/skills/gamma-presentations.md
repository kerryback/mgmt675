# Gamma.app Presentation Skill

Create professional slide decks using gamma.app with Python post-processing for the MGMT 675: Generative AI for Finance course.

## Workflow Overview

1. **Create in Gamma.app** - Let gamma.app generate content with AI images
2. **Configure for Export** - Set 16:9 aspect ratio and "Traditional" page style
3. **Export as PPTX** - Download the PowerPoint file
4. **Post-process with Python** - Tweak formatting, add cover slide, adjust styling

## Gamma.app Best Practices

### Creating a New Presentation

1. Go to [gamma.app](https://gamma.app) and click "Create new"
2. Enter your topic/outline or paste content
3. Let gamma.app generate with these recommended settings:
   - **Image source**: AI Generated (give gamma full creative freedom)
   - **Template**: Let gamma choose or select a professional theme
   - **Tone**: Professional, educational
   - **Audience**: MBA students / Finance professionals

### Configuring for 16:9 Export

Before exporting, configure the presentation:

1. Click the **three-dot menu (⋯)** in the top right
2. Select **Page Setup**
3. Set **Card Size** to **16:9 (Traditional)**
4. Enable **Show Card Backdrops** if desired
5. Review in **Present Mode** (this is what exports)

### Export Settings

1. Click **Share** → **Export**
2. Select **PowerPoint (PPTX)**
3. Download the file to your project folder

**Note**: Plus/Pro accounts export without watermark. Free accounts include "Made with Gamma" branding.

## Gamma API (Programmatic Creation)

For automated generation, use the Gamma API. See `test_gamma_api.py` for reference.

```python
# Required: GAMMA_API_KEY in .env file
# API endpoint: https://public-api.gamma.app/v1.0

payload = {
    "inputText": "Your content here with --- slide separators",
    "textMode": "generate",  # or "exact" to use your text as-is
    "format": "presentation",
    "numCards": 5,
    "imageOptions": {
        "source": "aiGenerated",
        "style": "professional, modern, finance theme"
    },
    "textOptions": {
        "amount": "medium",
        "tone": "professional, educational",
        "audience": "MBA students"
    },
    "exportAs": "pptx"
}
```

## Python Post-Processing

### Setup

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
import copy
```

### Common Operations

#### Verify/Set 16:9 Dimensions

```python
def ensure_16x9(pptx_path, output_path=None):
    """Ensure presentation is 16:9 aspect ratio (16x9 inches)"""
    prs = Presentation(pptx_path)

    # Standard 16:9 dimensions
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)

    output_path = output_path or pptx_path
    prs.save(output_path)
    print(f"Saved 16:9 presentation to {output_path}")
    return prs
```

#### Insert Cover Slide

```python
def insert_cover_slide(pptx_path, title, cover_template="cover_slide.pptx", output_path=None):
    """Insert a cover slide at the beginning of a presentation"""
    from pptx.util import Inches, Pt

    # Load both presentations
    prs = Presentation(pptx_path)
    cover_prs = Presentation(cover_template)

    # Get the cover slide layout from template
    cover_slide = cover_prs.slides[0]

    # Create a new slide at the beginning using blank layout
    blank_layout = prs.slide_layouts[6]  # Usually blank
    new_slide = prs.slides.add_slide(blank_layout)

    # Move the new slide to position 0
    slide_id = prs.slides._sldIdLst[-1]
    prs.slides._sldIdLst.remove(slide_id)
    prs.slides._sldIdLst.insert(0, slide_id)

    # Copy shapes from cover template
    for shape in cover_slide.shapes:
        # Clone shape (simplified - may need adjustment for complex shapes)
        if shape.has_text_frame:
            # Update title text if this is the title shape
            for para in shape.text_frame.paragraphs:
                if "AI Agents" in para.text or title.lower() in para.text.lower():
                    para.text = title

    output_path = output_path or pptx_path
    prs.save(output_path)
    return prs
```

#### Adjust Font Sizes

```python
def scale_fonts(pptx_path, scale_factor=1.2, output_path=None):
    """Scale all fonts by a factor"""
    prs = Presentation(pptx_path)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.size:
                            run.font.size = Pt(run.font.size.pt * scale_factor)

    output_path = output_path or pptx_path
    prs.save(output_path)
    return prs
```

#### Replace Colors

```python
def replace_color(pptx_path, old_rgb, new_rgb, output_path=None):
    """Replace a specific color throughout the presentation"""
    prs = Presentation(pptx_path)

    old_color = RGBColor(*old_rgb)
    new_color = RGBColor(*new_rgb)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.color.rgb == old_color:
                            run.font.color.rgb = new_color

    output_path = output_path or pptx_path
    prs.save(output_path)
    return prs
```

### Full Processing Pipeline

```python
def process_gamma_export(input_path, title, output_path=None):
    """Complete post-processing pipeline for gamma.app exports"""
    from pptx import Presentation
    from pptx.util import Inches

    output_path = output_path or input_path.replace('.pptx', '_final.pptx')

    # Load presentation
    prs = Presentation(input_path)

    # 1. Ensure 16:9 dimensions
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)

    # 2. Save processed version
    prs.save(output_path)

    print(f"Processed: {output_path}")
    print(f"  - Dimensions: {prs.slide_width.inches}x{prs.slide_height.inches} inches")
    print(f"  - Slides: {len(prs.slides)}")

    return output_path
```

## Cover Slide Design

The course uses a consistent cover slide format with three style options.

### Style Options

**Modern** (recommended):
- Dark background with blue accent bar on left
- Course title in uppercase at top
- Large bold title in center-left
- Decorative accent line under title
- "Rice Business" footer

**Classic**:
- Centered layout
- Course title in accent color above main title
- Traditional professional look

**Minimal**:
- Pure dark background
- Title only, centered
- Course title at bottom

### Creating a Cover Slide with Python

```bash
# Create a modern cover slide
python gamma_pptx_utils.py cover "AI Agents" cover_slide.pptx modern

# Create with background image
python -c "
from gamma_pptx_utils import create_cover_slide
create_cover_slide('AI Agents', background_image='image.png', style='modern')
"
```

### Creating Cover Slides with Gamma.app (for AI images)

For cover slides with AI-generated imagery:

1. **In gamma.app**, create a single-card presentation:
   - Enter just the topic title
   - Let gamma generate an AI image
   - Set Page Setup to 16:9

2. **Export as PPTX**

3. **Post-process** to add course branding:
   ```python
   from gamma_pptx_utils import process_gamma_export
   process_gamma_export('gamma_cover.pptx', title='AI Agents', add_cover=False)
   # Manually add course title text or use as background for Python-generated slide
   ```

### Cover Slide Template Structure

The `cover_slide.pptx` contains:
- One slide (16x9 inches)
- Dark background with optional AI-generated image
- Blue accent bar (modern style)
- Course title: "MGMT 675: GENERATIVE AI FOR FINANCE"
- Topic title: Large, bold text
- Footer: "Rice Business"

## Commands

### Process Gamma Export

When asked to "process gamma export [filename]":

1. Load the PPTX file
2. Verify/set 16:9 dimensions
3. Report slide count and any issues
4. Save processed version

### Create Cover Slide

When asked to "create cover slide for [topic]":

1. Generate a cover image prompt related to the topic
2. Create a new slide with the standard course layout
3. Save to cover_slide.pptx or specified filename

### Analyze Presentation

When asked to "analyze [filename].pptx":

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation('filename.pptx')
print(f"Dimensions: {prs.slide_width.inches} x {prs.slide_height.inches} inches")
print(f"Aspect ratio: {prs.slide_width.inches/prs.slide_height.inches:.3f}")
print(f"Slides: {len(prs.slides)}")

for i, slide in enumerate(prs.slides):
    print(f"\nSlide {i+1}: {slide.slide_layout.name}")
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = ' '.join(p.text for p in shape.text_frame.paragraphs if p.text.strip())
            if text:
                print(f"  - {text[:60]}...")
```

## Files Reference

- `cover_slide.pptx` - Cover slide template
- `gamma_pptx_utils.py` - Python utilities for PPTX post-processing
- `test_gamma_api.py` - Gamma API test script
- `.env` - Contains GAMMA_API_KEY (not in git)

## CLI Commands

```bash
# Analyze a presentation
python gamma_pptx_utils.py analyze presentation.pptx

# Process a gamma export (ensure 16:9)
python gamma_pptx_utils.py process input.pptx output.pptx

# Create a cover slide
python gamma_pptx_utils.py cover "Topic Title" output.pptx [style]
# Styles: modern (default), classic, minimal

# Convert to 16:9
python gamma_pptx_utils.py ensure16x9 input.pptx output.pptx
```

## Export Troubleshooting

| Issue | Solution |
|-------|----------|
| Gradients appear as solid colors | Expected limitation - redesign with solid colors |
| Fonts look different | Install fonts locally or use web-safe fonts |
| Layout shifted | Set "Traditional" page style before export |
| Watermark present | Requires Plus/Pro subscription |
| Images blurry | Use higher quality source images |

## Sources

- [Gamma Help: Export Options](https://help.gamma.app/en/articles/8022861-what-s-the-easiest-way-to-export-my-gamma)
- [Gamma Help: Page Setup](https://help.gamma.app/en/articles/11029115-how-do-i-control-card-sizes-and-adjust-page-setups)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
