import json

def convert_mapbox_to_feature_collection(input_file, output_file):
    """
    Reads a JSON file containing a list of Mapbox MatchedStepData objects
    and converts it into a single GeoJSON FeatureCollection file.
    """
    try:
        # Read the list of matched steps from the input file
        with open(input_file, 'r') as f:
            matched_steps = json.load(f)

        if not isinstance(matched_steps, list):
            print("Error: Input file is not a list of matched steps.")
            return

        # This will hold all the individual line features
        features = []

        # Loop through each step from your Mapbox output
        for i, step in enumerate(matched_steps):
            # The geometry is already in the correct format
            geometry = step.get("geometry")
            if not geometry:
                continue

            # Create a new GeoJSON Feature object for this step
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    # Add other data here to inspect it in geojson.io
                    "step_index": i,
                    "roadNames": step.get("roadNames", []),
                    "distanceMiles": step.get("distanceMiles", 0)
                }
            }
            features.append(feature)

        # Wrap all the features in a single FeatureCollection
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        # Write the new GeoJSON data to the output file
        with open(output_file, 'w') as f:
            json.dump(feature_collection, f, indent=2)

        print(f"Successfully converted {input_file} to {output_file}")
        print(f"You can now drag and drop '{output_file}' into geojson.io or mapshaper.org")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the conversion ---
if __name__ == "__main__":
    input_filename = "test-fallback2-combined.json"
    output_filename = "test-fallback2-combinedFINAL2.json"
    convert_mapbox_to_feature_collection(input_filename, output_filename)