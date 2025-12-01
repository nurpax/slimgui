#!/bin/bash
set -e

rm -rf docs/dist && npm run docs:build
CACHE_DIR=.cache npx gh-pages -d docs/dist --nojekyll
