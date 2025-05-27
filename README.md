# Distributed Systems Project - Socket Programming with RabbitMQ Logging

---
[Project Documentation](https://docs.google.com/document/d/1aezhWNhdD68XyykyIK8wOjnd12sbzsiM-eB3KcV-ed8/edit?usp=sharing)

This project is a client-server application where users can request employee information such as salary and leave details. It uses TCP sockets for communication between the client and server.

The server can handle multiple clients simultaneously, processes their requests, and retrieves employee data from a lightweight database (TinyDB). To keep track of all requests, the server logs each one asynchronously using RabbitMQ message queues.

The server is also packaged in a Docker container to make it easy to run on any system.
