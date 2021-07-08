# makemd

<p align="left">
  <a href="https://github.com/lawrennd/makemd"><img alt="GitHub Actions status" src="https://github.com/lawrennd/makemd/workflows/code-tests/badge.svg"></a>
</p>

A set of scripts for converting markdown files into talks.

The scripts rely on the generic preprocessor, `gpp`, https://github.com/logological/gpp. On Linux it can be installed using

```
apt-get install gpp
```

And on OSX it's available through brew.

```
brew install gpp
```
The code wraps gpp and creates make files for doing the conversion. 

* `maketalk`: for converting talk files from markdown to other formats.
* `makecv`: for converting CVs from markdown to other formats.
* `flags`: For extracting flags for pandoc's use from the configuration file `_config.yml`
* `mdfield`: for extracting a field from markdown header file.
* `dependencies`: for listing the dependencies in a given markdown file.
