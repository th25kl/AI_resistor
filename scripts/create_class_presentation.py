from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'Resistor_Value_Identifier_Calculator_Presentation.pptx'
CALC_47K = ROOT / 'manual_calculator_47k.png'
CALC_220 = ROOT / 'manual_calculator_220.png'
RESULTS_IMAGE = ROOT / 'runs' / 'classify' / 'resistor-values' / 'results.png'

SW, SH = 13.333, 7.5
INK = RGBColor(18, 29, 45)
PANEL = RGBColor(28, 43, 62)
PAPER = RGBColor(247, 247, 242)
WHITE = RGBColor(250, 250, 248)
MUTED = RGBColor(162, 177, 191)
TEAL = RGBColor(50, 197, 176)
YELLOW = RGBColor(246, 195, 78)
CORAL = RGBColor(239, 112, 96)
BLUE = RGBColor(79, 149, 220)
FONT = 'Aptos'
CODE_FONT = 'Aptos Mono'


def add_box(slide, x, y, w, h, fill, radius=True, line=None):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background() if line is None else None
    if line is not None:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    return shape


def add_text(slide, text, x, y, w, h, size=16, color=INK, bold=False,
             font=FONT, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
             margin=0.03):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return shape


def add_header(slide, eyebrow, title, page, dark=True):
    main = WHITE if dark else INK
    sub = MUTED if dark else RGBColor(93, 108, 122)
    add_text(slide, eyebrow.upper(), 0.62, 0.34, 8.8, 0.25, 9, TEAL, True)
    add_text(slide, title, 0.62, 0.68, 11.8, 0.53, 25, main, True)
    add_text(slide, f'{page} / 5', 12.12, 0.4, 0.55, 0.25, 9, sub, True, align=PP_ALIGN.RIGHT)


def add_photo(slide, image_path, x, y, w, h, background=WHITE):
    add_box(slide, x, y, w, h, background, radius=True)
    with Image.open(image_path) as image:
        image_w, image_h = image.size
    scale = min((w - 0.12) / image_w, (h - 0.12) / image_h)
    fitted_w, fitted_h = image_w * scale, image_h * scale
    slide.shapes.add_picture(
        str(image_path),
        Inches(x + (w - fitted_w) / 2),
        Inches(y + (h - fitted_h) / 2),
        width=Inches(fitted_w), height=Inches(fitted_h),
    )


def add_footer(slide, label, dark=True):
    color = MUTED if dark else RGBColor(93, 108, 122)
    add_text(slide, label, 0.62, 7.16, 11.9, 0.18, 8, color)


