#!/usr/bin/env python
import os
import sys
import re
from glob import glob
from ligaturize import ligaturize_font
import fontforge

# Nerd Fonts 3.5.1 inputs, no "copy character glyphs" variants.
LIGATURIZED_FONT_NAME_SUFFIX = 'Ligatured NF3'

SCALE_CHARACTER_GLYPHS_THRESHOLD = 0.1
SCALE_LIGATURE_THRESHOLD = 0.044

os.makedirs('fonts/output', exist_ok=True)

# Generate fira otf from ttf files
fira_ttf_list = glob('fonts/fira/distr/ttf/*.ttf')

if not fira_ttf_list:
    print("Error: pattern '%s' didn't match any fira fonts." % fira_ttf_list)
    sys.exit(1)

for fira_ttf in fira_ttf_list:
    font = fontforge.open(fira_ttf)
    print(fira_ttf.replace('.ttf', '.otf'))
    font.generate(fira_ttf.replace('.ttf', '.otf'))
    font.close()

styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']

tasks = []
for nf_family in ('HackNerdFont', 'HackNerdFontMono'):
    for style in styles:
        fira_style = 'Bold' if style.startswith('Bold') else 'Regular'
        tasks.append({
            'input': 'fonts/nerd-fonts/%s-%s.ttf' % (nf_family, style),
            'ligatures': [
                'fonts/fira/distr/ttf/FiraCode-%s.otf' % fira_style,
                'fonts/jetbrainsmono/fonts/ttf/JetBrainsMono-%s.ttf' % style,
            ],
        })

for task in tasks:
    input_pattern = task['input']
    input_files = glob(input_pattern)

    if not input_files:
        print("Error: pattern '%s' didn't match any files." % input_pattern)
        sys.exit(1)

    for liga_pattern in task['ligatures']:
        liga_files = glob(liga_pattern)
        if not liga_files:
            print("Error: pattern '%s' didn't match any files." % liga_pattern)
            sys.exit(1)

        for input_file in input_files:
            for liga_file in liga_files:
                liga_font_splits = re.split(r'-|\s', os.path.splitext(os.path.basename(liga_file))[0])
                liga_font_family = liga_font_splits[0]

                # grab all upper case letters of the font family
                ligatured_font_family = ''.join(list(filter(lambda x: x.isupper(), list(liga_font_family))))

                ligaturize_font(
                    input_font_file=input_file,
                    ligature_font_file=liga_file,
                    output_dir='fonts/output/',
                    output_name=None,
                    suffix="%s %s" % (ligatured_font_family, LIGATURIZED_FONT_NAME_SUFFIX),
                    copy_character_glyphs=False,
                    scale_character_glyphs_threshold=SCALE_CHARACTER_GLYPHS_THRESHOLD,
                    scale_ligature_threshold=SCALE_LIGATURE_THRESHOLD,
                )
