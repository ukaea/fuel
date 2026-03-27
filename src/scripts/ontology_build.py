import os
from rdflib import Graph
import urllib.request
from shutil import rmtree, copytree, copy
import shutil
import subprocess

ONTO_DIR = os.environ['ONTO_DIR']
ONTO_FILE = os.environ['ONTO_FILE']
ONTO_ABBREV = os.environ['ONTO_ABBREV']
DOCS_DIR = os.environ['DOCS_DIR']
RELEASES_DIR = os.environ['RELEASES_DIR']

RELEASE_VERSION = os.environ.get('RELEASE_VERSION')
BUILD_DIR = os.environ.get('BUILD_DIR')
IS_MAIN = os.environ.get('IS_MAIN') == 'true'
CURRENT_VERSION = os.environ.get('CURRENT_VERSION', '')

g = Graph()
g.parse(os.path.join(ONTO_DIR, ONTO_FILE))
target_fmts = [("ttl","turtle"),("jsonld","json-ld"),("nt","nt"),("owl","xml"),("n3","n3"),("trig","trig")]
      
# function to generate the ontology syntaxes
def generate_syntaxes(outdir):
    os.makedirs(outdir, exist_ok=True)
    for ext, fmt in target_fmts:
        g.serialize(
            destination=os.path.join(outdir, f"{ONTO_ABBREV}.{ext}"),
            format=fmt,
            encoding="utf-8"
            )
        
# function to create the documentation with pylode
def generate_pylode_docs(outdir):
    pylode_outdir = os.path.join(outdir, "pylode")
    os.makedirs(pylode_outdir, exist_ok=True)
    try:
        subprocess.run([
            "pylode",
            "-o", os.path.join(pylode_outdir, "index"),
            os.path.join(ONTO_DIR, ONTO_FILE)
        ], check=True)
        print(f"Pylode documentation generated at {pylode_outdir}")
    except FileNotFoundError:
        print("Warning: pylode executable not found; skipping pylode docs.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: pylode exited with code {e.returncode}; skipping pylode docs.")
        print(str(e))
        print("If this is pylode 3.4.x, pin pylode==3.2.1 in CI or requirements.")
        return
        
# function to create the documentation with ontospy
def generate_ontospy_docs(outdir):
    ontospy_outdir = os.path.join(outdir, "ontospy")
    os.makedirs(ontospy_outdir, exist_ok=True)
    try:
        from ontospy import Ontospy
        o = Ontospy(os.path.join(ONTO_DIR, ONTO_FILE))
        o.html(ontospy_outdir)
        print(f"Ontospy documentation generated at {ontospy_outdir}")
    except ImportError as e:
        print(f"Warning: ontospy import failed: {e}; skipping ontospy docs.")
    except Exception as e:
        print(f"Warning: ontospy execution failed: {e}; skipping ontospy docs.")
        
