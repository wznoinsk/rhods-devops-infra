#!/bin/bash

# Path to the file containing the repository URLs and their associated file paths
REPO_URL_FILE="repo_url.txt"

# Check if the repository URL file exists
if [ ! -f "$REPO_URL_FILE" ]; then
  echo "Error: Repository URL file not found: $REPO_URL_FILE"
  exit 1
fi

# Initialize a variable to keep track of SHA mismatches
sha_mismatch_found=0

# Function to check SHAs and print results
extract_names_with_sbom_extension() {
 local tag="$1"
 local hash="$2"

 if [ -z "$hash" ]; then
    echo "Error: The $tag image is referenced using floating tags. Exiting..."
    exit 1
 fi

 json_response=$(curl -s https://quay.io/api/v1/repository/modh/$tag/tag/ | jq -r '.tags | .[:3] | map(select(.name | endswith(".att"))) | .[].name')
 local names_part=$(echo "$json_response" | sed 's/^sha256-\(.*\)\.att$/\1/')
 echo "Processing tag: $tag"
 echo "Expected SHA: $hash"
 echo "Found SHA in tags: $names_part"

 if [ "$hash" = "$names_part" ]; then
     # Print in green if equal
     echo -e "\e[32m$hash\e[0m matches \e[32m$names_part\e[0m"
 else
     # Print in red if not equal
     echo -e "\e[31m$hash\e[0m does not match \e[31m$names_part\e[0m"
     sha_mismatch_found=1
 fi
}

# Read repository URLs and file paths from the file, one per line
while IFS=';' read -r REPO_URL FILE_PATH
do
    echo "Processing repository: $REPO_URL"

    # Clone the repository into the 'cloned_repo' directory
    git clone --depth 1 -b rhoai-2.9 "$REPO_URL"
    if [ $? -ne 0 ]; then
      echo "Error: Failed to clone branch 'rhoai-2.9' from '$REPO_URL'"
      exit 1
    else
      echo "Successfully cloned the branch 'rhoai-2.9'."
    fi

    # Verify the specific file in the cloned repository
    FULL_FILE_PATH="$FILE_PATH"
    if [ ! -f "$FULL_FILE_PATH" ]; then
      echo "File not found: $FULL_FILE_PATH"
    else
      echo "File found: $FULL_FILE_PATH"
      # Read each line in the file and check the SHA
      while IFS= read -r line; do
        local name=$(echo "$line" | cut -d'=' -f1)
        local hash=$(echo "$line" | awk -F 'sha256:' '{print $2}')
        extract_names_with_sbom_extension $name $hash
      done < "$FULL_FILE_PATH"
    fi

    # Remove the 'cloned_repo' directory to clean up after the operation
    rm -rf
done < "$REPO_URL_FILE"

# Check if any SHA mismatches were found
if [ "$sha_mismatch_found" -ne 0 ]; then
    echo "One or more SHA mismatches were found."
    exit 1
else
    echo "All SHA hashes match."
fi
