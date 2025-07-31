
from flask import Flask, request, jsonify
import instaloader
import re

app = Flask(__name__)

@app.route('/get_caption', methods=['POST'])
def get_caption():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "Missing url"}), 400

    try:
        # Initialize Instaloader
        L = instaloader.Instaloader()

        # Extract shortcode from URL using regex
        shortcode_match = re.search(r'/(?:reel|p)/([A-Za-z0-9_-]+)', url)
        if not shortcode_match:
            return jsonify({"error": "Invalid Instagram URL format"}), 400

        shortcode = shortcode_match.group(1)

        # Get the post using the shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Extract caption
        caption = post.caption if post.caption else ""

        return jsonify({"caption": caption})

    except instaloader.exceptions.PostUnavailableException:
        return jsonify({"error": "Post not found or unavailable"}), 404
    except instaloader.exceptions.LoginRequiredException:
        return jsonify({"error": "Login required to access this post"}), 403
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        return jsonify({"error": "Private profile - follow required"}), 403
    except Exception as e:
        return jsonify({"error": f"Failed to fetch caption: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
