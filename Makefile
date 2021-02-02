IMAGE ?= enho/deeplabcut:2.1.10
image:
	docker build -t $(IMAGE) .

shell: image
	docker run --rm -it $(IMAGE) bash

push: image
	docker push $(IMAGE)
