from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class ComplianceManager:
    def __init__(self, user_agent="CS172-Team-Bot"):
        self.user_agent = user_agent
        self.parsers = {}  # Cache parsers so we don't fetch robots.txt repeatedly

    def can_fetch(self, url):
        """Checks robots.txt for a given URL."""
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_url}/robots.txt"

        if base_url not in self.parsers:
            rp = RobotFileParser()
            try:
                rp.set_url(robots_url)
                rp.read()
                self.parsers[base_url] = rp
            except:
                # If robots.txt fails to load, assume it's okay (or be strict and return False)
                return True
        
        return self.parsers[base_url].can_fetch(self.user_agent, url)

    def check_meta_tags(self, html_content):
        """Checks for 'noindex' or 'nofollow' in the HTML head."""
        soup = BeautifulSoup(html_content, 'html.parser')
        meta_robots = soup.find("meta", attrs={"name": "robots"})
        
        if meta_robots:
            content = meta_robots.get("content", "").lower()
            return {
                "noindex": "noindex" in content,
                "nofollow": "nofollow" in content
            }
        return {"noindex": False, "nofollow": False}