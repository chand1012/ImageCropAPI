# ImageCrop API

A simple Microservice API that can crop, resize, and convert images.

# Usage

All of the endpoints can be accessed without an API key and can be used with either a GET or a POST request. If a GET request is used, then parameters must be added a a query string. If a POST request is used, then the parameters must be in the body of the request. All endpoints are accessed at https://image-crop-api.herokuapp.com/ . 

The documentation can be accessed by going to [this docs page](https://image-crop-api.herokuapp.com/docs). Each function and variable is pretty self explanatory. There is also a a "Try it out" feature available on the documentation in the top right of the endpoint dropdown.

Due to this microservice being hosted on [Heroku](https://heroku.com/), there may be times where a request takes twenty seconds. This is due to the dyno for the application being put to sleep when not in use. If you want this to change, either host is yourself (instructions below) or consider [Sponsoring Me](https://github.com/sponsors/chand1012/) so I can afford to have a paid dyno. 

# Hosting Yourself

The application can be hosted one of two ways, either by running inside a virtual environment, or via Docker. Currently the only way to host on a non-Linux Operating System is via Docker, as a few of the dependencies don't support anything but Linux. 

# Host via Docker.

## Pre Built Images

To get the latest image, just run `docker pull chand1012/image-crop-api:master`. Unlike most Docker Images, I opted to use the branch as the tag. `master` will always get you the latest version. After pulling the image, just run `docker run chand1012/image-crop-api:master`.

## Building the Docker Image.

If you are trying to run the application on a platform other than a 64-bit Linux system, such as for a Raspberry Pi or ARM server, you can build the Docker image with the following:

```Bash
# This is assuming you have Docker installed.
git clone https://github.com/chand1012/ImageCropAPI.git
cd ImageCropAPI
docker build . -t image-crop-api:master # This will take about 20 minutes
docker run image-crop-api:master 5000:5000
```

# Running from Source.

```Bash
sudo apt update
sudo apt install python3-pip python3-dev build-essential # this is for Ubuntu Linux. For Windows, you will just need Python >= 3.6.x # For other *nix OSes, the equivalent packages will be needed.
git clone https://github.com/chand1012/ImageCropAPI.git
cd ImageCropAPI
sudo pip3 install virtualenv 
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
deactivate
```

To run the application, you must use the virtual environment installed to the application. If you would rather run with the system Python installation, just skip the virtualenv steps and install like any other module.

To run the application:
```Bash
# assuming you are in the same directory as the application
source env/bin/activate
uvicorn main:app --reload
```

