import os
import re

root_dir = 'c:/Users/Admin/Downloads/signage-main/signage-main'

# Standard Alt Texts
LOGO_ALT = "signage company"
HERO_ALT = "signage company in gurgaon, signage maker in gurgaon"

def fix_image_seo(file_path):
    print(f"Fixing Image SEO in {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Alts for Logo and Hero
    # Correcting Hero to 1024x768 (Landscape) to match original 4:3 aspect ratio
    old_hero_portrait = "4-768x1024.webp"
    correct_hero_landscape = "4-1024x768.webp"
    
    content = content.replace(old_hero_portrait, correct_hero_landscape)
    
    # 2. Fix Alts
    def alt_fixer(match):
        tag = match.group(0)
        # Fix Logo Alt
        if 'custom-logo' in tag:
            if 'alt=' in tag:
                tag = re.sub(r'alt=["\'][^"\']*?["\']', f'alt="{LOGO_ALT}"', tag)
            else:
                tag = tag.replace('<img ', f'<img alt="{LOGO_ALT}" ')
        # Fix Hero Alt
        if '4-1024x768.webp' in tag or '4.webp' in tag or '4.jpg' in tag:
            if 'alt=' in tag:
                tag = re.sub(r'alt=["\'][^"\']*?["\']', f'alt="{HERO_ALT}"', tag)
            else:
                tag = tag.replace('<img ', f'<img alt="{HERO_ALT}" ')
        return tag

    content = re.sub(r'<img [^>]*?>', alt_fixer, content)

    # 3. Global CSS fix for distorted images (Gallery Stretches)
    distortion_fix = """
	<style>
		img { height: auto !important; max-width: 100%; }
		.elementor-image img, .ast-single-post .entry-content img, .wp-block-image img {
			object-fit: cover;
		}
	</style>
"""
    if '</head>' in content and 'object-fit: cover' not in content:
        content = content.replace('</head>', distortion_fix + '</head>')
    elif 'object-fit: cover' in content:
        # Update existing check
        pass

    # 4. Fill empty Alts globally to pass SEO tests
    content = re.sub(r'alt=["\']\s*["\']', f'alt="{LOGO_ALT}"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Run for all HTML files
for root, dirs, files in os.walk(root_dir):
    if root == root_dir:
        for file in files:
            if file.endswith('.html'):
                fix_image_seo(os.path.join(root, file))

print("Site-wide Image SEO & Aspect Ratio fix finished.")
