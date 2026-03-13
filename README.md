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

## Day 3 – DynamoDB Integration

Integrated DynamoDB to persist incoming orders.
The order-handler Lambda now generates a unique orderId and stores orders in the DynamoDB table.
Architecture:
Client → API Gateway → Lambda → DynamoDB

Day 4 introduces AWS Step Functions to orchestrate the order processing workflow.

The order-handler Lambda now triggers the Step Functions state machine after storing the order in DynamoDB. The workflow currently includes validation and status update states.
Architecture now includes API Gateway → Lambda → Step Functions.

## Day 5 – Inventory & Payment Processing

Added two new Lambda functions: **inventory-check** and **payment-processor** to simulate real order processing steps.  
Connected these Lambdas to the **Step Functions workflow** so orders now go through inventory verification and payment processing.  
The payment Lambda randomly succeeds or fails to simulate real-world payment scenarios.  
Configured **retry logic in Step Functions** so payment failures are automatically retried before failing the workflow.  
The system now follows a microservice-style architecture with orchestrated order processing.

Day 6 – EventBridge Notifications

Implemented event-driven architecture using Amazon EventBridge.
Step Functions now publishes an OrderCompleted event after payment processing.
Created a notification-service Lambda that listens for this event.
Configured an EventBridge rule to trigger the notification Lambda automatically.
Tested the full pipeline from workflow execution to event-triggered notificat

Day 7 introduces asynchronous processing using Amazon SQS.

The payment step was decoupled from the Step Functions workflow and moved to a worker-based architecture.
Step Functions now sends payment jobs to an SQS queue.
A payment-worker Lambda consumes messages from the queue and processes payments.
This improves system scalability, reliability, and fault tolerance.

Day 8 – Dead Letter Queue (DLQ)
Implemented a Dead Letter Queue to handle failed payment jobs.
Configured the main SQS queue with a redrive policy to move messages after 3 failed processing attempts.
Updated the payment worker Lambda to simulate failures for testing.
Verified that failed messages are safely routed to the DLQ instead of being lost.

Day 9 – Idempotent Order Processing

Implemented idempotent payment processing to prevent duplicate order charges caused by SQS’s at-least-once delivery model.
Added a DynamoDB payment-idempotency table to track processed orderId values.
The payment-worker Lambda now checks DynamoDB before executing payment logic.
If the orderId already exists, the worker skips processing to avoid duplicates.
This improves system reliability and ensures safe retry handling in distributed systems.

Day 10 – Observability and Structured Logging

Implemented structured JSON logging across all Lambda services to improve system observability.  
Added correlation IDs to track each order request across the entire distributed workflow.  
Logs from order-handler, inventory-check, payment-worker, and notification services can now be traced using a single correlation ID.  
Used CloudWatch Logs Insights to query and visualize request flow across multiple services.  
This enables easier debugging and monitoring of the serverless order processing pipeline.

Day 11 focused on monitoring and alerting using CloudWatch.

CloudWatch alarms were created to monitor Lambda errors, DLQ messages, and Step Functions failures.
This allows automatic detection of system issues such as payment failures.
The system can now alert engineers when processing problems occur.
This improves reliability and operational observability of the distributed workflow.
