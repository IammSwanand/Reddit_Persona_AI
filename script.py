"""Reddit User Persona Scraper with AI Analysis.

This script provides an interactive interface to analyze Reddit users
and generate comprehensive personas using GROQ's AI.
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class InteractiveRedditPersonaScraper:
    """Interactive Reddit persona scraper using GROQ AI."""

    def __init__(self):
        """Initialize the scraper with Reddit session and GROQ client."""
        # Reddit scraping
        self.session = requests.Session()
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/91.0.4472.124 Safari/537.36')
        self.session.headers.update({'User-Agent': user_agent})

        # GROQ client
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ API key not found. "
                           "Please set up your .env file.")

        self.groq_client = Groq(api_key=self.groq_api_key)

    def get_user_input(self) -> tuple:
        """Get user input for Reddit profile and output preferences.
        
        Returns:
            Tuple of (profile_url, filename, max_items)
        """
        print(" Please provide the following information:")
        print()

        # Get Reddit profile URL or username
        while True:
            print(" Enter Reddit profile information:")
            print("   • Full URL: https://www.reddit.com/user/username/")
            print("   • Username only: username")
            print("   • With u/ prefix: u/username")
            print()

            reddit_input = input(" Reddit Profile: ").strip()

            if not reddit_input:
                print(" Please enter a valid input!")
                continue

            # Convert input to proper URL
            profile_url = self.normalize_reddit_url(reddit_input)

            if profile_url:
                print(f" Profile URL: {profile_url}")
                break
            else:
                print(" Invalid Reddit profile format! Please try again.")

        print()

        # Get output filename
        while True:
            print(" Choose output filename:")
            print("   • Enter custom name: my_analysis.txt")
            print("   • Press Enter for auto-generated name")
            print()

            filename = input(" Output filename: ").strip()

            if not filename:
                # Auto-generate filename
                try:
                    username = self.extract_username(profile_url)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{username}_persona_{timestamp}.txt"
                    print(f" Auto-generated: {filename}")
                except Exception:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"reddit_persona_{timestamp}.txt"
                    print(f" Using default: {filename}")
                break
            else:
                # Add .txt extension if not present
                if not filename.endswith('.txt'):
                    filename += '.txt'
                print(f" Output filename: {filename}")
                break

        print()

        # Get data limit preference
        while True:
            print(" Data analysis limit:")
            print("   • Default: 1000 posts/comments (recommended)")
            print("   • Custom: Enter number (e.g., 500, 2000)")
            print("   • Note: Higher limits take longer to process")
            print()

            limit_input = input(" Max items (or press Enter for 1000): ").strip()

            if not limit_input:
                max_items = 1000
                print(f" Using default: {max_items}")
                break

            try:
                max_items = int(limit_input)
                if max_items <= 0:
                    print(" Please enter a positive number!")
                    continue
                if max_items > 3000:
                    print("  Warning: Large limits may take 5+ minutes to process.")
                    confirm = input("   Continue? (y/n): ").strip().lower()
                    if confirm not in ['y', 'yes']:
                        continue
                print(f" Max items: {max_items}")
                break
            except ValueError:
                print(" Please enter a valid number!")
                continue

        return profile_url, filename, max_items

    def normalize_reddit_url(self, reddit_input: str) -> str:
        """Convert various Reddit input formats to proper URL.
        
        Args:
            reddit_input: User input (URL, username, or u/username format)
            
        Returns:
            Normalized Reddit profile URL
        """
        reddit_input = reddit_input.strip()

        # Already a full URL
        if reddit_input.startswith("https://www.reddit.com/user/"):
            return reddit_input
        elif reddit_input.startswith("http://www.reddit.com/user/"):
            return reddit_input.replace("http://", "https://")
        elif reddit_input.startswith("www.reddit.com/user/"):
            return f"https://{reddit_input}"
        elif reddit_input.startswith("reddit.com/user/"):
            return f"https://{reddit_input}"
        elif reddit_input.startswith("u/"):
            username = reddit_input[2:]
            return f"https://www.reddit.com/user/{username}/"
        elif reddit_input.startswith("/u/"):
            username = reddit_input[3:]
            return f"https://www.reddit.com/user/{username}/"
        else:
            # Assume it's just a username
            return f"https://www.reddit.com/user/{reddit_input}/"

    def extract_username(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL.
        
        Args:
            profile_url: Reddit profile URL
            
        Returns:
            Username extracted from URL
            
        Raises:
            ValueError: If URL format is invalid
        """
        parsed = urlparse(profile_url.strip())
        path_parts = parsed.path.strip('/').split('/')

        if len(path_parts) >= 2 and path_parts[0] == 'user':
            return path_parts[1]
        else:
            raise ValueError(f"Invalid Reddit profile URL: {profile_url}")

    def get_user_data(self, username: str, max_items: int = 1000) -> Dict[str, List]:
        """Fetch user posts and comments from Reddit JSON API.
        
        Args:
            username: Reddit username
            max_items: Maximum number of posts/comments to fetch
            
        Returns:
            Dictionary containing posts and comments lists
        """
        posts = []
        comments = []

        print(f" Fetching posts for {username}...")

        # Fetch posts with pagination
        posts_after = None
        while len(posts) < max_items:
            posts_url = f"https://www.reddit.com/user/{username}/submitted.json?limit=100"
            if posts_after:
                posts_url += f"&after={posts_after}"

            try:
                posts_response = self.session.get(posts_url)
                posts_response.raise_for_status()
                posts_data = posts_response.json()

                new_posts = posts_data.get('data', {}).get('children', [])
                if not new_posts:
                    break

                posts.extend(new_posts)
                posts_after = posts_data.get('data', {}).get('after')

                print(f"    Fetched {len(posts)} posts...")

                if not posts_after:
                    break

                time.sleep(1)  # Rate limiting

            except requests.exceptions.RequestException as e:
                print(f" Error fetching posts: {e}")
                break

        print(f" Fetching comments for {username}...")

        # Fetch comments with pagination
        comments_after = None
        while len(comments) < max_items:
            comments_url = f"https://www.reddit.com/user/{username}/comments.json?limit=100"
            if comments_after:
                comments_url += f"&after={comments_after}"

            try:
                comments_response = self.session.get(comments_url)
                comments_response.raise_for_status()
                comments_data = comments_response.json()

                new_comments = comments_data.get('data', {}).get('children', [])
                if not new_comments:
                    break

                comments.extend(new_comments)
                comments_after = comments_data.get('data', {}).get('after')

                print(f"    Fetched {len(comments)} comments...")

                if not comments_after:
                    break

                time.sleep(1)  # Rate limiting

            except requests.exceptions.RequestException as e:
                print(f" Error fetching comments: {e}")
                break

        return {
            'posts': posts[:max_items],
            'comments': comments[:max_items]
        }

    def analyze_with_groq(self, username: str, posts: List, comments: List) -> str:
        """Use GROQ API to analyze Reddit content and generate persona.
        
        Args:
            username: Reddit username
            posts: List of post data
            comments: List of comment data
            
        Returns:
            Generated persona analysis text
        """
        print(" Analyzing content with GROQ AI...")
        print("   This may take 1-2 minutes for comprehensive analysis...")

        # Prepare content for AI analysis
        posts_text = ""
        comments_text = ""
        subreddits = {}

        # Process posts
        for post in posts[:10]:  # Limit to recent posts for AI
            post_data = post.get('data', {})
            subreddit = post_data.get('subreddit', '')
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')

            subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
            posts_text += f"Post in r/{subreddit}: {title} - {selftext[:200]}...\n"

        # Process comments
        for comment in comments[:20]:  # Limit to recent comments for AI
            comment_data = comment.get('data', {})
            subreddit = comment_data.get('subreddit', '')
            body = comment_data.get('body', '')

            subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
            comments_text += f"Comment in r/{subreddit}: {body[:200]}...\n"

        # Get top subreddits
        top_subreddits = sorted(subreddits.items(), 
                              key=lambda x: x[1], reverse=True)[:10]
        subreddits_text = ", ".join([f"r/{sub} ({count})" 
                                   for sub, count in top_subreddits])

        # Create AI prompt
        prompt = f"""
Analyze this Reddit user and create a comprehensive persona for: {username}

ACTIVITY SUMMARY:
- Total Posts: {len(posts)}
- Total Comments: {len(comments)}
- Top Subreddits: {subreddits_text}

RECENT POSTS:
{posts_text}

RECENT COMMENTS:
{comments_text}

Please provide a detailed persona analysis with:
1. Basic Information (age, location, occupation estimates)
2. Personality Traits (with confidence levels)
3. Interests and Hobbies
4. Communication Style
5. Demographic Indicators
6. Behavioral Patterns
7. Values and Beliefs
8. Motivations and Goals
9. Frustrations and Pain Points
10. Business/Marketing Insights

Format as a structured report with clear sections and evidence-based conclusions.
IMPORTANT: Please provide the response in plain text format without any markdown formatting (no asterisks, no bold text, no italic text).
"""

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", 
                     "content": "You are an expert user researcher and data "
                               "analyst specializing in social media behavior analysis."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192",
                temperature=0.1,
                max_tokens=4000,
                top_p=0.9,
                stream=False,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error during AI analysis: {e}"

    def clean_markdown_formatting(self, text: str) -> str:
        """Clean markdown formatting from text for plain text output.
        
        Args:
            text: Text with markdown formatting
            
        Returns:
            Cleaned plain text
        """
        # Remove markdown bold formatting (**text**)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        
        # Remove markdown italic formatting (*text*)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        
        # Clean up any remaining asterisks
        text = text.replace('*', '')
        
        # Fix multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Fix line breaks
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text.strip()

    def save_results(self, username: str, analysis_result: str, 
                    filename: str, posts: List, comments: List) -> bool:
        """Save the analysis results to a file.
        
        Args:
            username: Reddit username
            analysis_result: AI-generated analysis
            filename: Output filename
            posts: List of post data
            comments: List of comment data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Clean the analysis result from markdown formatting
            cleaned_analysis = self.clean_markdown_formatting(analysis_result)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== AI-POWERED REDDIT PERSONA ANALYSIS ===\n")
                f.write(f"Username: {username}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Posts Analyzed: {len(posts)}\n")
                f.write(f"Total Comments Analyzed: {len(comments)}\n")
                f.write(f"\n{cleaned_analysis}\n")
                f.write("\n=== ANALYSIS COMPLETED ===\n")
                f.write("Powered by GROQ AI (Llama 3 70B)\n")

            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False

    def run_interactive_analysis(self) -> None:
        """Main interactive analysis function."""
        try:
            # Get user input
            profile_url, filename, max_items = self.get_user_input()

            print("\n Starting Analysis...")
            

            # Extract username
            username = self.extract_username(profile_url)

            # Fetch data
            user_data = self.get_user_data(username, max_items)

            if not user_data['posts'] and not user_data['comments']:
                print(f" No data found for user {username}")
                print("   Profile may be private, deleted, or non-existent.")
                return

            print(f" Found {len(user_data['posts'])} posts "
                  f"and {len(user_data['comments'])} comments")

            # Analyze with AI
            analysis_result = self.analyze_with_groq(
                username, user_data['posts'], user_data['comments'])

            # Save results
            if self.save_results(username, analysis_result, filename, 
                               user_data['posts'], user_data['comments']):
                print("\n")
                print(" Analysis completed successfully!")
                print(f" Results saved to: {filename}")

                # Ask if user wants to view results
                print("\n Would you like to view the results?")
                view_choice = input("   View now? (y/n): ").strip().lower()

                if view_choice in ['y', 'yes']:
                    print("\n")
                    print(" ANALYSIS RESULTS")
                    print("\n")
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            print(f.read())
                    except Exception as e:
                        print(f" Error reading file: {e}")

                print("\n")
                print(" Thank you for using the Reddit Persona AI!")
                print("\n")

        except KeyboardInterrupt:
            print("\n Analysis cancelled by user.")
        except Exception as e:
            print(f" Error: {e}")
            print("\nPlease check:")
            print("1. Your internet connection")
            print("2. GROQ API key in .env file")
            print("3. Reddit profile URL format")


def main() -> None:
    """Main function."""
    # Check if GROQ API key is set
    if not os.getenv('GROQ_API_KEY'):
        print(" GROQ API key not found!")
        print("\nPlease set up your API key:")
        print("1. Get API key from: https://console.groq.com")
        print("2. Create .env file with: GROQ_API_KEY=your_key_here")
        print("3. Run this script again")
        return

    try:
        scraper = InteractiveRedditPersonaScraper()
        scraper.run_interactive_analysis()
    except Exception as e:
        print(f" Failed to initialize scraper: {e}")


if __name__ == "__main__":
    main()
