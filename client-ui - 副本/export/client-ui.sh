#!/bin/sh
echo -ne '\033c\033]0;client-ui\a'
base_path="$(dirname "$(realpath "$0")")"
"$base_path/client-ui.arm64" "$@"
