##!/bin/bash

# Create .streamlit folder
mkdir -p ~/.streamlit/

# Create config.toml file
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
