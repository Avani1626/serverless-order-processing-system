# Serverless Order Processing System with AI CloudOps

## Project Overview

This project is a production-style serverless backend system that processes e-commerce orders using AWS cloud services. The system automatically receives customer orders, stores them in a database, processes inventory and payment workflows, and sends notifications upon completion.

The goal of this project is to understand how real-world cloud systems are designed using event-driven architecture, serverless services, and infrastructure automation.

---

## System Workflow

1. A customer places an order through an API endpoint.
2. API Gateway receives the request and triggers a Lambda function.
3. The Order Lambda validates the request and stores the order in DynamoDB.
4. A Step Functions workflow manages the order processing steps.
5. Inventory Lambda checks whether the item is available.
6. Payment Lambda processes the payment for the order.
7. If processing is asynchronous, messages may pass through an SQS queue.
8. After successful processing, an event is published to EventBridge.
9. Notification Lambda sends confirmation to the customer.
10. Failed messages are sent to a Dead Letter Queue for investigation.

---

## AWS Services Used

* API Gateway – Entry point for order requests
* AWS Lambda – Serverless compute for business logic
* DynamoDB – NoSQL database to store orders
* Step Functions – Workflow orchestration
* Amazon SQS – Queue for asynchronous processing
* Dead Letter Queue – Handles failed jobs
* EventBridge – Event routing and notifications
* CloudWatch – Monitoring and logs
* X-Ray – Distributed tracing

---

## Project Architecture

The system follows a serverless and event-driven architecture where each service performs a single responsibility. This design improves scalability, reliability, and fault tolerance.

Architecture diagram will be added in the `/architecture` folder.

---

## Project Structure

```
serverless-order-processing-system
│
├── architecture        # System architecture diagrams
├── lambdas             # Lambda function source code
│   ├── order-handler
│   ├── inventory-check
│   ├── payment-processor
│   └── notification
│
├── terraform           # Infrastructure as Code configuration
├── docs                # Documentation and notes
└── README.md
```

---

## Project Phases

This project is built in multiple phases:

**Phase 1 — Core Serverless System**

* API Gateway
* Lambda functions
* DynamoDB integration
* Step Functions workflow

**Phase 2 — Reliability Engineering**

* SQS queues
* Dead Letter Queues
* Idempotency
* Structured logging
* Monitoring and alarms

**Phase 3 — Infrastructure as Code**

* Terraform setup
* AWS resources provisioned using code
* Modular infrastructure

**Phase 4 — AI CloudOps Engine**

* Terraform configuration analysis
* IAM risk detection
* Log summarization
* Automated postmortem generation

---

## Learning Goals

This project helps understand:

* Serverless architecture design
* Event-driven systems
* Cloud reliability engineering
* Infrastructure automation
* Observability and monitoring
* AI-assisted cloud operations

---

## Status

Day 1 – Project setup and architecture planning completed.

## Day 2 – API Gateway & Lambda Integration

* Created the **order-handler AWS Lambda** function to process incoming order requests.
* Implemented a basic Lambda handler to log incoming events and return a JSON response.
* Deployed an **HTTP API using API Gateway** and integrated it with the Lambda function.
* Created the **POST /order endpoint** to trigger the Lambda function.
* Successfully tested the API using curl and verified execution through CloudWatch logs.

