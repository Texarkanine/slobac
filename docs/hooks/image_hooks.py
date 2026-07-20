from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files, File

def on_files(files: Files, config: MkDocsConfig) -> Files:
    root = Path(config.config_file_path).resolve().parent
    brand = root / "docs" / "img"
    assets = {
        "favicon.ico": brand / "favicon.ico"
    }
    for src_uri, abs_path in assets.items():
        if not abs_path.is_file():
            raise FileNotFoundError(f"brand asset missing: {abs_path}")
        files.append(File.generated(config, src_uri, abs_src_path=str(abs_path)))
    return files