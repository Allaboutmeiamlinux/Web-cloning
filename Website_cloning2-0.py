import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib

class WebsiteCloner:
    def __init__(self, base_url, output_dir='cloned_site'):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited = set()

    def sanitize_path(self, path):
        # Remove invalid characters and shorten if necessary
        sanitized_path = "".join(c for c in path if c.isalnum() or c in [' ', '.', '_', '/']).rstrip()
        if len(sanitized_path) > 255:
            sanitized_path = hashlib.md5(sanitized_path.encode()).hexdigest()
        return sanitized_path

    def save_file(self, url, content):
        parsed_url = urlparse(url)
        file_path = os.path.join(self.output_dir, parsed_url.netloc, parsed_url.path.lstrip('/'))
        file_path = self.sanitize_path(file_path)
        
        if not os.path.splitext(file_path)[1]:
            file_path = os.path.join(file_path, 'index.html')
        
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except OSError as e:
            print(f'\033[31mFailed to create directory: {e}\033[0m')
            return
        
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f'\033[32mSaved: {file_path}\033[0m')

    def fetch(self, url):
        try:
            response = requests.get(url, verify=False)  # Disable SSL certificate verification
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f'\033[31mFailed to fetch {url}: {e}\033[0m')
            return None

    def parse_links(self, content, base_url):
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        tags_attrs = {
            'a': 'href',
            'link': 'href',
            'script': 'src',
            'img': 'src',
            'audio': 'src',
            'video': 'src',
            'source': 'src',
            'iframe': 'src',
            'embed': 'src',
            'object': 'data',
            'applet': 'code',
        }
        
        for tag, attr in tags_attrs.items():
            for element in soup.find_all(tag):
                link = element.get(attr)
                if link:
                    full_link = urljoin(base_url, link)
                    if self.is_same_domain(full_link):
                        links.add(full_link)
        return links

    def is_same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.base_url).netloc

    def clone(self, url):
        if url in self.visited:
            return
        print(f'Cloning: {url}')
        content = self.fetch(url)
        if content:
            self.save_file(url, content)
            self.visited.add(url)
            for link in self.parse_links(content, url):
                self.clone(link)

    def run(self):
        self.clone(self.base_url)
        print('\033[32mCloning completed.\033[0m')

def main():
    print('''\033[0;34m\t
    __        __   _         _ _              _             _             
    \ \      / /__| |__  ___(_) |_ ___    ___| | ___  _ __ (_)_ __   __ _ 
     \ \ /\ / / _ \ '_ \/ __| | __/ _ \  / __| |/ _ \| '_ \| | '_ \ / _` |
      \ V  V /  __/ |_) \__ \ | ||  __/ | (__| | (_) | | | | | | | | (_| |
       \_/\_/ \___|_.__/|___/_|\__\___|  \___|_|\___/|_| |_|_|_| |_|\__, |
                                                                    |___/ 
                                                                       2.O 
                                                            
                                                                  By linux
    \033[0m\n''')
    x = int(input("Enter password:-"))
    if x == 2002:
        print("\033[32m\tAccess Granted\033[0m")
        time.sleep(1)
        os.system('clear')
        print('''\033[0;35m\t
        __        __   _         _ _              _             _             
        \ \      / /__| |__  ___(_) |_ ___    ___| | ___  _ __ (_)_ __   __ _ 
         \ \ /\ / / _ \ '_ \/ __| | __/ _ \  / __| |/ _ \| '_ \| | '_ \ / _` |
          \ V  V /  __/ |_) \__ \ | ||  __/ | (__| | (_) | | | | | | | | (_| |
           \_/\_/ \___|_.__/|___/_|\__\___|  \___|_|\___/|_| |_|_|_| |_|\__, |
                                                                        |___/ 
                                                                           2.0
                                                            
                                                                      By linux
        \033[0m\n''')
        base_url = input("Enter your website URL: ")
        cloner = WebsiteCloner(base_url)
        cloner.run()
        
    else:
        print("\t\033[31mAccess Denied!\033[0m\n")    
    
if __name__ == '__main__':
    main()
