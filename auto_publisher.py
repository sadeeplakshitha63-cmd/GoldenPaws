import os
import random
import datetime
import urllib.parse
import xml.etree.ElementTree as ET
from xml.dom import minidom
import google.generativeai as genai

# -------------------------------------------------------------
# GoldenPaws Fully Automated Content Generator (Bug Fixed)
# -------------------------------------------------------------

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SITE_URL = "https://sadeeplakshitha63-cmd.github.io/GoldenPaws"
SITE_TITLE = "GoldenPaws Expert Guides"
SITE_DESCRIPTION = "The ultimate resource for Golden Retriever owners."

POST_TOPICS = [
    "Most common skin allergies in Golden Retrievers",
    "How much exercise does a 6-month-old Golden Retriever need?",
    "Golden Retriever shedding: Best grooming brushes and techniques",
    "Best toys for aggressive chewing Golden Retriever puppies",
    "Is a Golden Retriever good for a family with a baby?",
    "Golden Retriever vs Labrador: Which breed is right for you?"
]

article_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | GoldenPaws</title>
    <meta name="description" content="{seo_description}">
    <!-- Open Graph for Pinterest -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{seo_description}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:url" content="{site_url}/{filename}">
    
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body style="background-color: #FAFBFC;">
    <nav class="navbar" style="background: rgba(255, 255, 255, 0.95); box-shadow: 0 2px 10px rgba(0,0,0,0.05); padding: 1.2rem 5%; position: sticky; top: 0; z-index: 1000;">
        <div class="nav-container" style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; width: 100%;">
            <a href="index.html" class="logo" style="font-weight: 800; font-size: 1.5rem; text-decoration: none; color: #1C1E21;">🐾 GoldenPaws</a>
            <div class="nav-actions">
                <a href="https://www.pinterest.com/sadeeplakshitha2001/" target="_blank" style="background: #E60023; color: white; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: bold;">Follow on Pinterest</a>
            </div>
        </div>
    </nav>

    <header class="article-hero" style="padding: 60px 5%; text-align: center; background: white; border-bottom: 1px solid #eaeaea; margin-bottom: 40px;">
        <h1 style="font-family: 'Outfit'; font-size: 2.5rem; margin-bottom: 10px; max-width: 900px; margin: 0 auto;">{title}</h1>
    </header>

    <main class="prose" style="max-width: 800px; margin: 0 auto; padding: 0 5% 50px 5%; font-family: 'Inter', sans-serif; line-height: 1.8; color: #333; font-size: 1.1rem;">
        
        <div style="position:relative; margin-bottom: 40px;">
            <img src="{image_url}" alt="{title}" data-pin-url="https://www.pinterest.com/sadeeplakshitha2001/" data-pin-media="{image_url}" style="width:100%; border-radius:12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <a href="https://www.pinterest.com/pin/create/button/" data-pin-do="buttonBookmark" style="position: absolute; top: 20px; right: 20px; background: #E60023; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-weight: bold;">Save to Pinterest</a>
        </div>
        
        {content_html}
        
    </main>

    <script async defer src="//assets.pinterest.com/js/pinit.js"></script>
</body>
</html>
"""

def get_robust_image():
    # Direct links to high quality images to avoid broken link bugs
    photos = [
        "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&q=80&w=1200",
        "https://images.unsplash.com/photo-1546975490-e8b92a360b24?auto=format&fit=crop&q=80&w=1200",
        "https://images.unsplash.com/photo-1596492784531-6e6eb5ea9993?auto=format&fit=crop&q=80&w=1200",
        "https://images.unsplash.com/photo-1633722715463-d30f4f325e24?auto=format&fit=crop&q=80&w=1200",
        "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&q=80&w=1200"
    ]
    return random.choice(photos)

def generate_article(topic):
    if not GEMINI_API_KEY:
        # Fallback text if no API key
        return f"<p>This is a highly researched guide on {topic}. (API Key not connected yet, so this is placeholder text.)</p>"
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"Act as an expert veterinarian. Write a 1000-word highly authoritative blog post on '{topic}'. Output pure HTML (h2, p, ul). No markdown blocks."
        response = model.generate_content(prompt)
        return response.text.replace("```html", "").replace("```", "")
    except Exception as e:
        print(f"Bugs encountered in AI: {e}")
        return f"<p>Temporarily unavailable. Check back soon for our guide on {topic}.</p>"

def update_index_html(title, filename, image_url):
    # This automatically adds the new post to your homepage!
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Fix the old broken links while we're reading the file!
        content = content.replace('href="#" class="read-more"', 'href="article-food.html" class="read-more"')
        
        new_card = f"""
            <!-- AUTO-GENERATED POST -->
            <article class="card">
                <div class="card-img-wrapper">
                    <img src="{image_url}" alt="{title}" class="card-img" data-pin-media="{image_url}">
                    <span class="category tag-training">New</span>
                </div>
                <div class="card-body">
                    <h3>{title}</h3>
                    <p class="excerpt">Expert insights on {title} to keep your Golden Retriever healthy and happy.</p>
                    <div class="card-footer">
                        <span class="read-time"><i class="fa-regular fa-clock"></i> 5 min read</span>
                        <a href="{filename}" class="read-more">Read Full Guide <i class="fa-solid fa-arrow-right"></i></a>
                    </div>
                </div>
            </article>
            """
            
        # Inject right after the start of article-grid
        if '<div class="article-grid">' in content:
            parts = content.split('<div class="article-grid">')
            updated_content = parts[0] + '<div class="article-grid">\n' + new_card + parts[1]
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Successfully injected new post into index.html!")
    except Exception as e:
        print(f"Error updating index.html: {e}")

def update_rss_feed(title, filename, description, image_url):
    # THIS is what Pinterest reads to auto-publish!
    rss_path = "rss.xml"
    post_url = f"{SITE_URL}/{filename}"
    date_rfc822 = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    if not os.path.exists(rss_path):
        # Create new RSS feed
        rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}</link>
    <description>{SITE_DESCRIPTION}</description>
</channel>
</rss>"""
        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(rss_content)
    
    try:
        tree = ET.parse(rss_path)
        root = tree.getroot()
        channel = root.find("channel")
        
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = post_url
        ET.SubElement(item, "description").text = description
        ET.SubElement(item, "pubDate").text = date_rfc822
        
        # VERY important for Pinterest: The Image
        media_content = ET.SubElement(item, "media:content")
        media_content.set("url", image_url)
        media_content.set("medium", "image")
        
        tree.write(rss_path, encoding="utf-8", xml_declaration=True)
        print("RSS Feed updated successfully for Pinterest Auto-Publishing.")
        
    except Exception as e:
        print(f"Error updating RSS feed: {e}")

def run_bot():
    topic = random.choice(POST_TOPICS)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    slug = "-".join(topic.replace('?', '').replace(':', '').split()).lower()
    filename = f"{slug}-{date_str}.html"
    
    print(f"Drafting post: {topic}...")
    
    content = generate_article(topic)
    image = get_robust_image()
    
    html_output = article_template.format(
        title=topic, 
        seo_description=f"Learn everything about {topic} for your Golden Retriever.", 
        image_url=image, 
        site_url=SITE_URL, 
        filename=filename, 
        content_html=content
    )
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_output)
        
    print(f"Created HTML file: {filename}")
    
    # Run the bug fixes / automated components
    update_index_html(title=topic, filename=filename, image_url=image)
    update_rss_feed(title=topic, filename=filename, description=topic, image_url=image)
    
if __name__ == "__main__":
    run_bot()
