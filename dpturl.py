import argparse
import os
import requests
import shutil
import urllib.parse
import subprocess
import tempfile
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def get_filename(url):
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "downloaded_file"
    return filename

def download(url, path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        if os.path.exists(path):
            base, ext = os.path.splitext(path)
            i = 1
            while os.path.exists(f"{base}_{i}{ext}"):
                i += 1
            path = f"{base}_{i}{ext}"

        with open(path, 'wb') as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=path
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"Downloaded: {path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def exec_cmd(url, cmd_type):
    response = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(response.content)
        tmpfile_path = tmpfile.name
    if cmd_type == 'sh':
        command = f"bash {tmpfile_path}"
    elif cmd_type == 'python':
        command = f"python {tmpfile_path}"
    else:
        print(f"Unsupported command type: {cmd_type}")
        return
    subprocess.run(command, shell=True)
    os.remove(tmpfile_path)

def main():
    parser = argparse.ArgumentParser(description="Download files and execute commands.")
    parser.add_argument('-p', '--pic', type=str, help="Download an image file.")
    parser.add_argument('-f', '--file', type=str, help="Download a file.")
    parser.add_argument('-C', '--cmd', nargs=2, help="Execute command from a file (sh or python). First arg is the type (sh or python), second is the URL.")
    parser.add_argument('-o', '--out', type=str, help="Specify the output path for the downloaded file.")

    args = parser.parse_args()
    out_path = args.out if args.out else "."

    download_urls = []

    if args.pic:
        if os.path.dirname(args.out):
            full_path = args.out
        else:
            file_name = get_filename(args.pic)
            full_path = os.path.join(out_path, file_name)
        download_urls.append((args.pic, full_path))
    elif args.file:
        if os.path.dirname(args.out):
            full_path = args.out
        else:
            file_name = get_filename(args.file)
            full_path = os.path.join(out_path, file_name)
        download_urls.append((args.file, full_path))
    elif args.cmd:
        cmd_type, url = args.cmd
        exec_cmd(url, cmd_type)
        return

    with ThreadPoolExecutor() as executor:
        executor.map(lambda x: download(x[0], x[1]), download_urls)

if __name__ == "__main__":
    main()
