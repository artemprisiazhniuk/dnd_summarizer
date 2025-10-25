#!/bin/bash

part_length_in_minutes=$1
if [ -z "$part_length_in_minutes" ]; then
    part_length_in_minutes=45
fi

part_length_threshold=$2
if [ -z "$part_length_threshold" ]; then
    part_length_threshold=5
fi

# Loop through all mp3 files in the data/recordings directory
for input_filename in ./data/recordings/*.mp3; do
    input_filename="${input_filename%.mp3}"

    # Get the duration of the mp3 file in seconds
    duration=$(ffmpeg -i "$input_filename.mp3" 2>&1 | grep "Duration" | awk '{print $2}' | tr -d , | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')
    duration=$(echo $duration | awk '{print int($1)}')

    echo "Duration: $duration seconds"

    # Define the length of each part in seconds (1 hour)
    part_length=$((60 * $part_length_in_minutes))


    # Calculate the number of parts
    num_parts=$((duration / part_length))
    # If the remaining duration is more than threshold, add an extra part
    if [ $((duration - num_parts * part_length)) -gt $((60 * $part_length_threshold))]; then
        num_parts=$((num_parts + 1))
    fi

    if [ $num_parts -gt 1 ]; then
        echo "Number of parts: $num_parts"
        echo "Total duration: $((num_parts * part_length)) seconds"

        # Split the mp3 file into 1-hour parts
        for i in $(seq 0 $num_parts); do
            start_time=$((i * part_length))
            ffmpeg -i "$input_filename.mp3" -ss $start_time -t $part_length -acodec copy "${input_filename}_part_$((i + 1)).mp3"
        done

        # Remove the original mp3 file
        rm "$input_filename.mp3"
    fi
done