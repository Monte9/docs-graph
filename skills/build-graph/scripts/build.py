#!/usr/bin/env python3
"""
Scans a docs folder for .md files with YAML frontmatter,
extracts metadata, and generates graph.json for the viewer.

Usage:
    python build.py                     # scans docs/ sibling of _graph/
    python build.py /path/to/docs       # scans a specific folder

Project grouping:
    - If run from inside a project folder (e.g., rosebud/_graph/),
      all docs belong to that project (named after the folder).
    - If run from a parent strategy folder containing multiple projects,
      each subfolder is its own project.
"""

import os
import sys
import json
import re


def parse_frontmatter(filepath):
    """Extract YAML frontmatter and body from a markdown file.
    Returns (meta_dict, body_string) or (None, full_content)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return None, content

    end = content.find('---', 3)
    if end == -1:
        return None, content

    fm_text = content[3:end].strip()
    body = content[end + 3:].lstrip('\n')
    meta = {}
    current_key = None
    current_list = None

    for line in fm_text.split('\n'):
        if line.strip().startswith('- ') and current_key:
            if current_list is None:
                current_list = []
            current_list.append(line.strip()[2:].strip())
            meta[current_key] = current_list
            continue

        match = re.match(r'^(\w+)\s*:\s*(.*)', line)
        if match:
            current_list = None
            key = match.group(1)
            value = match.group(2).strip()
            current_key = key
            if value:
                meta[key] = value
                current_list = None
            else:
                meta[key] = []
                current_list = meta[key]

    return meta, body


def is_external_ref(ref):
    """Check if a reference is an external URL."""
    return ref.startswith('http://') or ref.startswith('https://')


def external_node_name(url):
    """Generate a short display name for an external URL."""
    # Notion pages: extract the page name from the URL
    match = re.search(r'/([A-Za-z0-9-]+)-[a-f0-9]{32}', url)
    if match:
        name = match.group(1).replace('-', ' ')
        # Capitalize
        return name.title()
    return url.split('/')[-1][:30]


def scan_folder(root_path):
    """Scan all .md files under root_path."""
    root_name = os.path.basename(os.path.normpath(root_path))

    # Detect mode: are there subdirs that look like projects (contain .md files)?
    # Or is this a single project with date subdirs?
    # Heuristic: if first-level subdirs contain .md files directly, they're projects.
    # If first-level subdirs contain only more subdirs (dates), this is a single project.
    first_level_dirs = [
        d for d in os.listdir(root_path)
        if os.path.isdir(os.path.join(root_path, d))
        and not d.startswith('_') and not d.startswith('.')
    ]

    # Check if any first-level dir has .md files nested inside
    multi_project = False
    for d in first_level_dirs:
        subpath = os.path.join(root_path, d)
        for _, _, files in os.walk(subpath):
            if any(f.endswith('.md') for f in files):
                # Check if this dir name looks like a date (YYYY-MM-DD)
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', d):
                    multi_project = True
                break

    projects = {}
    nodes = []
    edges = []
    external_nodes = {}  # url -> node

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('_') and not d.startswith('.')]

        for fname in filenames:
            if not fname.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(filepath, root_path)
            parts = rel_path.split(os.sep)

            if multi_project:
                project = parts[0] if len(parts) > 1 else root_name
            else:
                project = root_name

            meta, body = parse_frontmatter(filepath)
            if meta is None:
                meta = {
                    'name': fname.replace('.md', '').replace('-', ' ').title(),
                    'type': 'note',
                    'description': '',
                    'references': []
                }

            node_id = rel_path
            node = {
                'id': node_id,
                'name': meta.get('name', fname.replace('.md', '')),
                'type': meta.get('type', 'note'),
                'description': meta.get('description', ''),
                'date': meta.get('date', ''),
                'project': project,
                'path': rel_path,
                'external': False,
                'content': body,
            }
            nodes.append(node)

            if project not in projects:
                projects[project] = []
            projects[project].append(node_id)

            # Build edges from references
            refs = meta.get('references', [])
            if isinstance(refs, str):
                refs = [refs]
            for ref in refs:
                edges.append({'source': node_id, 'target': ref})

                # Track external references as special nodes
                if is_external_ref(ref) and ref not in external_nodes:
                    ext_name = external_node_name(ref)
                    external_nodes[ref] = {
                        'id': ref,
                        'name': ext_name,
                        'type': 'external',
                        'description': ref,
                        'date': '',
                        'project': '_external',
                        'path': ref,
                        'external': True,
                    }

    # Add external nodes
    if external_nodes:
        nodes.extend(external_nodes.values())
        projects['_external'] = list(external_nodes.keys())

    return {
        'projects': {k: {'nodes': v} for k, v in projects.items()},
        'nodes': nodes,
        'edges': edges,
    }


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        # _graph/ lives at the project root; docs/ is a sibling directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        root = os.path.join(project_root, 'docs')
        if not os.path.isdir(root):
            print(f"No docs/ folder found at {root}")
            print("Create it or pass a path: python build.py /path/to/docs")
            sys.exit(1)

    print(f"Scanning: {root}")
    graph = scan_folder(root)
    print(f"Found {len(graph['nodes'])} docs across {len(graph['projects'])} project(s)")
    print(f"Found {len(graph['edges'])} references")

    for proj, data in graph['projects'].items():
        print(f"  {proj}: {len(data['nodes'])} docs")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Write graph.json
    out_path = os.path.join(script_dir, 'graph.json')
    with open(out_path, 'w') as f:
        json.dump(graph, f, indent=2)
    print(f"Wrote {out_path}")

    # Embed data into index.html (replaces the GRAPH_DATA placeholder)
    html_path = os.path.join(script_dir, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            html = f.read()

        # Replace the GRAPH_DATA block between markers
        start_marker = '// __GRAPH_DATA_START__'
        end_marker = '// __GRAPH_DATA_END__'
        s_idx = html.index(start_marker)
        e_idx = html.index(end_marker) + len(end_marker)
        embedded = start_marker + '\nconst GRAPH_DATA = ' + json.dumps(graph, indent=2) + ';\n' + end_marker
        new_html = html[:s_idx] + embedded + html[e_idx:]

        with open(html_path, 'w') as f:
            f.write(new_html)
        print(f"Embedded data into {html_path}")


if __name__ == '__main__':
    main()
