PYTHON ?= python3
IMAGE ?= enho/deeplabcut:2.1.10
ALLOCATION ?= SD2E-Community
SIF ?= ./deeplabcut_2_1_10.sif

# ------------------------------- Sanity checks -------------------------------

PROGRAMS := git docker $(PYTHON) singularity tox
.PHONY: $(PROGRAMS)
.SILENT: $(PROGRAMS)

docker:
	docker info 1> /dev/null 2> /dev/null && \
	if [ ! $$? -eq 0 ]; then \
		echo "\n[ERROR] Could not communicate with docker daemon. You may need to run with sudo.\n"; \
		exit 1; \
	fi
$(PYTHON) poetry singularity:
	$@ -h &> /dev/null; \
	if [ ! $$? -eq 0 ]; then \
		echo "[ERROR] $@ does not seem to be on your path. Please install $@"; \
		exit 1; \
	fi
tox:
	$@ -h &> /dev/null; \
	if [ ! $$? -eq 0 ]; then \
		echo "[ERROR] $@ does not seem to be on your path. Please pip install $@"; \
		exit 1; \
	fi
git:
	$@ -h &> /dev/null; \
	if [ ! $$? -eq 129 ]; then \
		echo "[ERROR] $@ does not seem to be on your path. Please install $@"; \
		exit 1; \
	fi

# ---------------------------- Docker/Singularity -----------------------------

image: | docker
	docker build -t $(IMAGE) .

shell: image | docker
	docker run --rm -it $(IMAGE) bash

push: image | docker
	docker push $(IMAGE)

$(SIF):
	singularity pull $(SIF) docker://$(IMAGE)

sing-dlc-demo: $(SIF) | singularity
	singularity exec --nv --home $$PWD \
		-B local_models:/opt/conda/lib/python3.7/site-packages/deeplabcut/pose_estimation_tensorflow/models/pretrained/ \
		$(SIF) bash -c "cd examples && python3 Demo_labeledexample_Openfield.py"

sing-shell: $(SIF) | singularity
	singularity shell --nv --home $$PWD \
		-B local_models:/opt/conda/lib/python3.7/site-packages/deeplabcut/pose_estimation_tensorflow/models/pretrained/ \
		$(SIF)

sif: $(SIF)

# ----------------------------- Jupyter ---------------------------------------

jupyter-mav2: $(SIF)
	sbatch -A $(ALLOCATION) scripts/mav2.jupytersing -i $(SIF)
	sleep 10
	tail -f jupyter.out

jupyter-frontera: $(SIF)
	sbatch -A $(ALLOCATION) scripts/frontera.jupytersing -i $(SIF)
	sleep 10
	tail -f jupyter.out
