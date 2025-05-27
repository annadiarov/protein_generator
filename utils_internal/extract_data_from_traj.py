import sys, os, subprocess, pickle, time, json
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path = sys.path + [script_dir+'/../utils/'] + [script_dir+'/../model/']
from inpainting_util import write_pdb
import torch


def convert_seq_idx_to_aa(seq_idx: torch.Tensor) -> str:
    """
    Convert a sequence of indices to amino acid characters.
    """
    # To convert sequence indices to amino acid characters
    CONVERSION = 'ARNDCQEGHILKMFPSTWYVX-'
    # output string of amino acids
    seq = ''.join([CONVERSION[i] for i in seq_idx])
    return seq


def load_pt_traj_data(traj_pt_file: str) -> dict:
    """
    Load Protein Generator trajectory data from a .pt file, which contains a dictionary
    with the step as the key and a tuple of (xyz, seq_out, seq_diffused, pred_lddt) as the value.
    """
    return torch.load(traj_pt_file)


def write_fasta(seq: str, out_file: str, header: str = 'sequence') -> None:
    """
    Save a sequence to a FASTA file.
    """
    with open(out_file, 'w') as f:
        f.write(f'>{header}\n{seq}\n')


def extract_step_data_from_traj(
        traj_pt_file: dict,
        out_dir: str = '.',
        save_pdb: bool = True,
        save_fasta: bool = False,
) -> None:
    """
    Extract PDB files from trajectory data and save them in the specified output directory.
    Each PDB file is named with the design name and step number.
    """
    traj_data = load_pt_traj_data(traj_pt_file)
    design_name = '.'.join(split for split in os.path.basename(traj_pt_file).split('.')[:-1])  # Remove file extension
    out_fastas = []

    for step, data in traj_data.items():
        xyz, seq_out, seq_diffused, pred_lddt = data

        seq = torch.argmax(seq_out, dim=-1)
        aa_seq = convert_seq_idx_to_aa(seq)

        print(f'{design_name} {step}: {aa_seq} mean pLDDT {pred_lddt.mean().item():.2f}')

        # write pdb file
        if save_pdb:
            out_pdb = os.path.join(out_dir, f'{design_name}_{step}.pdb')
            write_pdb(out_pdb, seq, xyz, Bfacts=pred_lddt)

        # save fasta file
        if save_fasta:
            out_fasta = os.path.join(out_dir, f'{design_name}_{step}.fasta')
            out_fastas.append(out_fasta)
            write_fasta(aa_seq, out_fasta, header=f'{design_name}_{step}|meanpLDDT_{pred_lddt.mean().item():.2f}')

    # join fasta files into one
    if save_fasta and out_fastas:
        combined_fasta = os.path.join(out_dir, f'{design_name}.fasta')
        with open(combined_fasta, 'w') as combined_file:
            for fasta_file in out_fastas:
                with open(fasta_file, 'r') as f:
                    combined_file.write(f.read())
        # Remove individual fasta files if combined
        for fasta_file in out_fastas:
            os.remove(fasta_file)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Extract PDBs from trajectory data.")
    parser.add_argument('input_file', type=str, help='Path to the *pt file containing Protein Generator trajectory data.')
    parser.add_argument('-np', '--no-save-pdb', action='store_true', help='If set, do not save PDB files.')
    parser.add_argument('-nf', '--no-save-fasta', action='store_true', help='If set, do not save FASTA files.')
    args = parser.parse_args()

    out_dir = os.path.dirname(args.input_file)

    save_pdb = not args.no_save_pdb
    save_fasta = not args.no_save_fasta

    extract_step_data_from_traj(
        traj_pt_file=args.input_file,
        out_dir=out_dir,
        save_pdb=save_pdb,
        save_fasta=save_fasta
    )
