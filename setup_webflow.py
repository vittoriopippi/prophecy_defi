from pathlib import Path
import shutil
from tqdm import tqdm
import argparse
import zipfile
import re

parser = argparse.ArgumentParser(description='Setup webflow project')
parser.add_argument('zip_folder', type=str, help='Path to zip folder')
parser.add_argument('--webflow_path', type=str, default='tmp_webflow', help='Path to tmp folder')
parser.add_argument('--templates_path', type=str, default='templates', help='Path to templates folder')
parser.add_argument('--static_path', type=str, default='static', help='Path to static folder')
parser.add_argument('--keep_old', action='store_true', help='Keep old folders')
args = parser.parse_args()

webflow = Path(args.webflow_path)
templates = Path(args.templates_path)
static = Path(args.static_path)

assert Path(args.zip_folder).exists(), f'Path {args.zip_folder} does not exist'

if not args.keep_old:
    shutil.rmtree(webflow, ignore_errors=True)
    shutil.rmtree(templates, ignore_errors=True)
    shutil.rmtree(static, ignore_errors=True)

webflow.mkdir(exist_ok=True)
with zipfile.ZipFile(args.zip_folder, 'r') as zip_ref:
    zip_ref.extractall(webflow)

templates.mkdir(exist_ok=True)
static.mkdir(exist_ok=True)

all_urls = {str(path.relative_to(webflow).as_posix()): path for path in webflow.rglob('*') if path.is_file()}

static_files = [path for path in webflow.rglob('*') if path.suffix != '.html' and path.is_file()]
for path in tqdm(static_files, desc='Copying static files'):
    if path.suffix != '.html' and path.is_file():
        dst_path = static / path.relative_to(webflow)
        dst_path.parent.mkdir(exist_ok=True)

        if path.suffix == '.css':
            text = path.read_text(encoding='utf-8')
            url_pattern = re.compile(r'url\([\'"]?(.*?)[\'"]?\)', re.IGNORECASE)
            for css_url in set(re.findall(url_pattern, text)):
                css_url_key = '/'.join(Path(css_url).parts[-2:])
                if css_url_key in all_urls:
                    text = text.replace(css_url, f'/static/{css_url_key}')
            dst_path.write_text(text, encoding='utf-8')
        else:
            shutil.copy(path, dst_path)

static_folders = [path.name for path in static.iterdir() if path.is_dir()]
templates_files = [path for path in webflow.rglob('*.html') if path.is_file()]
for path in tqdm(templates_files, desc='Copying templates'):
    text = path.read_text(encoding='utf-8')

    urls = set(re.findall(r'href="([^"]*)"', text))
    urls.update(set(re.findall(r'src="([^"]*)"', text)))
    urls.update(set(sum([[s.split()[0] for s in sset.split(', ')] for sset in re.findall(r'srcset="([^"]*)"', text)], [])))
    urls = {'/'.join(Path(url).parts[-2:]): url for url in urls}

    for key, url in urls.items():
        if key in all_urls:
            if any(key.startswith(folder) for folder in static_folders):
                text = text.replace(url, f'/static/{key}')
            elif url.endswith('.html'):
                text = text.replace(url, f'/{key}'[:-5])
            else:
                raise ValueError(f'Unknown url {url}')
    
    dst_path = templates / path.relative_to(webflow)
    dst_path.parent.mkdir(exist_ok=True)
    dst_path.write_text(text, encoding='utf-8')
    