def slide_one(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = INK
    add_box(slide, 0, 0, 0.16, SH, TEAL, radius=False)
    add_text(slide, 'ECE PROJECT  /  COMPUTER VISION', 0.78, 0.72, 6.7, 0.28, 10, TEAL, True)
    add_text(slide, 'Resistor Value\nIdentifier', 0.75, 1.25, 6.8, 1.52, 34, WHITE, True)
    add_text(slide, 'Choose the bands. Read the value.', 0.8, 3.02, 6.1, 0.44, 18, MUTED)
    add_text(slide, 'A hands-on tool for selecting resistor bands and reading the resulting resistance.',
             0.8, 3.62, 5.7, 0.8, 14, WHITE)
    add_box(slide, 0.8, 4.75, 5.9, 0.82, PANEL, radius=True)
    add_text(slide, '4-band', 1.02, 4.98, 1.2, 0.3, 15, TEAL, True)
    add_text(slide, '5-band', 2.78, 4.98, 1.2, 0.3, 15, YELLOW, True)
    add_text(slide, 'Live value + tolerance', 4.08, 4.98, 2.35, 0.3, 12, WHITE, True)
    add_photo(slide, CALC_47K, 7.35, 1.05, 4.75, 5.95, background=PANEL)
    add_text(slide, 'THE MANUAL CALCULATOR', 7.35, 6.87, 4.75, 0.2, 8, TEAL, True, align=PP_ALIGN.CENTER)
    add_footer(slide, 'Resistor Value Identifier  •  Class presentation')


def slide_two(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAPER
    add_header(slide, '01  /  Main feature', 'Manual calculator: from bands to a value', 2, dark=False)
    add_photo(slide, CALC_47K, 0.7, 1.55, 5.15, 5.35, background=INK)
    steps = [
        ('1', 'Choose band count', 'Select a 4-band or 5-band resistor.'),
        ('2', 'Set each color', 'Use the labeled selectors; the resistor preview updates.'),
        ('3', 'Read the result', 'Resistance in ohms and tolerance recalculate immediately.'),
    ]
    for index, (number, title, body) in enumerate(steps):
        y = 1.85 + index * 1.38
        add_box(slide, 6.45, y, 5.92, 1.12, WHITE, radius=True, line=RGBColor(220, 225, 226))
        add_text(slide, number, 6.7, y + 0.21, 0.45, 0.4, 20, TEAL if index != 1 else CORAL, True)
        add_text(slide, title, 7.25, y + 0.16, 4.75, 0.29, 15, INK, True)
        add_text(slide, body, 7.25, y + 0.52, 4.75, 0.4, 11, RGBColor(75, 87, 96))
    add_text(slide, '4-band: 2 significant digits  •  5-band: 3 significant digits',
             6.5, 6.3, 5.8, 0.35, 12, INK, True)
    add_footer(slide, 'The manual calculator works independently of photo detection.', dark=False)


def slide_three(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = INK
    add_header(slide, '02  /  Calculator examples', 'Change the bands; the decoded value follows', 3)
    add_photo(slide, CALC_220, 0.68, 1.52, 5.75, 4.9, background=PANEL)
    add_photo(slide, CALC_47K, 6.9, 1.52, 5.75, 4.9, background=PANEL)
    add_text(slide, 'RED • RED • BROWN • GOLD', 0.78, 6.53, 5.55, 0.26, 10, TEAL, True, align=PP_ALIGN.CENTER)
    add_text(slide, '220 Ω  /  ±5%', 0.78, 6.82, 5.55, 0.25, 12, WHITE, True, align=PP_ALIGN.CENTER)
    add_text(slide, 'YELLOW • VIOLET • RED • GOLD', 7.0, 6.53, 5.55, 0.26, 10, YELLOW, True, align=PP_ALIGN.CENTER)
    add_text(slide, '4.7 kΩ  /  ±5%', 7.0, 6.82, 5.55, 0.25, 12, WHITE, True, align=PP_ALIGN.CENTER)
    add_footer(slide, 'Both examples were selected and decoded in the running manual calculator.')


def slide_four(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAPER
    add_header(slide, '03  /  How the calculator works', 'Digits, multiplier, tolerance', 4, dark=False)
    add_text(slide, '4-BAND RESISTOR', 0.8, 1.63, 5.55, 0.26, 10, BLUE, True)
    swatches = [
        ('RED\n2', CORAL), ('RED\n2', CORAL), ('BROWN\n×10', RGBColor(124, 72, 42)), ('GOLD\n±5%', YELLOW),
    ]
    for index, (label, color) in enumerate(swatches):
        x = 0.82 + index * 1.42
        add_box(slide, x, 2.02, 1.18, 0.9, color)
        add_text(slide, label, x + 0.05, 2.23, 1.08, 0.43, 12, INK if color == YELLOW else WHITE, True, align=PP_ALIGN.CENTER)
    add_box(slide, 0.8, 3.12, 5.65, 0.85, INK)
    add_text(slide, '(22) × 10 = 220 Ω', 1.03, 3.34, 5.2, 0.36, 20, WHITE, True, align=PP_ALIGN.CENTER)

    add_text(slide, '5-BAND RESISTOR', 6.9, 1.63, 5.55, 0.26, 10, TEAL, True)
    five_swatches = [
        ('YELLOW\n4', YELLOW), ('VIOLET\n7', RGBColor(112, 74, 173)), ('RED\n0', CORAL),
        ('BROWN\n×10', RGBColor(124, 72, 42)), ('GOLD\n±5%', YELLOW),
    ]
    for index, (label, color) in enumerate(five_swatches):
        x = 6.92 + index * 1.13
        add_box(slide, x, 2.02, 0.94, 0.9, color)
        add_text(slide, label, x + 0.03, 2.23, 0.88, 0.43, 10, INK if color == YELLOW else WHITE, True, align=PP_ALIGN.CENTER)
    add_box(slide, 6.9, 3.12, 5.65, 0.85, INK)
    add_text(slide, '(470) × 10 = 4.7 kΩ', 7.12, 3.34, 5.2, 0.36, 20, WHITE, True, align=PP_ALIGN.CENTER)

    add_box(slide, 0.8, 4.55, 11.75, 1.18, RGBColor(231, 238, 239))
    add_text(slide, 'Why tolerance matters', 1.05, 4.8, 2.55, 0.3, 14, INK, True)
    add_text(slide, 'Gold indicates ±5%; silver indicates ±10%. Metallic colors are not valid significant digits.',
             3.65, 4.77, 8.5, 0.52, 12, RGBColor(65, 80, 89))
    add_text(slide, '4-band formula: (10 × first digit + second digit) × multiplier',
             0.95, 6.28, 11.45, 0.34, 13, INK, True, align=PP_ALIGN.CENTER)
    add_footer(slide, 'The calculator updates the value and tolerance as soon as a band selection changes.', dark=False)


def slide_five(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = INK
    add_header(slide, '04  /  Project results', 'A practical resistor calculator with an AI extension', 5)
    add_box(slide, 0.7, 1.7, 3.25, 3.95, TEAL)
    add_text(slide, 'MANUAL\nCALCULATOR', 0.95, 2.0, 2.75, 0.9, 22, INK, True, align=PP_ALIGN.CENTER)
    add_text(slide, '4-BAND  /  5-BAND', 0.98, 3.18, 2.7, 0.34, 11, INK, True, align=PP_ALIGN.CENTER)
    add_text(slide, '220 Ω\n4.7 kΩ', 1.04, 3.7, 2.55, 0.84, 20, INK, True, align=PP_ALIGN.CENTER)
    add_text(slide, 'Decoded values with tolerance, updated from color selections.',
             1.03, 4.78, 2.6, 0.55, 9, INK, align=PP_ALIGN.CENTER)

    add_text(slide, 'WORKING FEATURES', 4.55, 1.82, 3.35, 0.25, 9, YELLOW, True)
    add_text(slide, '• Select four or five bands\n• See a resistor preview\n• Decode resistance and tolerance\n• Upload-photo AI mode is optional',
             4.55, 2.2, 3.45, 1.65, 13, WHITE)
    add_text(slide, 'AI MODEL SUPPORT', 8.48, 1.82, 3.8, 0.25, 9, CORAL, True)
    add_text(slide, '• 37 resistor classes\n• 91% top-1 test accuracy\n• 99.7% top-5 on 289 held-out photos\n• Model/band conflicts are flagged',
             8.48, 2.2, 4.0, 1.72, 13, WHITE)

    add_box(slide, 4.52, 4.55, 7.97, 1.08, PANEL)
    add_text(slide, 'TAKEAWAY', 4.78, 4.76, 1.35, 0.24, 9, TEAL, True)
    add_text(slide, 'The manual calculator is the core; image recognition adds a second way to identify a resistor.',
             6.2, 4.72, 5.93, 0.48, 14, WHITE, True)
    add_text(slide, 'Questions?', 4.55, 6.05, 7.9, 0.45, 21, YELLOW, True)
    add_footer(slide, 'Measured project result; broader real-world accuracy still requires additional evaluation.')


def main():
    for required in (CALC_47K, CALC_220, RESULTS_IMAGE):
        if not required.is_file():
            raise FileNotFoundError(required)

    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    slide_one(prs)
    slide_two(prs)
    slide_three(prs)
    slide_four(prs)
    slide_five(prs)
    prs.save(OUTPUT)
    print(f'Created {OUTPUT.name} with {len(prs.slides)} slides.')


if __name__ == '__main__':
    main()