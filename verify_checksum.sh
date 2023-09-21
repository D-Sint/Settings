#!/bin/bash

# Function to display usage information
show_usage() {
    echo "Usage: $0 [OPTIONS] <file> <hashsum>"
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"
    exit 1
}

# Check if the script was invoked with the -h or --help option
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_usage
fi

# Check if both file and hashsum arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Error: Invalid number of arguments."
    show_usage
fi

file="$1"
expected_checksum="$2"

# Check if the file exists
if [ ! -e "$file" ]; then
    echo "Error: File '$file' does not exist."
    exit 1
fi

# Calculate the SHA-256 checksum of the file
checksum=$(sha256sum "$file" | cut -d " " -f1)

# Compare the calculated checksum with the expected checksum
if [ "$checksum" = "$expected_checksum" ]; then
    echo "Checksums match. The file is valid."
else
    echo "Checksums do not match. The file may be corrupted."
fi

