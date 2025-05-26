import yaml
from typing import Union
from collections import Counter


def get_n_aa_composition(
        sequence: str,
        expected_composition: Union[dict, None] = None,
        print_output: bool = False
) -> dict:
    """
    Get the amino acid counts and their proportions in the sequence.
    If expected_composition is provided, it will also print the expected values.
    """
    sequence = sequence.upper()
    aa_counts = Counter(sequence)
    total = sum(aa_counts.values())  # Total number of amino acids in the sequence

    data_dict = {}

    print("AA\tn_aa\texpected_n_aa\tdiff_n_aa\tcomposition\texpected_composition\tdiff_composition")
    for aa in sorted(set(aa_counts.keys()).union(
            expected_composition.keys() if expected_composition else [])):
        n_aa = aa_counts.get(aa, 0)
        composition = n_aa / total if total > 0 else 0.0
        expected_n_aa = total * expected_composition.get(aa, 'N/A') if expected_composition else 'N/A'
        expected_composition_value = expected_composition.get(aa, 'N/A') if expected_composition else 'N/A'

        if isinstance(expected_n_aa, str):
            diff_n_aa = 'N/A'
            diff_composition = 'N/A'
        else:
            diff_n_aa = n_aa - expected_n_aa
            diff_composition = composition - expected_composition_value if isinstance(expected_composition_value, (int, float)) else 'N/A'

        if print_output:
            print(f"{aa}\t{n_aa:.0f}\t" \
                  f"{expected_n_aa if isinstance(expected_n_aa, str) else f'{expected_n_aa:.0f}'}\t" \
                  f"{diff_n_aa if isinstance(diff_n_aa, str) else f'{diff_n_aa:.0f}'}\t" \
                  f"{composition:.2f}\t" \
                  f"{expected_composition_value if isinstance(expected_composition_value, str) else f'{expected_composition_value:.2f}'}\t" \
                  f"{diff_composition if isinstance(diff_composition, str) else f'{diff_composition:.2f}'}")

        data_dict[aa] = {
            'n_aa': n_aa,
            'expected_n_aa': expected_n_aa,
            'diff_n_aa': diff_n_aa,
            'composition': composition,
            'expected_composition': expected_composition_value,
            'diff_composition': diff_composition
        }

    # print summary of different n_aa if expected composition is provided
    if print_output and expected_composition:
        total_diff_n_aa = sum(
            abs(data['diff_n_aa']) for data in data_dict.values() if isinstance(data['diff_n_aa'], (int, float)))

        print(f'Total different n_aa: {total_diff_n_aa:.0f} in sequence length {total:.0f}')

    return data_dict


if __name__ == "__main__":
    import argparse as ap

    parser = ap.ArgumentParser(description="Compute amino acid composition of a sequence.")
    parser.add_argument('sequence', type=str, help='Amino acid sequence to analyze.')
    parser.add_argument('-e', '--expected-composition',
                        default='../data/design_constraints.yaml',
                        type=str, help='Path to a YAML file with expected amino acid composition.' \
                                       'Only used to print expected values.')
    args = parser.parse_args()

    # Load expected amino acid composition from a YAML file if provided
    expected_composition = None
    if args.expected_composition:
        with open(args.expected_composition, 'r') as file:
            expected_composition = yaml.safe_load(file)
        try:
            expected_composition = expected_composition['aa_composition']
        except KeyError:
            print(f"Warning: 'aa_composition' key not found in {args.expected_composition}. "
                  "Expected composition will not be printed.")
            expected_composition = None

    # Compute and print the amino acid composition
    get_n_aa_composition(args.sequence, expected_composition, print_output=True)
