#!/bin/bash
# Package the docs-graph plugin for distribution
cd "$(dirname "$0")"
rm -f docs-graph.plugin
zip -r docs-graph.plugin . -x ".git/*" ".gitignore" "*.DS_Store" "*.plugin" "build.sh"
echo "Created docs-graph.plugin ($(du -h docs-graph.plugin | cut -f1))"
