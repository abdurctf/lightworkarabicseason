import instaloader

def download_first_post(target_username):
    print("Initializing Instaloader instance.")
    
    # Get instance
    L = instaloader.Instaloader()

    print(f"Attempting to retrieve posts for {target_username}.")
    
    # Initialize the Profile from a username
    profile = instaloader.Profile.from_username(L.context, target_username)
    
    # Iterate over posts and download only the first post
    for index, post in enumerate(profile.get_posts()):
        if index == 0:  # First post
            print(f"Found the first post with the shortcode: {post.shortcode}. Downloading...")
            L.download_post(post, target=target_username)
            print(f"Downloaded the first post from {target_username}.")
            break  # Exit the loop as we've downloaded the first post
        else:
            print("No posts found!")
            
if __name__ == '__main__':
    target_username = 'some_public_profile_username'  # Replace with the target username
    print(f"Starting the download process for {target_username}.")
    download_first_post(target_username)
    print("Download complete.")
