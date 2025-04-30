# Getting Started!

## Inference input arguments
List of relevant arguments for inference.py to use potentials.

### General arguments

I/O:
* `length` Specify length, or length range, you want the outputs. e.g. 100 or 95-105
* `num_designs` Number of designs to make
* `sequence` input sequence to diffuse. The positions to be should be masked with `X`, e.g. `AHXXCLX`. Multiple chains can be specified by separating them with `/`, e.g. `AHXXCLX/AXXXCLX`.
* `contigs` pieces of input protein to keep.
  * (?) Investigate effect when no input sequence is provided (uncoditional generation).
* `input_json` json file with all the arguments for running an inference. Check [this example](../examples/args.json).
* `out` output directory and for files.
* `T` Number of timesteps to use. The bigger the protein, the higher the number. Default 25.
  
Diffusion-related:
* `sampling_temp`: Temperature to sample input sequence to as a fraction of `T` (0 to 1). If `sequence` is provided, the diffusion process will only sample the masked positions.
  * Partial diffusion mode (`sampling_temp` < 1) is used in the paper to promote further exploration of known active sequence subspaces for the multistate designs, check [this example](../examples/multistate_args.json).
    This mode requires an input `pdb` to be provided.
    Apparently, the `sampling_temp` reduce the number of timestep to sample the input as `T * sampling_temp`.
  * Default diffusion mode (`sampling_temp` = 1) allows only the diffusion of the user masked AA with `X`. The rest of the sequence is kept fixed throughout the diffusion process.

Potential-related:
* `potentials` comma separated list of potentials to use, must be paired with potenatial_scale e.g. aa_bias,solubility,charge.
* `potential_scale` comma seperated list of weights for each potential in same order as potentials (multiplying factor gradient).

### Potential specific arguments

New potentials can be defined in [utils/potentials.py](../utils/potentials.py)

#### aa_bias: Amino acid composition potential 
* `aa_weights_json` defines specific weights for individual amino acids. It is used to directly control how much bias is applied to each amino acid in the sequence.
  Weights can rate between -1 to 1. Where -1 is discouraged,  
  Check [this example](../examples/aa_weights.json).
    * Similarly, it can be specified through command line with parameters: 
      * `aa_spec` string of AA to which we want to add weights, e.g. ASL
        * `aa_weights` string of weights to be 
  > Note: Can we add weight to k-mers? In this way we could bias towards cleavage motifs.
* `frac_seq_to_weight` fraction of a sequence to add AA weight bias too (will be randomly sampled)
* `add_weight_every_n` frequency to add aa weight. 
  * Is this flag mutually exclusive with `frac_seq_to_weight`?
* `aa_composition` aa composition specified by one letter aa code and fraction to represent in sequence eg. `H0.2,K0.5`. The sum of fractions should not exceed 1.


## Use case examples

WIP
