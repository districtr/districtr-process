# Running districtr-process (with Docker)
## Why Docker?
Docker is a tool to standardize and automate the setup of a virtual enviroment. 
It allows every developer to test and work with the same enviroment, regardless of operating system, as long as they have Docker installed.
The districtr-process scripts only work on older versions of Python and require building custom libraries with `make`, which can be finnicky.
Using Docker allows us to skip the normal convoluted setup process and simply fetch a pre-built virtual enviroment to work in.

## Installing Docker
First, install Docker.
On macOS, you can install Docker from here: https://docs.docker.com/docker-for-mac/install/

For Linux, you can install Docker with an official script:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```
For Windows, follow the instructions here: https://docs.docker.com/docker-for-windows/install/

## Getting a Docker image
Then, to fetch the pre-built Docker image, run:
```bash
docker pull innovativeinventor/districtr-process:latest
```
Alternatively, you can build the dockerfile in `docker/Dockerfile` yourself.

## Running
Finally, to run `districtr-process`, you can run in the root of this git repo:
```bash
bash docker/run.sh [args] 
```
where `[args]` are whatever arguments you pass to districtr_process (e.g. `python -m districtr_process data/minnesota.yml` becomes `bash docker/run.sh data/data/minnesota.yml`).

This is equivalent to running:
```
docker run -it --rm -v $(pwd):/districtr-process innovativeinventor/districtr-process python3 -m districtr_process [args]
```
where `$(pwd)` is the path to your `districtr-process` repo. 

If you want to pass a mapbox API token to the Docker container, simply add it to `.env.list` file. For example, the contents of `.env.list` would look like:
```
MAPBOX_ACCESS_TOKEN=SOMESECRETKEY
```
where `SOMESECRETKEY` is your API token.

# Alternate, non-containerized setup

Run the following steps in terminal:

`$ git clone https://github.com/districtr/districtr-process.git`

`$ cd districtr-process`

`$ pip install pipenv`

`$ pipenv install`

`$ pipenv shell`

## Test the process command on Minnesota

`$ python -m districtr_process data/minnesota.yml`

You might get one warning about deprecated syntax, that's okay. 

# What you need to upload to Districtr

Now check the `output.json` file. Has it been populated with a Minnesota districting problem?
This is what you will add to the Districtr code itself, under `/assets/data/modules/Minnesota.json`. That file will contain an array of objects. `output.json` also contains an array with a single object inside 
You'll want to add the _object_ from `output.json` to the _array_ in Districtr. (In this case it's already in there. Add it in anyway as a duplicate, to show you know how to do it, and we just won't merge the pull request.)

You'll also need to edit `/assets/data/landing_pages.json` in order for the module to show up on the landing page. This file is also an array of objects. You'll have to find the object for the state, and locate the `modules` key, which has an array as its value. Find the correct geography object (in this case it's the one with `"name": "Statewide"` because we're using a statewide module) and add the `id` from `output.json` to the `ids` array. In this case the id is `minnesota`. (In this case it's already in there. Add it in anyway as a duplicate, to show you know how to do it, and we just won't merge the pull request.)

Make a pull request with these changes (with a branch named after your module id) and we'll review it. Then you can start creating new modules! 

# How to make the yml in the first place

The easiest way to do this is truly to copy another yml that's already in there and emulate the structure. There are a lot of examples to choose from. Make sure the column names align with what's in your shapefile, either by viewing them in QGIS or Python.

Formatting the YAML can be tricky, as the indentation needs to be correct. Make sure you're paying attention to this when creating yours.

# How do I actually upload to mapbox?

First run `$ python -m districtr_process data/{filename}.yml`. Then check the `output.json` to make sure it generated something. 

Then, you can run `$ python -m districtr_process data/{filename}.yml --upload` to actually upload it.

Notice in the output JSON there'll be a line that looks something like `"url": "mapbox://districtr.minnesota_precincts_points"`. That's how Districtr talks to the data you upload to load modules.



