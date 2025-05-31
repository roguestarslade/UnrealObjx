build-container:
	docker build --tag unrealobjx:latest .

build-container-verbose:
	docker build \
		--progress=plain \
		--no-cache \
		--pull \
		--tag unrealobjx:latest .

fetch:
	docker run --rm \
		-v $(CURDIR):/UnrealObjX \
		-v $(CURDIR)/ObjaverseDownloads:/export \
		unrealobjx fetch-internal PROMPT="$(PROMPT)"

fetch-internal:
	python fetch_prompt.py "$(PROMPT)"

build-index:
	docker run --rm \
		-v $(CURDIR):/UnrealObjX \
		unrealobjx build-index-internal

build-index-internal:
	python build_index.py
	
nuke-it-all:
	docker container stop $$(docker container ls -aq) 2>/dev/null || true
	docker system prune -a --volumes --force
	docker builder prune --all --force
