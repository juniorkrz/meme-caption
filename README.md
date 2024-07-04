# Meme Caption Generator API

> Add text captions (top and bottom) to images using an API.

Blog post: [Caption Memes in Python](http://blog.lipsumarium.com/caption-memes-in-python/)

## Why an API?

I modified this project into an API via Docker to be consumed by my [StickerBot](https://github.com/juniorkrz/stickerbot).

## Installation

1. Clone this repository.
2. Navigate into the repo directory: `cd meme-caption`.
3. Build the Docker image: `docker build -t meme-caption .`
4. Run the Docker container:
   ```bash
   docker run -d --name meme-caption -p 8000:8000 meme-caption
   ```

   This will start an API at `http://localhost:8000`.

## Usage

- Visit `http://localhost:8000/docs` to interact with the API using Swagger UI.
- Use `http://localhost:8000/addCaption` to access the API endpoint.

### Example

```curl
curl -X POST "http://localhost:8000/addCaption" \
-H "Content-Type: multipart/form-data" \
-F "topText=TOP_TEXT_HERE" \
-F "bottomText=BOTTOM_TEXT_HERE" \
-F "file=@/caminho/para/sua/imagem.jpg"
```

![Example Result](http://blog.lipsumarium.com/assets/img/posts/2017-07-22-caption-memes-in-python/out.jpg)