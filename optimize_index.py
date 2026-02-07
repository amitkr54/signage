import os
import re

file_path = 'c:/Users/Admin/Downloads/signage-main/signage-main/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Cleanup picture tags (remove duplicate source tags) while preserving img attributes
def cleanup_picture(match):
    picture_content = match.group(1)
    
    # Extract source tags
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
        img_tag = img_match.group(1)
        # Ensure img_tag is clean
        img_tag = img_tag.strip()
        result += "\n\t\t\t\t\t\t\t\t\t\t" + img_tag
    
    return f"<picture>{result}\n\t\t\t\t\t\t\t\t\t\t</picture>"

content = re.sub(r'<picture>(.*?)</picture>', cleanup_picture, content, flags=re.DOTALL)

# 2. Add fetchpriority="high" to the first and second images (logo and first hero)
# And remove decoding="async" for LCP candidates
def optimize_lcp_img(tag):
    # Add high priority
    if 'fetchpriority="high"' not in tag:
        tag = tag.replace('<img ', '<img fetchpriority="high" ')
    # Remove async decoding for LCP
    tag = tag.replace('decoding="async"', '')
    # Clean up double spaces
    tag = ' '.join(tag.split())
    # Fixed closing bracket
    if not tag.endswith('>'): tag += '>'
    return tag

# Find first two <img> tags and optimize them
img_count = 0
def img_optim_callback(match):
    global img_count
    img_tag = match.group(0)
    if img_count < 2:
        img_tag = optimize_lcp_img(img_tag)
        img_count += 1
    return img_tag

content = re.sub(r'<img.*?>', img_optim_callback, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Final Optimization script finished.")
