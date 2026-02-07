import os
import re

# Root directory
root_dir = 'c:/Users/Admin/Downloads/signage-main/signage-main'

# Preloads to add (only to index.html as they are specific to its LCP)
# Update preloads to 768px version for better hero clarity on mobile
index_preloads = '\t<link rel="preload" as="image" href="wp-content/uploads/2020/12/4-768x1024.webp" type="image/webp">\n\t<link rel="preload" as="image" href="wp-content/uploads/2020/12/cropped-logo-1024x768.webp" type="image/webp">\n'

cdn_font_link = '<link rel="stylesheet" id="google-fonts-cdn" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Roboto+Slab:wght@100..900&family=Scada:ital,wght@0,400;0,700;1,400;1,700&display=swap" media="all">'

def optimize_file(file_path):
    print(f"Optimizing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Preloads (index.html only)
    if os.path.basename(file_path) == 'index.html':
        # Remove old image preloads first to avoid duplicates or outdated versions
        content = re.sub(r'<link rel="preload" as="image" href="wp-content/uploads/2020/12/.*?\.webp" type="image/webp">\s*', '', content)
        if '<head>' in content:
            content = content.replace('<head>', '<head>\n' + index_preloads)

    # 2. Fonts
    content = re.sub(r'<link rel="stylesheet" id="elementor-gf-local-.*?-css".*?href=.*?>', '', content, flags=re.DOTALL)
    if 'id="google-fonts-cdn"' not in content:
        if '<!--[if IE]>' in content:
            content = content.replace('<!--[if IE]>', cdn_font_link + '\n\t<!--[if IE]>')
        elif '<script src="wp-includes/js/jquery/' in content:
            content = re.sub(r'(<script src="wp-includes/js/jquery/.*?>)', cdn_font_link + '\n\t\\1', content)
        else:
            content = content.replace('</head>', '\t' + cdn_font_link + '\n</head>')

    # 3. LCP Priority & Resolution Enhancement (First 2 images)
    img_count = 0
    def img_callback(match):
        nonlocal img_count
        tag = match.group(0)
        
        if img_count < 2:
            # Add fetchpriority
            if 'fetchpriority="high"' not in tag:
                tag = tag.replace('<img ', '<img fetchpriority="high" ')
            tag = tag.replace('decoding="async"', '')
            
            # High-Resolution Upgrades for Hero and Logo
            if '4.webp' in tag or '4.jpg' in tag:
                # Upgrade hero to 768px for Retina mobile
                tag = re.sub(r'src=["\'](.*?)["\']', 'src="wp-content/uploads/2020/12/4-768x1024.webp"', tag)
                tag = re.sub(r'srcset=["\'](.*?)["\']', 'srcset="wp-content/uploads/2020/12/4-768x1024.webp 768w, wp-content/uploads/2020/12/4-1024x768.webp 1024w"', tag)
                tag = re.sub(r'sizes=["\'](.*?)["\']', 'sizes="(max-width: 400px) 100vw, 768px"', tag)
            
            if 'cropped-logo' in tag:
                # Upgrade logo to higher res for Retina
                tag = re.sub(r'src=["\'](.*?)["\']', 'src="wp-content/uploads/2020/12/cropped-logo-1024x768.webp"', tag)
                # Keep intrinsic display width small but source large
                if 'width=' in tag:
                    tag = re.sub(r'width=["\']\d+["\']', 'width="233"', tag)
                if 'height=' in tag:
                    tag = re.sub(r'height=["\']\d+["\']', 'height="53"', tag)

            tag = ' '.join(tag.split())
            if not tag.endswith('>'): tag += '>'
            img_count += 1
        return tag
    
    content = re.sub(r'<img.*?>', img_callback, content, flags=re.DOTALL)

    # 4. Cleanup picture tags
    def cleanup_picture(match):
        picture_content = match.group(1)
        # Update any source tags inside picture to point to higher resolution
        if '4.webp' in picture_content or '4.jpg' in picture_content:
            picture_content = re.sub(r'srcset=["\'](.*?)["\']', 'srcset="wp-content/uploads/2020/12/4-768x1024.webp"', picture_content)
        
        source_tags = re.findall(r'<source.*?>.*?</source>|<source.*?>', picture_content, re.DOTALL)
        img_match = re.search(r'(<img.*?>)', picture_content, re.DOTALL)
        unique_sources = []
        seen_srcsets = set()
        for source in source_tags:
            srcset_match = re.search(r'srcset=["\'](.*?)["\']', source)
            if srcset_match:
                srcset = srcset_match.group(1)
                if srcset not in seen_srcsets:
                    unique_sources.append(source.strip())
                    seen_srcsets.add(srcset)
        result = "\n" + "\n".join(["\t\t\t\t\t\t\t\t\t\t" + s for s in unique_sources])
        if img_match:
            img_tag = img_match.group(1).strip()
            result += "\n\t\t\t\t\t\t\t\t\t\t" + img_tag
        return f"<picture>{result}\n\t\t\t\t\t\t\t\t\t\t</picture>"

    content = re.sub(r'<picture>(.*?)</picture>', cleanup_picture, content, flags=re.DOTALL)

    # 5. Whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Run for all HTML files in root
for root, dirs, files in os.walk(root_dir):
    if root == root_dir:
        for file in files:
            if file.endswith('.html'):
                optimize_file(os.path.join(root, file))

print("Site-wide Image Resolution Boost finished.")
