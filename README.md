# TIF Chunker

This project was created to divide a large orthomosiac available as a `tif` file
into multiple `tif` and/or `png` because we cannot directly load a large `tif file` into
memory but we can definitely work with smaller chunks.

# Required Files

To make this script work, you need to have 2 large tif files.

```
assets
|--- pre_flood.tif
|--- post_flood.tif
```

This is indicated in `main.py` as:

```python
pre = "assets/pre_flood.tif"
pre_out = "chunks/pre"
post = "assets/post_flood.tif"
post_out = "chunks/post"
```

`pre_out` is the output directory for `pre_flood.tif` files.

`post_out` is the output directory for `post_flood.tif` files.

# Code Structure

Following are the important piece of code that make chunking work

```
project
|- src
|  |--- tiff_chunker.py
|  |--- single_chunk_cleaner.py
|- main.py
```

## File: _tiff_chunker.py_

This is the main code which allows a tif to be tiled into multiple chunks.
This code can be used in 2 different ways:

_1. Normal Chunking_

Normal Chunking allows user to chunks the large tif file into multiple tiles simply by specifying the `tile_size`. Default is 1024. This method
is showcased in `main.py` as:

```python
c1 = TiffChunker(pre, pre_out, tile_size=TILE_SIZE)
c1.chunk_and_save_tif(window=w1, limit=limit)
c1.chunk_and_save_png(window=w1, limit=limit)
```

_2. Chunking with reference_

This method allows user to chunk tif file with reference to existing chunks. This allows user to chunk tif files that align perfectly with a `pre tif image`.

Example:

```python
c1 = TiffChunker(
    post,
    post_out,
    reference_path=f"{pre_out}/meta",
    tile_size=TILE_SIZE,
)
c1.chunk_and_save_tif(window=w2, limit=limit)
c1.chunk_and_save_png(window=w2, limit=limit)
```

Here, it expect a reference path which contains all the tif files that should be used as a reference to tile a large tif file.

## File: _single_chunks_cleaner.py_

This is the code which allows user to clean up any `pre_flood` tiles that do not have a matching entry for `post_flood`.

Usage:

```python
pre_out = "chunks/pre"
post_out = "chunks/post"
SingleChunkCleaner(pre_out, post_out).clean()
```

`pre_out` is the output directory for `pre_flood.tif` files.

`post_out` is the output directory for `post_flood.tif` files.

## File: _main.py_

This is where all the modules are connected together to make it work and it serves as an example to use the library.
