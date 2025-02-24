import argparse
import os
import requests
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
        directory = os.path.dirname(path) or "."
        filename = os.path.basename(path)

        os.makedirs(directory, exist_ok=True)
        
        full_path = os.path.join(directory, filename)
        
        if os.path.exists(full_path):
            base, ext = os.path.splitext(full_path)
            i = 1
            while os.path.exists(f"{base}_{i}{ext}"):
                i += 1
            full_path = f"{base}_{i}{ext}"

        with open(full_path, 'wb') as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=full_path
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"Downloaded: {full_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def exec_cmd(url, cmd_type):
    try:
        response = requests.get(url)
        response.raise_for_status()
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
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Error executing command: {e}")
    finally:
        if os.path.exists(tmpfile_path):
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
        file_name = get_filename(args.pic)
        full_path = os.path.join(out_path, file_name) if not os.path.isabs(args.out) else args.out
        download_urls.append((args.pic, full_path))
    elif args.file:
        file_name = get_filename(args.file)
        full_path = os.path.join(out_path, file_name) if not os.path.isabs(args.out) else args.out
        download_urls.append((args.file, full_path))
    elif args.cmd:
        cmd_type, url = args.cmd
        exec_cmd(url, cmd_type)
        return

    with ThreadPoolExecutor() as executor:
        for url, path in download_urls:
            executor.submit(download, url, path)

if __name__ == "__main__":
    main()
