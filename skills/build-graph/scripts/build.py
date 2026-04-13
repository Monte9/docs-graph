#!/usr/bin/env python3
"""
Scans a docs folder for .md files with YAML frontmatter,
extracts metadata, and generates graph.json for the viewer.
Also scans a data/ folder for research nodes.

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
    # Notion pages with workspace + slug: /workspace/Slug-Name-<32hex>
    match = re.search(r'/([A-Za-z0-9-]+)-[a-f0-9]{32}', url)
    if match:
        name = match.group(1).replace('-', ' ')
        return name.title()
    # Bare Notion page IDs: notion.so/<32hex> — no readable name available
    if re.search(r'notion\.so/[a-f0-9]{32}$', url):
        return url.split('/')[-1][:12] + '…'
    return url.split('/')[-1][:30]


def scan_data_folder(data_path, nodes, edges, projects):
    """Scan data/ folder for research nodes.
    Each subfolder becomes a 'research' node. Source .md files inside
    are counted, and facts.csv presence is noted.
    projects must be a dict (will be mutated to add '_research' key)."""
    if not os.path.isdir(data_path):
        return
    if not isinstance(projects, dict):
        raise TypeError(f"projects must be a dict, got {type(projects).__name__}")

    for folder in sorted(os.listdir(data_path)):
        folder_path = os.path.join(data_path, folder)
        if not os.path.isdir(folder_path) or folder.startswith('.') or folder.startswith('_'):
            continue

        # Walk all subdirectories to find .md source files and facts.csv
        all_source_files = []  # (subfolder_name, filename) tuples
        top_level_md = []
        has_facts = False
        fact_count = 0

        for item in sorted(os.listdir(folder_path)):
            item_path = os.path.join(folder_path, item)
            if item == 'facts.csv':
                has_facts = True
                with open(item_path, 'r', encoding='utf-8') as f:
                    fact_count = max(0, sum(1 for line in f if line.strip()) - 1)
            elif item.endswith('.md'):
                top_level_md.append(item)
            elif os.path.isdir(item_path) and not item.startswith('.'):
                # Scan subdirectory for .md files
                sub_files = sorted(f for f in os.listdir(item_path) if f.endswith('.md'))
                for sf in sub_files:
                    all_source_files.append((item, sf))

        total_sources = len(top_level_md) + len(all_source_files)

        # Build content for the side panel
        display_name = folder.replace('-', ' ').title()
        content_parts = [f"# {display_name}\n\n"]
        content_parts.append(f"**{total_sources} source files**")
        if has_facts:
            content_parts.append(f" | **{fact_count} facts**")
        content_parts.append('\n\n')

        # Group sources by subdirectory
        if all_source_files:
            # Collect unique subdirectories in order
            seen_subs = []
            for sub, _ in all_source_files:
                if sub not in seen_subs:
                    seen_subs.append(sub)
            for sub in seen_subs:
                sub_display = sub.replace('-', ' ').title()
                sub_sources = [sf for s, sf in all_source_files if s == sub]
                content_parts.append(f"### {sub_display}\n")
                for sf in sub_sources:
                    name = sf.replace('.md', '').replace('-', ' ').title()
                    content_parts.append(f"- {name}\n")
                content_parts.append('\n')

        if top_level_md:
            if all_source_files:
                content_parts.append('### Other\n')
            for sf in top_level_md:
                name = sf.replace('.md', '').replace('-', ' ').title()
                content_parts.append(f"- {name}\n")

        node_id = f"data/{folder}"
        description = f"Research: {total_sources} sources"
        if has_facts:
            description += f", {fact_count} facts"

        node = {
            'id': node_id,
            'name': display_name,
            'type': 'research',
            'description': description,
            'date': '',
            'project': '_research',
            'path': f"data/{folder}",
            'external': False,
            'content': ''.join(content_parts),
        }
        nodes.append(node)

        if '_research' not in projects:
            projects['_research'] = []
        projects['_research'].append(node_id)


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

            # Only include files that have all three required fields:
            # name, date, and type. This filters out random READMEs,
            # changelogs, and other .md files that weren't created
            # with the docs-graph frontmatter format.
            if meta is None:
                continue
            required = ('name', 'date', 'type')
            if not all(meta.get(k) for k in required):
                continue

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
            # Pass through chart path for chart-type docs
            if meta.get('chart'):
                node['chart'] = meta['chart']
            nodes.append(node)

            if project not in projects:
                projects[project] = []
            projects[project].append(node_id)

            # Build edge from data field (links doc to research node)
            data_ref = meta.get('data', '').strip()
            if data_ref:
                # Strip leading data/ if someone includes it in frontmatter
                if data_ref.startswith('data/'):
                    data_ref = data_ref[5:]
                edges.append({'source': node_id, 'target': f"data/{data_ref}"})

            # Build edges from references
            refs = meta.get('references', [])
            if isinstance(refs, str):
                refs = [refs]
            for ref in refs:
                # Normalize relative local paths.
                # If the ref starts with ../ it's relative to the file's dir.
                # If it looks like YYYY-MM-DD/file.md it's already root-relative.
                # Either way, normpath cleans it up.
                if not is_external_ref(ref):
                    if ref.startswith('.'):
                        ref = os.path.normpath(os.path.join(os.path.dirname(rel_path), ref))
                    else:
                        ref = os.path.normpath(ref)
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
        # _graph/ lives at the project root; prefer docs/ if it exists,
        # otherwise scan the whole root (frontmatter filter keeps it clean)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        docs_dir = os.path.join(project_root, 'docs')
        root = docs_dir if os.path.isdir(docs_dir) else project_root

    print(f"Scanning: {root}")
    graph = scan_folder(root)

    # Scan data/ folder for research nodes
    script_dir_tmp = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir_tmp)
    data_dir = os.path.join(project_root, 'data')
    research_projects = {}
    if os.path.isdir(data_dir):
        scan_data_folder(data_dir, graph['nodes'], graph['edges'], research_projects)
        for k, v in research_projects.items():
            graph['projects'][k] = {'nodes': v}

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
