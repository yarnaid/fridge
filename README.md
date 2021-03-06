# Fridge

This is a sample project to demonstrate how to work with ReST API and related
tools.

In this guide, we will:

-   write open API specification with the editor
-   generate a mock server
-   write tests
-   implement real server and client

## Tools

We will use the default [OpenAPI](https://swagger.io/tools/swagger-editor/), editor. You can find it [here](https://editor.swagger.io). Also, there are a lot of extensions for text editors and IDEs like [this](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi). There are a lot of other options for the editor, e.g., run it locally in the docker or with NodeJS.

For the generation of the mock, we also can use the same editor, but for educational purposes, we will try [Postman](https://www.postman.com)

## Steps

### Generate a Mock Server with Minimal API

![Mock server](src/mock%20server.png)

### Generate a Mock Server with Postman

Create an API for Postman
![postman api](src/postman%20API.png)

Create a mock server with API
![postman mock](src/postman%20mock.png)

Run request to the mock server
![request mock server](src/mock%20get%20item.png)

## FastAPI Server

Just a simple initiated server already has a lot of features.
![fastapi init](src/fastapi%20init.png)

## Cache

With new headers, we don't send new requests to the server
![cache](src/cache.png)
