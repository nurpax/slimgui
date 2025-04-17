#!/bin/bash
set -e

CACHE_DIR=.cache npx gh-pages -d dist
