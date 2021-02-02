image:
	docker build -t enho/deeplabcut .

shell: image
	docker run --rm -it enho/deeplabcut:latest bash
