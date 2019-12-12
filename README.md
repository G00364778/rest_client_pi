# rest_client_pi

## REST API client for a Raspberry PI SensorHub HAT.

This project works in conjunction with [another project](https://github.com/G00364778/rest_api_server_python_flask).

The fist project provides a REST API server that allows the rest_client_pi application to publish the sensor data collected to a cloud based server.

The project runs on a [Raspberry PI](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) fitted with a [Sensor board](https://wiki.52pi.com/index.php/DockerPi_Sensor_Hub_Development_Board_SKU:_EP-0106).

<img src="https://wiki.52pi.com/images/3/36/Sensorhub2.jpg" alt="DockerPi Sensor Hub" width="100">

# Sample Graph

![Raspberry Pi Graph](/img/pi_graph.jpg)

The Graph is generated by the Server API from data pushed to the cloud by the pi client application.