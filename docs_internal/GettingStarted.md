# Getting Started!

## Inference input arguments
List of relevant arguments for `inference.py` to use potentials to generate new
sequences without using `pdb` as input.

### General arguments

I/O:
* `contigs` pieces of input protein to keep according to `inference.py`. However,
  when **not** using `pdb` it **sets the lengths of the output sequences**.
  Length can be specified in the following ways:
  * Just a number to specify a concrete length, e.g. 100.
  * A range of numbers to specify a range of lengths to sample in each design,
    e.g. 30-40. Notice that at each denoising step, the length of the sequence
    will be fixed to an specific value in the range (it will not oscillate).
  * Multiple chains designs seem **not** to be supported without a PDB file using the
    nomenclature eg. `A10/B10` (raises AssertionError), `10,20` (samples a monomeric seq of max length 30).
    A workaround is using `sequence` (below) to specify masked chains, e.g. `XXXXX/XXXXXXX`.
  
  **/!\ WARNING**: the `length` argument does not seem to be used in the original code. Instead,
    `contigs` is used to set the length of the output sequence although it is in disagreement with
    `inference.py` docstring.
* `length` NOT USED IN CODE! but when provided in `ContigMap` in `sampler.py` (see code snippet below),
  it checks the compatibility between `contigs` and `length`. For instance, if `contigs` is 10-40 but 
  length is 10-15, only sequences of length 10-15 will be generated. Maybe this has more relevance
  when using `pdb` files as input (not our expected use-case).
  ```python
  class SEQDIFF_sampler:
    ...
    def feature_init(self):
      ...
      self.features['rm'] = ContigMap(self.features['parsed_pdb'], self.args['contigs'], 
                                    self.args['inpaint_seq'], self.args['inpaint_str'],
                                    self.args['length'])
  ```
* `num_designs` Number of designs to make
* `sequence` input sequence to diffuse. The positions to be should be masked with `X`, e.g. `AHXXCLX`. Multiple chains can be specified by separating them with `/`, e.g. `AHXXCLX/AXXXCLX`.
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