# function to create the documentation with widoco
def generate_widoco_docs(outdir, onto_dir, onto_file, version="1.4.25"):
    widoco_dir = os.path.join(outdir, "widoco")
    os.makedirs(widoco_dir, exist_ok=True)
    widoco_jar = os.path.join(widoco_dir, "widoco.jar")

    # Download Widoco if not already present
    if not os.path.exists(widoco_jar):
        url = f"https://github.com/dgarijo/Widoco/releases/download/v{version}/widoco-{version}-jar-with-dependencies_JDK-17.jar"
        print(f"Downloading Widoco {version}...")
        urllib.request.urlretrieve(url, widoco_jar)

    # Run Widoco
    cmd = [
        "java", "-jar", widoco_jar,
        "-ontFile", os.path.join(onto_dir, onto_file),
        "-oops", "-webVowl", "-includeAnnotationProperties",
        "-outFolder", widoco_dir,
        "-rewriteAll", "-includeImportedOntologies", "-uniteSections", "-excludeIntroduction",
        "-lang", "en-es"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Widoco documentation generated at {widoco_dir}")

        # Copy index-en.html to index.html if it exists
        index_en = os.path.join(widoco_dir, "index-en.html")
        index_default = os.path.join(widoco_dir, "index.html")
        if os.path.exists(index_en):
            shutil.copy(index_en, index_default)
            print("Copied index-en.html → index.html")
        else:
            print("index-en.html not found, skipping copy.")

    except subprocess.CalledProcessError as e:
        print("Widoco execution failed:")
        print(e)

def generate_index(outdir, title, heading, is_root_main=False):
    index_path = os.path.join(outdir, 'index.html')
    with open(index_path, 'w') as f:
        f.write(f"<html><head><title>{title}</title></head><body>\n")
        f.write(f"<h1>{heading}</h1>\n<ul>\n")
        f.write('<li><a href="docs/pylode/">Pylode Documentation</a></li>\n')
        f.write('<li><a href="docs/widoco/">Widoco Documentation</a></li>\n')
        f.write('<li><a href="docs/ontospy/">Ontospy Documentation</a></li>\n')
        for ext, fmt in target_fmts:
            f.write(f'<li><a href="{ONTO_ABBREV}.{ext}">{ONTO_ABBREV}.{ext}</a></li>\n')
        f.write("</ul>\n")
        if is_root_main:
            f.write('<h2><a href="releases/">Previous Releases</a></h2>\n')
            f.write('<h2><a href="dev/">Development Build</a></h2>\n')
        f.write("</body></html>\n")

if RELEASE_VERSION:
# --- release build ---
    release_dir = os.path.join(RELEASES_DIR, RELEASE_VERSION)
    generate_syntaxes(release_dir)

    release_docs_dir = os.path.join(release_dir, "docs")
    generate_pylode_docs(release_docs_dir)
    generate_widoco_docs(release_docs_dir, ONTO_DIR, ONTO_FILE)
    generate_ontospy_docs(release_docs_dir)

    # Generate index for this specific release
    generate_index(
        release_dir,
        title=f"FUEL Ontology Release {RELEASE_VERSION}",
        heading=f"FUEL Ontology (Release {RELEASE_VERSION})",
        is_root_main=False
    )

    # Update latest
    latest_dir = os.path.join(RELEASES_DIR, "latest")
    if os.path.exists(latest_dir):
        rmtree(latest_dir)
        copytree(release_dir, latest_dir)

    # Generate releases index.html
    releases_index = os.path.join(RELEASES_DIR, 'index.html')
    release_folders = sorted([d for d in os.listdir(RELEASES_DIR) if os.path.isdir(os.path.join(RELEASES_DIR,d))])
    with open(releases_index, 'w') as f:
        f.write("<html><head><title>FUEL Releases</title></head><body>\n")
        f.write("<h1>FUEL Ontology Releases</h1>\n<ul>\n")
        for r in release_folders:
            f.write(f'<li><a href="{r}/">{r}</a></li>\n')
        f.write("</ul>\n</body></html>\n")

if BUILD_DIR:
    # --- base build ---
    generate_syntaxes(BUILD_DIR)

    build_docs_dir = os.path.join(BUILD_DIR, "docs")
    generate_pylode_docs(build_docs_dir)
    generate_widoco_docs(build_docs_dir, ONTO_DIR, ONTO_FILE)
    generate_ontospy_docs(build_docs_dir)

   # Generate build index.html
    if IS_MAIN:
        title = f"FUEL Ontology (v{CURRENT_VERSION})" if CURRENT_VERSION else "FUEL Ontology"
        heading = f"FUEL Ontology (Latest Release v{CURRENT_VERSION})" if CURRENT_VERSION else "FUEL Ontology (Latest Release)"
    else:
        title = "FUEL Development Build"
        heading = "FUEL Ontology (Development Build)"
        
    generate_index(BUILD_DIR, title, heading, is_root_main=IS_MAIN)