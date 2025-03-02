import argparse
import os
import requests
import urllib.parse
import tempfile
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def get_filename(url):
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_file"

def convert_to_raw_url(url):
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return url

def download(url, path):
    try:
        url = convert_to_raw_url(url)
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
    tmpfile_path = None
    try:
        url = convert_to_raw_url(url)
        response = requests.get(url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(response.content)
            tmpfile_path = tmpfile.name

        if cmd_type not in ['sh', 'python']:
            print(f"Unsupported command type: {cmd_type}")
            return

        command = [cmd_type, tmpfile_path] if cmd_type == 'python' else ['bash', tmpfile_path]
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error executing command: {e}")
    finally:
        if tmpfile_path and os.path.exists(tmpfile_path):
            os.remove(tmpfile_path)

def main():
    parser = argparse.ArgumentParser(description="Download files and execute commands.")
    parser.add_argument('-f', '--file', type=str, help="URL of the file to download.")
    parser.add_argument('-o', '--out', type=str, help="Output path (directory or full path).")
    parser.add_argument('-od', '--out-dir', type=str, help="Output directory.")
    parser.add_argument('-on', '--out-name', type=str, help="Output file name.")
    parser.add_argument('-C', '--cmd', nargs=2, help="Execute command from a file (sh or python). First arg is the type (sh or python), second is the URL.")

    args = parser.parse_args()

    if args.cmd:
        cmd_type, url = args.cmd
        exec_cmd(url, cmd_type)
        return

    if not args.file:
        print("Error: URL of the file to download is required.")
        return

    if args.out:
        if os.path.basename(args.out):
            out_path = args.out
        else:
            out_path = os.path.join(args.out, get_filename(args.file))
    elif args.out_dir or args.out_name:
        out_dir = args.out_dir or "."
        out_name = args.out_name or get_filename(args.file)
        out_path = os.path.join(out_dir, out_name)
    else:
        out_path = get_filename(args.file)

    download(args.file, out_path)

if __name__ == "__main__":
    main()
