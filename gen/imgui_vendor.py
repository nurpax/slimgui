# See DEVELOPMENT.md on how to use this.

import shutil
import tempfile
import zipfile
import os
from contextlib import contextmanager

import urllib.request

@contextmanager
def temp_downloaded_unzipped_dir(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "archive.zip")
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, zip_path)
        print(f"Downloaded to {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        print(f"Extracted to {temp_dir}")
        yield temp_dir


def vendor_in(src_url, outdir, subdir: str | None = None):
    with temp_downloaded_unzipped_dir(src_url) as extracted_dir:
        subdirs = [d for d in os.listdir(extracted_dir) if os.path.isdir(os.path.join(extracted_dir, d))]
        if len(subdirs) != 1:
            raise RuntimeError(f"Expected exactly one subdirectory, found {len(subdirs)}: {subdirs}")
        src_dir = os.path.join(extracted_dir, subdirs[0])
        if subdir is not None:
            src_dir = os.path.join(src_dir, subdir)

        def ignore_github_dirs(dir, names):
            return [name for name in names if name == ".github"]

        shutil.rmtree(outdir)
        shutil.copytree(src_dir, outdir, ignore=ignore_github_dirs, dirs_exist_ok=True)

if __name__ == "__main__":
    imgui_src = "https://github.com/ocornut/imgui/archive/refs/tags/v1.92.1.zip"
    cimgui_src = "https://github.com/cimgui/cimgui/archive/refs/tags/1.92.0.zip" # 1.92.1 not available as of Jul 10, 2025, but 1.92.0 should work too
    implot_src = "https://github.com/epezent/implot/archive/3da8bd34299965d3b0ab124df743fe3e076fa222.zip"
    cimplot_src = "https://github.com/cimgui/cimplot/archive/98a6ee7762c6b208ec7df908119b3a8d549db977.zip"
    vendor_in(imgui_src, 'src/c/imgui')
    vendor_in(implot_src, 'src/c/implot')
    vendor_in(cimgui_src, 'gen/cimgui', 'generator/output')
    vendor_in(cimplot_src, 'gen/cimplot', 'generator/output')
