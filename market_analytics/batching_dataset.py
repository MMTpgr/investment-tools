import json

def batch_list(lst, batch_size):
    """Yield successive batches of size `batch_size` from `lst`."""
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

def batch_json_batches(input_path: str, output_path: str, batch_size: int = 100,file =None):
    """
    Read a JSON file containing a flat list of integers, split it into batches,
    and write out a new JSON file where each batch is an array of up to `batch_size` elements.

    :param input_path: Path to the source JSON file (flat list of integers).
    :param output_path: Path where the batched JSON will be written.
    :param batch_size: Number of items per batch (default: 100).
    """
    # Load the source list
    print(file)
    if file:
        data = file
    else:
        print('QQQQ')
        with open(input_path, 'r') as infile:
            data = json.load(infile)

    if not isinstance(data, list):
        raise ValueError(f"Expected input JSON to be a list, got {type(data)}")

    # Create batches
    batches = list(batch_list(data, batch_size))

    # Write out the batched data
    with open(output_path, 'w') as outfile:
        json.dump({"batches": batches}, outfile, indent=2)



batch_json_batches("symbol_ids.json","niflheim_production_energy_100.json",100)