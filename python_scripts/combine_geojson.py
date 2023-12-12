import json
import sys
import logging

def load_json(filename):
    """
    Load JSON data from a file.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        sys.exit(1)

def filter_and_modify_moonboard(data):
    """
    Filter out non-commercial entries and add 'board' field for moonboard data.
    """
    return [{'Name': loc['Name'], 'Latitude': loc['Latitude'], 'Longitude': loc['Longitude'], 'board': 'moon'} for loc in data if loc['IsCommercial']]

def prepare_tensionboard(data):
    """
    Prepare tensionboard data.
    """
    return [{'name': loc['name'], 'Latitude': loc['latitude'], 'Longitude': loc['longitude'], 'board': loc['board']} for loc in data]

def convert_to_geojson(data):
    """
    Convert data to GeoJSON format.
    """
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    for loc in data:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [loc['Longitude'], loc['Latitude']]
            },
            'properties': {
                'name': loc.get('Name', loc.get('name')),
                'board': loc['board']
            }
        }
        geojson['features'].append(feature)
    
    return geojson

def main(moonboard_file, tensionboard_file):
    logging.basicConfig(level=logging.INFO)

    # Load the datasets
    logging.info("Loading moonboard data.")
    moonboard_data = load_json(moonboard_file)

    logging.info("Loading tensionboard data.")
    tensionboard_data = load_json(tensionboard_file)

    # Process the datasets
    logging.info("Processing moonboard data.")
    moonboard_data = filter_and_modify_moonboard(moonboard_data)

    logging.info("Processing tensionboard data.")
    tensionboard_data = prepare_tensionboard(tensionboard_data)

    # Combine datasets
    combined_data = moonboard_data + tensionboard_data
    logging.info("Combining datasets.")

    # Convert to GeoJSON
    geojson = convert_to_geojson(combined_data)
    logging.info("Converting to GeoJSON format.")

    # Save to file
    output_file = 'combined_geojson.json'
    with open(output_file, 'w') as file:
        json.dump(geojson, file, indent=4)
    logging.info(f"GeoJSON saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python combine_geojson.py moonboard_file.json tensionboard_file.json")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
