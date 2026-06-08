import requests
import re
import json
import os
import time

BASE_URL = "https://raw.githubusercontent.com/cporter202/API-mega-list/main/"

def get_categories():
    print("Discovering categories from root README...")
    response = requests.get(BASE_URL + "README.md")
    if response.status_code != 200:
        print(f"Error fetching root README: {response.status_code}")
        return []

    # Matches: - [CategoryName](./category-path/)
    # We use a non-greedy match for the name and path
    pattern = r"- \[(.*?)\]\(\.\/(.*?)\/\)"
    categories = re.findall(pattern, response.text)
    print(f"Found {len(categories)} categories.")
    return categories

def fetch_category_apis(cat_name, cat_path):
    url = f"{BASE_URL}{cat_path}/README.md"
    print(f"Fetching {cat_name} from {url}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"  [!] Failed to fetch {cat_name}: {response.status_code}")
            return []
    except Exception as e:
        print(f"  [!] Exception fetching {cat_name}: {e}")
        return []

    # Markdown table row pattern: | [Name](Link) | Description |
    # We skip rows that look like headers or separators
    apis = []
    lines = response.text.split('\n')
    for line in lines:
        if line.strip().startswith('|') and '[' in line and '](' in line:
            # Match | [Name](Link) | Description |
            match = re.search(r"\| \[(.*?)\]\((.*?)\) \| (.*?) \|", line)
            if match:
                name = match.group(1).strip()
                link = match.group(2).strip()
                desc = match.group(3).strip()
                # Simple validation to avoid separators like |---|
                if name and link and desc and not all(c in '-:| ' for c in name):
                    apis.append({
                        "name": name,
                        "link": link,
                        "description": desc,
                        "category": cat_name,
                        "source": "mega-list"
                    })

    print(f"  [+] Found {len(apis)} APIs in {cat_name}.")
    return apis

def integrate():
    categories = get_categories()
    if not categories:
        print("No categories found. Integration aborted.")
        return

    all_new_apis = []
    for name, path in categories:
        cat_apis = fetch_category_apis(name, path)
        all_new_apis.extend(cat_apis)
        # GitHub raw content usually doesn't have strict rate limits but let's be safe
        time.sleep(0.1)

    data_path = 'data/apis.json'
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            apis = json.load(f)
    else:
        apis = []

    # De-duplicate by name and link to keep the registry clean
    seen = {(a['name'], a['link']) for a in apis}
    added_count = 0
    for api in all_new_apis:
        key = (api['name'], api['link'])
        if key not in seen:
            apis.append(api)
            seen.add(key)
            added_count += 1

    # Ensure data directory exists
    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    with open(data_path, 'w') as f:
        json.dump(apis, f, indent=2)

    print(f"\nBulk Integration Complete.")
    print(f"New unique APIs added: {added_count}")
    print(f"Final Registry Total: {len(apis)}")

if __name__ == "__main__":
    integrate()
