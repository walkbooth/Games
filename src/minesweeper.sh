# !/bin/bash

set -eu

if [ ! -d "util" ]; then
    mkdir util
    echo "Created Minesweeper/util directory"
fi

if [ ! -f "util/config.yml" ]; then 
    
cat << 'EOF' > util/config.yml
width: 5                  # Width of the grid 
height: 5                 # Height of the grid 
bombs: 5                 # Number of bombs to spawn in grid 
EOF

    echo "Created example Minesweeper/util/config.yml file. Modify it to change your Minesweeper settings."
    echo "Launching game in 3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1

fi

python3 src/ui.py