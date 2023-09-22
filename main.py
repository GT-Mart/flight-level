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
    for parameter in parameters:
        job_name = parameter.lower()
        if job_name in config.JOBS:
            config.JOBS[job_name](config, job_name)
        else:
            print(f"{job_name} is not a valid job.")


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
if __name__ == "__main__":
    app()
