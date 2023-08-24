#!/bin/bash

# Define the URLs
remote_url="https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json"
local_file="$(git rev-parse --show-toplevel)/schema.json"
commit_message="chore: update jsonresume schema"

# Function to check if the remote file is different from the local file
is_different() {
	remote_md5=$(curl -sSL "$remote_url" | md5sum | cut -d ' ' -f 1)
	local_md5=$(md5sum "$local_file" | cut -d ' ' -f 1)

	if [ "$remote_md5" != "$local_md5" ]; then
		return 0
	else
		return 1
	fi
}

# Main script
if is_different; then
	echo "Downloading updated schema..."
	curl -sSL -o "$local_file" "$remote_url"

	echo "Committing changes..."
	git add "$local_file"
	git commit -m "$commit_message"

	echo "Changes committed."
else
	echo "No changes in the schema. Nothing to do."
fi
