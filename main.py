# -*- coding: utf-8 -*-
""" Basic implementation of command line tool that receives a list of unnamed arguments """

from typing import List
import typer

import config

# Instantiate the typer library
app = typer.Typer()


# define the function for the command line
@app.command()
def main(parameters: List[str]):
    job_name = parameters[0].lower()
    if job_name in config.JOBS:
        if len(parameters) > 1:
            config.JOBS[job_name](config, parameters)
        else:
            config.JOBS[job_name](config, job_name)


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
if __name__ == "__main__":
    app()
