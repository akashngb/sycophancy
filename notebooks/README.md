# notebooks/

For exploratory analysis and plots. Keep the committed notebook short
and clean. If you want scratch work, add a `scratch_<name>.ipynb` to
this folder and gitignore it locally.

To run a notebook with the project environment:

```bash
uv run --extra dev jupyter notebook
# or register a kernel and open from VS Code / JupyterLab
uv run python -m ipykernel install --user --name syco --display-name "syco"
```

`00_quickstart.ipynb` loads the seed data, runs a tiny eval against the
fake backend, and prints metrics. It is the fastest way to see what the
harness does without downloading a model.
