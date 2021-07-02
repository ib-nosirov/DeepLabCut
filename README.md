# Ibrohim's Fork of DeepLabCut v2.1.10

This fork sets up DeepLabCut v2.1.10 on TACC GPU systems and enables proper GUI
functionality on Mac OS Big Sur.

### DeepLabCut (with GUI) on MacOS

This installation uses PyPI to install DLC. This means that the supporting
Python packages, namely wxPython and Tensorflow v1.15, must be installed separately.

*Note:* [Homebrew](https://brew.sh) is assumed to be installed

1. `brew install python@3.7` to install a Python version that is compatible
with wxPython
<!-- This path is env specific. User will need to `brew info python@3.7` 
to determine path to the brew installed 3.7 -->
3. `/usr/local/opt/python@3.7/bin/python3 -m venv --system-site-packages
my_env` to create a virtual environment
<!-- lose the brackets, user wants something that they can directly cut and paste -->
4. `source my_env/bin/activate` to activate the virtual environment
5. `pip install tensorflow==1.15` to install Tensorflow
6. `git clone git@github.com:DeepLabCut/DeepLabCut.git` to clone the
DeepLabCut repo
7. `cd DeepLabCut`
8. `pip install -e .` to install DeepLabCut

<!-- It's good that you are documenting your process somewhere. However, these 
docs above have a high likelihood of becoming stale. They are also env specific.
If I were to write the above paragraph, I would simply provide a link to DeepLabCut's
installation instructions, which we can assume are always up to date. -->

### DeepLabCut on a TACC Machine

1. Open an SSH session on a TACC system that supports GPU computation (Maverick
2 or Frontera)
2. Clone this repository to your $WORK2 directory on a GPU-enabled TACC system.
```bash
cd $WORK2
git clone https://github.com/ib-nosirov/DeepLabCut.git dlc
cd dlc
```

*Note:* `$WORK2` on Maverick2 is meant for non I/O intensive workflows and as
of this writing, no such directory exists. Verify with a TACC expert before
proceeding.

3. `make image` to build the image using Docker
4. `make push` to push the built image

4. Change the `SIF` variable in the [Makefile](./Makefile) to a file path
(usually somewhere on $WORK2) where you would like to store the `*.sif` file.
By default, this is set to a path in the current working directory.
5. Launch an idev session and load the following modules:
    1. `module load cuda/10.0`
    2. `module load nccl cudnn tacc-singularity`
    3. My `module list`:
    ```bash
    Currently Loaded Modules:
      1) intel/19.1.1   4) autotools/1.2   7) pmix/3.1.4     10) TACC            13) cudnn/7.6.2            (g)
      2) impi/19.0.9    5) python3/3.7.0   8) hwloc/1.11.12  11) cuda/10.0  (g)  14) ooops/1.4
      3) git/2.24.1     6) cmake/3.16.1    9) xalt/2.10.2    12) nccl/2.4.7 (g)  15) tacc-singularity/3.6.3
    ```
6. In the idev session, pull the Docker image to a `*.sif` file:
```bash
idev
make sif
```
7. Alternatively, `make sing-shell` to run a container in Singularity and open an interactive bash session

<!-- Again, great that you are documenting your workflow. But these docs could also
just reference upstream (my fork). Unless there is an error in my docs, in which case
a pull request (PR) to upstream would be appropriate. -->

### Running Jupyter within the Singularity image on TACC GPU

1. Complete steps 1-6 in the idev workflow described [above](#pull-and-run-the-docker-image-via-idev-and-singularity-on-tacc-gpu)
2. Change the `ALLOCATION` in the [Makefile](./Makefile) from "SD2E-Community" to a valid allocation. You can view your allocations on the [TACC User Portal](https://portal.tacc.utexas.edu/projects-and-allocations).
3. From a login node, `make jupyter-mav2` or `make jupyter-frontera` to launch
a SLURM job running Jupyter in the `SIMG` container, on a Maverick2 GTX node or
Fronterat RTX node, respectively. This step is similar to running `sbatch
/share/doc/slurm/job.jupyter`.
4. Wait patiently until `tail -f ./jupyter.out` prints a URL to which you
should direct your web browser.
5. Make sure to `scancel` your job after you are done working.

<!-- Same as above: the workflow is fine, but it's already documented elsewhere.
When posible, we should always try to consolidate documentation. Doing otherwise
makes docs disparate, difficult to read, and difficult to find. 

This is all great logging, but you will find that it is mostly for your own
reference. My daily journal looks a lot like this, and I encourage you to also try a daily journal.
The GUI section, for instance, will point to your env-specific
python3.7 installation, but will only work for (guesstimating here) 50% of users
just due to env/OS variability. This is often the problem with YouTube tutorials,
which is why I try to avoid them.

For official docs, best practice is usually to:
1. Reference other (in this case upstream) docs when possible
2. If upstream docs have errors, submit PR
  1. Note that errors does not mean "it didn't work for me". Issues with a users specific env cannot and should not be covered in docs.
  2. The space of user envs is usually too large to practically address them in one ground truth document.
3. Write and maintain documentation for use cases that are not covered by other docs.

"If I don't have detailed recapitulated docs, what will I give to Rayna at 
the end of the summer?"
You will (ideally) give her an ETL pipeline or sbatch script where she can
`sbatch ibrohims_script.sh --video my_video` on Stampede2 and everything above "just works".
That's one line of code that falls into category 3 mentioned above.
-->

## Additional Docs

* [Singularity on TACC systems](https://containers-at-tacc.readthedocs.io/en/latest/singularity/01.singularity_basics.html)
* [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut)
* [TACC-ML base images](https://github.com/TACC/tacc-ml)
