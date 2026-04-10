#!/bin/bash
# Package the docs-graph plugin for distribution
cd "$(dirname "$0")"
rm -f docs-graph.zip
zip -r docs-graph.zip . \
  -x ".git/*" ".gitignore" "*.DS_Store" "*.zip" \
  "build.sh" "AGENTS.md" ".github/*"
echo "Created docs-graph.zip ($(du -h docs-graph.zip | cut -f1))"
