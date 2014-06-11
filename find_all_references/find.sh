#!/bin/sh

if [ "$1" != "" ]; then
	pattern="$(pbpaste)"
	lines="$(echo "$pattern" | wc -l | sed -e "s/^ *//" -e "s/ *$//")"
	[ "$lines" != "1" ] && return
	output="$(gawk -v OFS=: -v str="$pattern" 'n = match($0, str) { print FILENAME, FNR, n, $0 }' "$1")"
	lines="$(echo "$output" | wc -l | sed -e "s/^ *//" -e "s/ *$//")"
	echo "Found $lines matching row for pattern '$pattern':"
	echo "$output"
fi
