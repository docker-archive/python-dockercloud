# python-docker-cloud

Python library for Docker Cloud

## Installation

In order to install the Docker Cloud Python library, you can use pip install:

	pip install python-dockercloud

It will install a Python module called dockercloud which you can use to interface with the API.

## Authorization

The authentication can be configured in the following ways:

* Manually set it in your Python initialization code:

		import dockercloud
		dockercloud.user = "username"
		dockercloud.apikey = "apikey"

* Login with docker cli, and the library will read the configfile automatically:

		$ docker login

* Set the environment variables DOCKERCLOUD_USER and DOCKERCLOUD_APIKEY:

		export DOCKERCLOUD_USER=username
		export DOCKERCLOUD_APIKEY=apikey

## Errors

Errors in the HTTP API will be returned with status codes in the 4xx and 5xx ranges.

The Python library will detect this status codes and raise ApiError exceptions with the error message, which should be handled by the calling application accordingly.


## Quick examples

### Services

	>>> import dockercloud
	>>> dockercloud.Service.list()
	[<dockercloud.api.service.Service object at 0x10701ca90>, <dockercloud.api.service.Service 	object at 0x10701ca91>]
	>>> service = dockercloud.Service.fetch("fee900c6-97da-46b3-a21c-e2b50ed07015")
	<dockercloud.api.service.Service object at 0x106c45c10>
	>>> service.name
	"my-python-app"
	>>> service = dockercloud.Service.create(image="dockercloud/hello-world", name="my-new-	app", target_num_containers=2)
	>>> service.save()
	True
	>>> service.target_num_containers = 3
	>>> service.save()
	True
	>>> service.stop()
	True
	>>> service.start()
	True
	>>> service.delete()
	True

### Containers

	>>> import dockercloud
	>>> dockercloud.Container.list()
	[<dockercloud.api.container.Container object at 0x10701ca90>, <dockercloud.api.container.Container object at 0x10701ca91>]
	>>> container = dockercloud.Container.fetch("7d6696b7-fbaf-471d-8e6b-ce7052586c24")
	<dockercloud.api.container.Container object at 0x10701ca90>
	>>> container.public_dns = "my-web-app.example.com"
	>>> container.save()
	True
	>>> container.stop()
	True
	>>> container.start()
	True
	>>> container.logs()
	"2014-03-24 23:58:08,973 CRIT Supervisor running as root (no user in config 	file) [...]"
	>>> container.delete()
	True
