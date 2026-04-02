import instaloader
import json
import os
import shutil

L = instaloader.Instaloader(
    download_videos=False, 
    save_metadata=False, 
    post_metadata_txt_pattern='',
    dirname_pattern='static/instagram'
)

# Login
# try:
#     print("Logging in...")
#     # L.login('berat_makina_', 'beratmachina1975.')
#     print("Login successful!")
# except Exception as e:
#     print(f"Login failed: {e}")

# Fetch posts
try:
    print("Fetching profile...")
    profile = instaloader.Profile.from_username(L.context, 'berat_makina_')
    
    posts_data = []
    count = 0
    for post in profile.get_posts():
        if count >= 6:
            break
            
        print(f"Downloading post {post.shortcode}")
        L.download_post(post, target='static/instagram')
        
        # Sadece resim dosyalarını saklayacağımız için TXT gibi diğerlerini silelim ama Instaloader parametreleriyle kapattık zaten.
        # Find the downloaded image filename
        img_filename = f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.jpg"
        
        posts_data.append({
            'shortcode': post.shortcode,
            'url': f"https://www.instagram.com/p/{post.shortcode}/",
            'image': img_filename
        })
        count += 1
        
    with open('static/instagram/posts.json', 'w') as f:
        json.dump(posts_data, f)
    print("Done!")
except Exception as e:
    print(f"Fetch failed: {e}")
