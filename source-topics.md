# Core CS

## DBMS

### Getting Started

- Introduction to SQL
- Why SQL Exists
- How Databases Work
- Database Systems
- Installation and Tools

### DBMS Foundations and Architecture

- File Systems vs Database Management Systems
- Data Abstraction, Schemas, Instances, and Data Independence
- DBMS Components and End-to-End Query Flow
- Database Users, Roles, and Deployment Architectures
- Data Models and Database Families

### Core Foundations

- Database & Table Basics
- SQL Basics and Commands
- Working with Databases in SQL
- SQL Data Types
- Creating and Managing Tables in SQL
- Primary Key
- Foreign Key
- Constraints in SQL
- NULL vs 0 vs Empty String
- DDL vs DML
- Query Lifecycle
- Indexing in SQL

### Conceptual Data Modeling

- Entities, Entity Sets, and Attributes
- Relationships and Structural Constraints
- Weak Entities and Enhanced ER Modeling
- ER/EER-to-Relational Mapping

### Database Design

- Database Design Fundamentals
- Importance, Raw Data and Pain
- Core Concepts (Overview)
- Mental Model (First Principle)
- Schema Design
- Entity and Attributes
- Relationships, Cardinality and Optionality
- Everything About Keys
- Normalisation and their Forms

### Relational Model and Formal Query Languages

- Formal Relational Model and Integrity Constraints
- Fundamental Relational Algebra
- Joins and Extended Relational Algebra
- Tuple and Domain Relational Calculus
- Views and Materialized Views
- Triggers, Stored Routines, and Database-Side Logic

### Functional Dependencies and Database Design

- Redundancy and Update Anomalies
- Functional Dependencies and Keys
- Armstrong’s Axioms, Attribute Closure, and Minimal Cover
- First, Second, Third, and Boyce-Codd Normal Forms
- Decomposition Quality and Normalization Algorithms
- Multivalued Dependencies, 4NF, Join Dependencies, and 5NF

### Querying Essentials

- Query Fundamentals
- SELECT AND FROM
- WHERE
- Comparison Operators
- Logical Operators
- Arithmetic Operators
- ORDER BY and LIMIT
- DISTINCT and AS (Aliases)
- Big Countries
- Profitable Customers in 2021
- Odd Non-Boring Movies
- Filtering Essentials
- IS NULL vs. IS NOT NULL, IN, and NOT IN
- BETWEEN and NOT BETWEEN
- LIKE and NOT LIKE
- Filter Records Excluding a Specific Pattern
- Find Records Excluding a Given Set of Values
- Find Salaries Outside the Expected Range
- Non-Referred Customers

### Aggregation and Analysis

- Data Summarization
- Fundamentals of GROUP BY
- Basic Aggregate Functions (MIN, MAX, SUM, AVG)
- COUNT Functions
- HAVING Clause (Basics, HAVING with COUNT)
- First Login Analysis
- Employee Work Time Summary
- Unique Subjects per Teacher
- User Follower Count
- CRM Automotive Sales Analysis
- Highest Order Placing Customer
- Frequent Actor-Director Duos
- Large Classes
- Email Duplicates

### Set Operations

- Merging Query Results
- UNION
- UNION ALL
- Difference Between UNION and UNION ALL
- Intersection
- Combine Active and Archived Users
- Merge Recent Orders from Multiple Sources
- Combine Sales Records Without Deduplication
- Reshape Products Data

### SQL Joins

- Joins Deep Dive
- RIGHT JOIN
- ON vs. WHERE
- LEFT JOIN
- INNER JOIN
- FULL OUTER JOIN
- CROSS JOIN
- IMPLICIT JOIN
- SELF JOIN
- NATURAL JOIN
- Employees and Their Departments
- Customer Orders Overview
- Employees With Confirmed Salary Records
- Generate All Possible User-Category Pairs
- Employees With or Without Salary Records
- Match Employees With Their Salaries
- Employees Earning More Than Their Manager
- Students Enrolled in Courses
- Sales Analysis
- Minimum Distance Between Points
- Suspended Accounts
- Find Team Size for Each Employee
- Average Experience by Project
- Warehouse Stock Manager
- Table Join Operation
- Inactive Customers
- Students Enrolled in Non-Existent Departments
- Low Bonus Employees
- Available Seat Streaks
- Visitors Without Transactions
- A & B Buyers Without C
- Product Selling Price Report
- Updated Bank Balances
- Most Frequent Travellers
- Suggested Pages

### Subqueries

- Everything about Subqueries
- Introduction to Subqueries (IN)
- EXISTS and NOT EXISTS
- Correlated Subqueries
- Contest Participation Rate
- High-Report Managers
- All-Product Buyers
- Highest Non-Repeating Number
- Find the First Device Logged In by Each Player
- Salespersons Without RED Orders
- Employees with the Highest Salary in Each Department
- Find the Most Recent Order for Each Product
- Find Transactions with Maximum Amount Per Day
- Incomplete Employee Records
- Find Quiet Students in All Exams
- Top Grade per Student
- Swap Consecutive Seats
- Safe Investment Countries
- Tennis Grand Slam Winners
- Football Team Scores
- Order Count per Customer
- Boolean Expression Evaluator
- Immediate First Orders Percentage
- Find All Employees Reporting to the Head of the Company
- Orphan Employees

### Data Modification and Schema Evolution

- Editing Data and Tables
- INSERT
- UPSERT
- UPDATE
- DELETE
- ALTER
- TRUNCATE
- DELETE vs. TRUNCATE vs. DROP
- System Settings
- Employee Salary

### Physical Storage, Indexing, and Hashing

- Storage Hierarchy, Pages, Records, and Buffers
- File Organization
- Index Classification and Design
- B-Trees and B+ Trees
- Static and Dynamic Hashing

### Data Storage, Keys, and Query Optimization

- Storage, Keys and Query Performance
- Where Rows Actually Live
- How a B+ Tree Is Built with Data
- Why the Wrong Primary Key Can Quietly Destroy You
- Index Strategy at Scale

### Query Processing and Optimization

- From SQL to an Executable Plan
- Algorithms for Selection, Projection, Sorting, and Aggregation
- Join Processing Algorithms
- Cost-Based Query Optimization

### Query Performance

- Performance & Debugging
- Raw Data Setup and Stored Procedures
- Debugging Queries with EXPLAIN
- Query Performance
- Debugging Correctness

### Transactions and Access Control

- Permissions and Transactions Part-1
- Privileges and Roles
- GRANTS
- GRANT ALL and WITH GRANT OPTION
- ALTER USER
- REVOKE
- Permissions and Transactions Part-2
- Connection, Connection Pool and Commit
- Rollback
- Savepoint
- Internal Working of Transactions, Timeout and Deadlock

### Transactions and Concurrency Control

- Transaction Concepts, ACID, and States
- Schedules and Concurrency Anomalies
- Conflict and View Serializability
- Recoverable, Cascadeless, and Strict Schedules
- Lock-Based Protocols and Two-Phase Locking
- Deadlock Handling
- Timestamp Ordering, Optimistic Control, and MVCC
- SQL Isolation Levels

### Database Recovery and Durability

- Failures, Storage, and Recovery Goals
- Log-Based Recovery and Write-Ahead Logging
- Checkpoints and ARIES Intuition
- Shadow Paging, Backup, and Point-in-Time Recovery

### Integrity, Security, and Database Operations

- Declarative Integrity Beyond Keys
- Authorization, Views, and Auditing
- Database Security Threats and Protection
- Metadata, Statistics, Maintenance, and Observability

### Distributed Databases, NoSQL, and Analytical Systems

- Distributed Database Foundations
- Partitioning, Sharding, and Distributed IDs
- Replication, Consistency, and CAP/PACELC
- Distributed Transactions and Coordination
- NoSQL Data Models and SQL-vs-NoSQL Decisions
- OLTP, OLAP, Warehousing, and Columnar Storage

### Applied Learning and Preparation

- Schema-Design Capstone
- Storage and Query-Plan Lab
- Concurrency and Recovery Lab
- GATE and Semester Problem Track
- Interview Depth by Candidate Level
- Final Coverage and Source Alignment

## Operating Systems

### Module-1 (Operating System Basics and OS Introduction)

- Why Do We Need an Operating System?
- Operating System as a Manager
- What Happens When We Open an App?
- How Many Apps Run at the Same Time?
- OS and Protection

### Module-2 (Process Management in Operating System)

- Process Basics
- Program vs. Process vs. Thread
- Process States and Process Control Block
- Process Creation and Termination

### Module-3 (CPU Scheduling Algorithms in Operating System))

- Scheduling Queues and Schedulers
- Context Switching in OS
- CPU Scheduling Basics
- First Come First Serve (FCFS) Scheduling
- Shortest Job First (SJF) Scheduling
- Shortest Remaining Time First (SRTF) Scheduling
- Highest Response Ratio Next (HRRN) Scheduling
- Round Robin (RR) Scheduling
- Priority Scheduling
- Multilevel Queue (MLQ) Scheduling
- Multilevel Feedback Queue (MLFQ) Scheduling

### Module-4 (Kernel, OS Structures, and Advanced Scheduling)

- Kernel in OS
- Types of Operating Systems
- Types of Kernel Structures
- Why OS Schedulers Can't Implement Textbook Scheduling Algorithms
- Multicore Scheduling
- Load Balancing in OS
- CPU Affinity, Cache Locality, and NUMA

### Module-5 (Threads and Multithreading in Operating System)

- Threads in Operating System
- Threads vs Processes
- What Memory Is Shared Between Threads?
- User-Level Threads vs Kernel-Level Threads
- Multithreading Models in OS
- POSIX Threads
- Thread Pools
- Concurrency vs Parallelism
- Multiprogramming vs Multitasking vs Multiprocessing vs Multithreading
- Thread Safety, Reentrancy, and Race Condition

### Module-6 (Process Synchronization and Concurrency Control)

- Race Conditions in Operating Systems
- Critical Section Problem and Mutual Exclusion
- Dekker’s Algorithm
- Peterson’s Algorithm
- Bakery Algorithm
- Hardware Synchronization Principles
- Test-and-Set
- Compare-and-Swap
- Locks, Mutexes, and Types of Locks
- Semaphores
- Mutex vs Semaphores
- Producer-Consumer Problem
- Condition Variables in OS
- Monitoring in OS
- Readers-Writers Problem
- Sleeping Barber Problem
- Dining Philosophers Problem

### Module-7 (Deadlock, Starvation, and Concurrency Bugs)

- Deadlock in Operating Systems
- Conditions for Deadlock
- Resource Allocation Graph
- Wait-for Graph, Safe State, and Unsafe State
- Deadlock Prevention
- Deadlock Avoidance
- Banker’s Algorithm
- Deadlock Detection
- Deadlock Recovery
- Starvation vs Deadlock vs Livelock
- Priority Inversion
- Debugging Concurrency Bugs

### Module-8 (System Calls and Inter-Process Communication)

- System Calls in Operating System
- Types of System Calls
- Traps, Interrupts, and Exceptions
- fork, exec, wait, and exit
- Program Loading, Linking, and Dynamic Libraries
- Zombie and Orphan Processes
- Daemon Processes
- Inter-Process Communication (IPC)
- Pipes and Named Pipes
- Message Queues
- Shared Memory
- Memory-Mapped Files and mmap
- Signals in Operating Systems
- Sockets in Operating Systems
- IPC Decision Guide

### Module-9 (Memory Management in Operating System)

- Address Space in Operating System
- Stack, Heap, Code, and Data Segments
- Memory Allocation APIs: malloc, free, brk, and mmap
- Logical Address vs. Physical Address and MMU
- Swapping in Operating System
- Contiguous Memory Allocation
- Fixed vs. Variable Partitioning
- First Fit, Best Fit, Worst Fit, and Next Fit
- Internal vs. External Fragmentation
- Compaction and Buddy System

### Module-10 (Paging and Virtual Memory in Operating System)

- Paging in Operating System
- Paging vs Segmentation
- Pages, Frames, Page Tables, and PTEs
- PTE Numerical
- Multilevel Paging
- Inverted Page Table
- TLB in Operating System
- Effective Access Time with TLB
- Virtual Memory in Operating System
- Demand Paging
- Page Fault in Operating System
- Copy-on-Write and Lazy Allocation

### Module-11 (Page Replacement Algorithms and Thrashing)

- Page Replacement Algorithms
- FIFO Page Replacement
- Optimal Page Replacement
- LRU Page Replacement
- LFU and MFU Page Replacement
- Second-Chance and Clock Page Replacement
- Belady's Anomaly
- Thrashing and Working Set Model
- Frame Allocation Strategies

### Module-12 (File System in Operating System)

- File System in Operating System
- Files, Directories, and Paths
- File Descriptor in Operating System
- File Access Methods
- Inode, FCB, and File Metadata
- Hard Link vs Soft Link
- File Permissions and ACLs
- Directory Structure in Operating System
- File Allocation Methods
- Contiguous, Linked, and Indexed File Allocation
- Free Space Management
- Caching and Buffering in File Systems
- Journaling and Crash Consistency
- Backup, Recovery, and Network File Systems

## Computer Networks

### Module-1 (CN Foundations)

- Why Networks exists
- Network Types
- Internet and Backbone Networks
- Clients, Servers and Peers
- How data moves in packets

### Module-2 (Network Models)

- Why do we need layered Architecture
- OSI Model
- How Data Travels Up the OSI Model
- TCP/IP Model
- OSI vs TCP/IP
- Encapsulation and Decapsulation

### Module-3 (Physical and Data Link Layer)

- Physical Layer
- Transmission Media
- Twisted Pair Cable
- Fiber Optic Cable
- Coaxial Cable
- Full duplex vs Half duplex
- Network Device
- Mac address
- Error Detection
- Medium Access and CSMA
- Address Resolution Protocol
- Network Access Control
- Why do we need STP?
- Spanning Tree Protocol (STP)

### Module-4 (Network Topologies and VLANs)

- Network Topologies and VLANs Introduction
- Physical Topologies
- Hybrid Topology
- Logical Topologies
- Ethernet Switching
- Virtual LANs
- Switching vs Routing

### Module-5 (Network Layer: IP Addressing)

- Introduction to Network Layer
- IPv4 Introduction
- IPv4 Datagram
- IP Addressing Modes
- Private vs Public IP
- Classful Addressing
- Subnetting
- Common Interview Questions
- CIDR - Classless Addressing
- IPv6 Introduction
- IPv6 Datagram
- IPv6 over IPv4

### Module-6 (Network Layer: Routing)

- Router vs Forwarding
- Routing Tables Basics
- Static Routing
- Dynamic Routing
- Distance Vector Routing and RIP
- Routing Loop and Prevention
- Link State Routing and OSPF
- Hybrid Routing and EIGRP
- Border Gateway Protocol

### Module-7 (Transport Layer)

- Transport Layer Introduction
- Port and Sockets
- UDP
- TCP-I: Connection Setup and Numbering
- TCP-II: Reliability, Flow Control and Sliding Window
- TCP-III: Congestion Control and Connection Closing
- When to choose TCP/UDP

### Module-8 (Application Layer)

- Application Layer Introduction
- HTTP-Request Response Model
- HTTP methods and status codes
- HTTP Versions
- HTTP/3 and QUIC
- HTTPS and TLS
- Cookies, Sessions, and tokens
- Rest API’s
- WebSockets
- File Transfer Protocol
- Email Protocols

### Module-9 (NAT and Internet Edge Networking)

- NAT and Why do we need it?
- NAT Packet Flow
- Types of NAT
- SNAT, DNAT and Port Forwarding
- NAT Limitations
- DNS
- DNS Record Types
- DNS Security
- DNSSEC
- Dynamic Host Configuration Protocol (DHCP)

### Module-10 (Switching Techniques)

- What is Switching and Why?
- Fundamental Switching Techniques
- Circuit Switching
- Packet Switching
- Datagram Packet Switching
- Virtual Circuit Packet Switching
- MPLS
- Circuit Switching vs. Virtual Packet Switching
- Message Switching
- Why Packet Switching became backbone of Internet
- Comparisons between all 3
- FAQs - Switching

### Module-11 (Network Security)

- Why Network Security?
- CIA Triad
- AAA Framework
- Common Network Security Threats
- Firewalls and Types
- Firewall Type Comparison - L3, L4, and L7
- IDPS
- VPNs
- Zero Trust Architecture

### Module-12 (Cryptography and Secure Protocols)

- Introduction of Cryptography
- Security Goals of Cryptography
- Basic Cryptography Terms
- Symmetric Encryption
- Asymmetric Cryptography
- Diffie Hellman Key Exchange Method
- Hybrid Encryption
- Hash Functions
- MAC and HMAC
- Digital Signatures
- Certificate Authority and Chain of Trust
- Public Key Infrastructure
- Certificate Pinning
- TLS and SSL
- TLS Handshake and Forward Secrecy

### Module-13: (Wireless Networking)

- Wireless Networking Introduction
- Basics of Wireless Networking
- Wi-Fi Joining Flow
- WPA and WPA/WPA-2/WPA-3 Security Handshake
- IEEE 802.11 and Wi-Fi Generations
- Why Wi-Fi speed drops in Real Life
- How Wi-Fi avoids Collisions
- Wi-Fi Frame Types
- Wi-Fi Security
- Packet Flow: Opening a website over Wi-Fi

### Module-14 (Network Performance)

- Introduction to Network Performance
- Metrics Deep Dive
- Data Transfer and Bottlenecks, BDP
- Latency Sources, Delay, and TTFB
- Congestion, Bufferbloat, and Congestion Collapse Loop
- QoS, Traffic Shaping, and Policing
- Rate Limiting
- Fixed Window Counter - Rate Limiting Algo
- Sliding Window Log - Rate Limiting Algo
- Sliding Window Counter - Rate Limiting Algo
- Token Bucket - Rate Limiting Algo
- Leaky Bucket - Rate Limiting Algo
- Concurrency Limiter - Rate Limiting Algo
- Load Balancing Fundamentals
- L4 vs L7 Load Balancers
- Load Balancing Algorithms
- CDN Caching and Lifestyle

### Module-15 (Situation Based Explanations)

- What happens when you type google.com
- What happens when DNS fails?
- What happens when you connect to public Wi-Fi?
- How does a CDN serve an image/video?

## DBMS Interview prep

### Getting Started

#### Foundational Overview of SQL

- Introduction to SQL

#### Theoretical Breakdown of Databases

- Why SQL Exists
- How Databases Work
- Database Systems

#### SQL Setup Guide

- Installation and Tools

### DBMS Foundations and Architecture

- File Systems vs Database Management Systems
- Data Abstraction, Schemas, Instances, and Data Independence
- DBMS Components and End-to-End Query Flow
- Database Users, Roles, and Deployment Architectures
- Data Models and Database Families

### Core Foundations

#### Database Fundamentals

- Database & Table Basics

#### Breakdown of Table Basics

- SQL Basics and Commands
- Working with Databases in SQL
- SQL Data Types
- Creating and Managing Tables in SQL
- Primary Key
- Foreign Key
- Constraints in SQL
- NULL vs 0 vs Empty String
- DDL vs DML
- Query Lifecycle
- Indexing in SQL

### Conceptual Data Modeling

- Entities, Entity Sets, and Attributes
- Relationships and Structural Constraints
- Weak Entities and Enhanced ER Modeling
- ER/EER-to-Relational Mapping

### Database Design

#### Principles of Data Modeling & Database Design

- Database Design Fundamentals

#### Conceptual Breakdown of DB Design

- Importance, Raw Data and Pain
- Core Concepts (Overview)
- Mental Model (First Principle)
- Schema Design
- Entity and Attributes
- Relationships, Cardinality and Optionality
- Everything About Keys
- Normalisation and their Forms

### Relational Model and Formal Query Languages

- Formal Relational Model and Integrity Constraints
- Fundamental Relational Algebra
- Joins and Extended Relational Algebra
- Views and Materialized Views
- Triggers, Stored Routines, and Database-Side Logic

### Functional Dependencies and Database Design

- Redundancy and Update Anomalies
- Functional Dependencies and Keys
- First, Second, Third, and Boyce-Codd Normal Forms
- Decomposition Quality and Normalization Algorithms

### Querying Essentials

#### Data Retrieval Fundamentals

- Query Fundamentals

#### Data Selection Protocols

- SELECT AND FROM
- WHERE
- Comparison Operators
- Logical Operators
- Arithmetic Operators
- ORDER BY and LIMIT
- DISTINCT and AS (Aliases)

#### Problems Level 1 (Query Fundamentals)

- Big Countries
- Profitable Customers in 2021
- Odd Non-Boring Movies

#### Advanced Filtering Techniques

- Filtering Essentials

#### Conceptual Breakdown of Filters

- IS NULL vs. IS NOT NULL, IN, and NOT IN
- BETWEEN and NOT BETWEEN
- LIKE and NOT LIKE

#### Problem Level 1 (Filtering Essentials)

- Filter Records Excluding a Specific Pattern
- Find Records Excluding a Given Set of Values
- Find Salaries Outside the Expected Range
- Non-Referred Customers

### Aggregation and Analysis

#### Data Aggregation & Summarization

- Data Summarization

#### Conceptual Breakdown of Aggregates

- Fundamentals of GROUP BY
- Basic Aggregate Functions (MIN, MAX, SUM, AVG)
- COUNT Functions
- HAVING Clause (Basics, HAVING with COUNT)

#### Problems Level 1 (Data Summarization)

- First Login Analysis
- Employee Work Time Summary
- Unique Subjects per Teacher
- User Follower Count
- CRM Automotive Sales Analysis
- Highest Order Placing Customer

#### Problems Level 2 (Data Summarization)

- Frequent Actor-Director Duos
- Large Classes
- Email Duplicates

### Set Operations

#### Set Theory & Result Merging

- Merging Query Results

#### Conceptual Breakdown of Unions

- UNION
- UNION ALL
- Difference Between UNION and UNION ALL
- Intersection

#### Problems Level 1 (Merging Query Results)

- Combine Active and Archived Users
- Merge Recent Orders from Multiple Sources
- Combine Sales Records Without Deduplication
- Reshape Products Data

### SQL Joins

#### Join Fundamentals

- Joins Deep Dive

#### Conceptual breakdown of Joins

- RIGHT JOIN
- ON vs. WHERE
- LEFT JOIN
- INNER JOIN
- FULL OUTER JOIN
- CROSS JOIN
- IMPLICIT JOIN
- SELF JOIN
- NATURAL JOIN

#### Problems Level 1 (Joins Deep Dive)

- Employees and Their Departments
- Customer Orders Overview
- Employees With Confirmed Salary Records
- Generate All Possible User-Category Pairs
- Employees With or Without Salary Records
- Match Employees With Their Salaries
- Employees Earning More Than Their Manager
- Students Enrolled in Courses

#### Problems Level 2 (Joins Deep Dive)

- Sales Analysis
- Minimum Distance Between Points
- Suspended Accounts
- Find Team Size for Each Employee
- Average Experience by Project
- Warehouse Stock Manager

#### Problems Level 3 (Joins Deep Dive)

- Table Join Operation
- Inactive Customers
- Students Enrolled in Non-Existent Departments
- Low Bonus Employees
- Available Seat Streaks
- Visitors Without Transactions
- A & B Buyers Without C
- Product Selling Price Report
- Updated Bank Balances
- Most Frequent Travellers
- Suggested Pages

### Subqueries

#### Mastering Subqueries

- Everything about Subqueries

#### Conceptual Breakdown of Nested Logic

- Introduction to Subqueries (IN)
- EXISTS and NOT EXISTS
- Correlated Subqueries

#### Problems Level 1 (Everything about Subqueries)

- Contest Participation Rate
- High-Report Managers
- All-Product Buyers
- Highest Non-Repeating Number
- Find the First Device Logged In by Each Player
- Salespersons Without RED Orders

#### Problems Level 2 (Everything about Subqueries)

- Employees with the Highest Salary in Each Department
- Find the Most Recent Order for Each Product
- Find Transactions with Maximum Amount Per Day
- Incomplete Employee Records
- Find Quiet Students in All Exams
- Top Grade per Student

#### Problems Level 3 (Everything about Subqueries)

- Swap Consecutive Seats
- Safe Investment Countries
- Tennis Grand Slam Winners
- Football Team Scores
- Order Count per Customer
- Boolean Expression Evaluator
- Immediate First Orders Percentage
- Find All Employees Reporting to the Head of the Company
- Orphan Employees

### Data Modification and Schema Evolution

#### Data Manipulation

- Editing Data and Tables

#### Table Alteration Commands

- INSERT
- UPSERT
- UPDATE
- DELETE
- ALTER
- TRUNCATE
- DELETE vs. TRUNCATE vs. DROP

#### Problems Level 1 (Editing Data and Tables)

- System Settings
- Employee Salary

### Physical Storage, Indexing, and Hashing

- Storage Hierarchy, Pages, Records, and Buffers
- File Organization
- Index Classification and Design
- B-Trees and B+ Trees

### Data Storage, Keys, and Query Optimization

#### How Storage and Keys Impact Queries

- Storage, Keys and Query Performance

#### Breakdown of Storage, Keys, and Query Performance

- Where Rows Actually Live
- How a B+ Tree Is Built with Data
- Why the Wrong Primary Key Can Quietly Destroy You
- Index Strategy at Scale

### Query Processing and Optimization

- From SQL to an Executable Plan
- Algorithms for Selection, Projection, Sorting, and Aggregation
- Join Processing Algorithms
- Cost-Based Query Optimization

### Query Performance

#### Performance Engineering

- Performance & Debugging

#### Breakdown of Performance & Debugging

- Raw Data Setup and Stored Procedures
- Debugging Queries with EXPLAIN
- Query Performance
- Debugging Correctness

### Transactions and Access Control

#### Access Control Part 1

- Permissions and Transactions Part-1

#### Breakdown of Transactions and Access Part 1

- Privileges and Roles
- GRANTS
- GRANT ALL and WITH GRANT OPTION
- ALTER USER
- REVOKE

#### Access Control Part 2

- Permissions and Transactions Part-2

#### Breakdown of Transactions and Access Part 2

- Connection, Connection Pool and Commit
- Rollback
- Savepoint
- Internal Working of Transactions, Timeout and Deadlock

### Transactions and Concurrency Control

- Transaction Concepts, ACID, and States
- Schedules and Concurrency Anomalies
- Conflict and View Serializability
- Lock-Based Protocols and Two-Phase Locking
- Deadlock Handling
- Timestamp Ordering, Optimistic Control, and MVCC
- SQL Isolation Levels

### Database Recovery and Durability

- Failures, Storage, and Recovery Goals
- Log-Based Recovery and Write-Ahead Logging
- Checkpoints and ARIES Intuition
- Shadow Paging, Backup, and Point-in-Time Recovery

### Integrity, Security, and Database Operations

- Declarative Integrity Beyond Keys
- Authorization, Views, and Auditing
- Database Security Threats and Protection
- Metadata, Statistics, Maintenance, and Observability

### Distributed Databases, NoSQL, and Analytical Systems

- Distributed Database Foundations
- Partitioning, Sharding, and Distributed IDs
- Replication, Consistency, and CAP/PACELC
- Distributed Transactions and Coordination
- NoSQL Data Models and SQL-vs-NoSQL Decisions
- OLTP, OLAP, Warehousing, and Columnar Storage

### Applied Learning and Preparation

- Schema-Design Capstone
- Storage and Query-Plan Lab
- Concurrency and Recovery Lab
- Interview Depth by Candidate Level

## Operating Systems  - Interview Prep

### Module-1 (Operating System Basics and OS Introduction)

- Why Do We Need an Operating System?
- Operating System as a Manager
- What Happens When We Open an App?
- OS and Protection

### Module-2 (Process Management in Operating System)

- Process Basics
- Program vs. Process vs. Thread
- Process States and Process Control Block
- Process Creation and Termination

### Module-3 (CPU Scheduling Algorithms in Operating System))

- Scheduling Queues and Schedulers
- Context Switching in OS
- CPU Scheduling Basics
- First Come First Serve (FCFS) Scheduling
- Shortest Job First (SJF) Scheduling
- Shortest Remaining Time First (SRTF) Scheduling
- Round Robin (RR) Scheduling
- Priority Scheduling
- Multilevel Queue (MLQ) Scheduling
- Multilevel Feedback Queue (MLFQ) Scheduling

### Module-4 (Kernel, OS Structures, and Advanced Scheduling)

- Kernel in OS
- Why OS Schedulers Can't Implement Textbook Scheduling Algorithms
- Multicore Scheduling
- Load Balancing in OS
- CPU Affinity, Cache Locality, and NUMA

### Module-5 (Threads and Multithreading in Operating System)

- Threads in Operating System
- Threads vs Processes
- What Memory Is Shared Between Threads?
- User-Level Threads vs Kernel-Level Threads
- Thread Pools
- Concurrency vs Parallelism
- Multiprogramming vs Multitasking vs Multiprocessing vs Multithreading
- Thread Safety, Reentrancy, and Race Condition

### Module-6 (Process Synchronization and Concurrency Control)

- Race Conditions in Operating Systems
- Critical Section Problem and Mutual Exclusion
- Dekker’s Algorithm
- Peterson’s Algorithm
- Bakery Algorithm
- Test-and-Set
- Compare-and-Swap
- Locks, Mutexes, and Types of Locks
- Semaphores
- Mutex vs Semaphores
- Producer-Consumer Problem
- Condition Variables in OS
- Monitoring in OS
- Readers-Writers Problem
- Sleeping Barber Problem
- Dining Philosophers Problem

### Module-7 (Deadlock, Starvation, and Concurrency Bugs)

- Deadlock in Operating Systems
- Conditions for Deadlock
- Resource Allocation Graph
- Wait-for Graph, Safe State, and Unsafe State
- Deadlock Prevention
- Deadlock Avoidance
- Banker’s Algorithm
- Deadlock Detection
- Deadlock Recovery
- Starvation vs Deadlock vs Livelock
- Priority Inversion
- Debugging Concurrency Bugs

### Module-8 (System Calls and Inter-Process Communication)

- System Calls in Operating System
- Types of System Calls
- Traps, Interrupts, and Exceptions
- fork, exec, wait, and exit
- Zombie and Orphan Processes
- Daemon Processes
- Inter-Process Communication (IPC)
- Pipes and Named Pipes
- Message Queues
- Shared Memory
- Memory-Mapped Files and mmap
- Signals in Operating Systems
- Sockets in Operating Systems
- IPC Decision Guide

### Module-9 (Memory Management in Operating System)

- Address Space in Operating System
- Stack, Heap, Code, and Data Segments
- Memory Allocation APIs: malloc, free, brk, and mmap
- Logical Address vs. Physical Address and MMU
- Swapping in Operating System
- Contiguous Memory Allocation
- Internal vs. External Fragmentation
- Compaction and Buddy System

### Module-10 (Paging and Virtual Memory in Operating System)

- Paging in Operating System
- Paging vs Segmentation
- Pages, Frames, Page Tables, and PTEs
- Multilevel Paging
- TLB in Operating System
- Effective Access Time with TLB
- Virtual Memory in Operating System
- Demand Paging
- Page Fault in Operating System
- Copy-on-Write and Lazy Allocation

### Module-11 (Page Replacement Algorithms and Thrashing)

- Page Replacement Algorithms
- FIFO Page Replacement
- Optimal Page Replacement
- LRU Page Replacement
- LFU and MFU Page Replacement
- Second-Chance and Clock Page Replacement
- Belady's Anomaly
- Thrashing and Working Set Model

### Module-12 (File System in Operating System)

- File System in Operating System
- Files, Directories, and Paths
- File Descriptor in Operating System
- Inode, FCB, and File Metadata
- Hard Link vs Soft Link
- File Permissions and ACLs
- File Allocation Methods
- Caching and Buffering in File Systems
- Journaling and Crash Consistency

### Module-13 (Storage Management, Disk Scheduling, and I/O Systems)

- HDD vs SSD
- Disk Structure: Tracks, Sectors, Cylinders, Blocks, and Pages
- Disk Access Time
- Disk Scheduling Algorithms
- RAID in Operating System
- Device Drivers in Operating System
- Interrupts in Operating System
- DMA in Operating System
- Polling vs Interrupts and Blocking vs Non-Blocking I/O
- Event-Based I/O and Network I/O Path
- Booting, BIOS vs UEFI, and Bootloader

### Module-14 (OS Security, Virtualization, Containers, and Interview Revision)

- Users, Groups, Authentication, and Authorization
- Access Control Models: ACLs, Access Matrix, and Capabilities
- Privilege Separation, Sandboxing, and File System Encryption
- Common OS Security Risks
- Virtual Machines and Hypervisors
- Containers in Operating System
- Containers vs Virtual Machines
- Namespaces and cgroups
- OS Observability and Performance Debugging
- OS Concepts in Backend Systems and Databases
- Must-Know OS Interview and Exam Checklist

## Computer Networks  - Interview Prep

### Module-1 (CN Foundations)

- Network Types
- Internet and Backbone Networks
- Clients, Servers and Peers
- How data moves in packets

### Module-2 (Network Models)

- Why do we need layered Architecture
- OSI Model
- TCP/IP Model
- OSI vs TCP/IP
- Encapsulation and Decapsulation

### Module-3 (Physical and Data Link Layer)

- Physical Layer
- Full duplex vs Half duplex
- Network Device
- Mac address
- Error Detection
- Medium Access and CSMA
- Address Resolution Protocol

### Module-4 (Network Topologies and VLANs)

- Physical Topologies
- Ethernet Switching
- Virtual LANs
- Switching vs Routing

### Module-5 (Network Layer: IP Addressing)

- Introduction to Network Layer
- IPv4 Introduction
- IPv4 Datagram
- IP Addressing Modes
- Private vs Public IP
- Classful Addressing
- Subnetting
- Common Interview Questions
- CIDR - Classless Addressing
- IPv6 Introduction
- IPv6 Datagram
- IPv6 over IPv4

### Module-6 (Network Layer: Routing)

- Router vs Forwarding
- Routing Tables Basics
- Static Routing
- Dynamic Routing
- Distance Vector Routing and RIP
- Routing Loop and Prevention
- Link State Routing and OSPF
- Border Gateway Protocol

### Module-7 (Transport Layer)

- Transport Layer Introduction
- Port and Sockets
- UDP
- TCP-I: Connection Setup and Numbering
- TCP-II: Reliability, Flow Control and Sliding Window
- TCP-III: Congestion Control and Connection Closing
- When to choose TCP/UDP

### Module-8 (Application Layer)

- HTTP-Request Response Model
- HTTP methods and status codes
- HTTP Versions
- HTTP/3 and QUIC
- HTTPS and TLS
- Cookies, Sessions, and tokens
- Rest API’s
- WebSockets
- File Transfer Protocol

### Module-9 (NAT and Internet Edge Networking)

- NAT and Why do we need it?
- NAT Packet Flow
- Types of NAT
- SNAT, DNAT and Port Forwarding
- NAT Limitations
- DNS
- DNS Record Types
- DNS Security
- Dynamic Host Configuration Protocol (DHCP)

### Module-10 (Switching Techniques)

- What is Switching and Why?
- Circuit Switching
- Packet Switching
- Datagram Packet Switching
- Virtual Circuit Packet Switching

### Module-11 (Network Security)

- CIA Triad
- AAA Framework
- Common Network Security Threats
- Firewalls and Types
- Firewall Type Comparison - L3, L4, and L7
- VPNs

### Module-12 (Cryptography and Secure Protocols)

- Introduction of Cryptography
- Security Goals of Cryptography
- Basic Cryptography Terms
- Symmetric Encryption
- Asymmetric Cryptography
- Diffie Hellman Key Exchange Method
- Hybrid Encryption
- Hash Functions
- MAC and HMAC
- Digital Signatures
- Certificate Authority and Chain of Trust
- TLS and SSL
- TLS Handshake and Forward Secrecy

### Module-13: (Wireless Networking)

- Basics of Wireless Networking
- Wi-Fi Joining Flow
- Why Wi-Fi speed drops in Real Life
- How Wi-Fi avoids Collisions
- Wi-Fi Security

### Module-14 (Network Performance)

- Metrics Deep Dive
- Data Transfer and Bottlenecks, BDP
- Latency Sources, Delay, and TTFB
- Congestion, Bufferbloat, and Congestion Collapse Loop
- Rate Limiting
- Fixed Window Counter - Rate Limiting Algo
- Sliding Window Log - Rate Limiting Algo
- Sliding Window Counter - Rate Limiting Algo
- Token Bucket - Rate Limiting Algo
- Leaky Bucket - Rate Limiting Algo
- Concurrency Limiter - Rate Limiting Algo
- Load Balancing Fundamentals
- L4 vs L7 Load Balancers
- Load Balancing Algorithms
- CDN Caching and Lifestyle

### Module-15 (Situation Based Explanations)

- What happens when you type google.com
- What happens when DNS fails?
- What happens when you connect to public Wi-Fi?
- How does a CDN serve an image/video?

# System Design

## OOPS

### Introduction to OOPS

- Java Basics
- What is OOPS
- Classes and Objects
- Practice (Classes and Objects)
- Attributes and Methods
- Practice (Attributes and Methods)
- Constructors
- Practice (Constructors)

### Core Principles of OOPS

- Encapsulation
- Practice (Encapsulation)
- Access Modifiers
- Practice (Access Modifiers)
- Inheritance
- Practice (Inheritance)
- Polymorphism
- Practice (Polymorphism)

### Advance OOPS features

- Abstraction
- Practice (Abstraction)
- Interfaces
- Practice (Interfaces)
- Static Keyword
- Practice (Static Keyword)
- Inner classes
- Practice (Inner classes)

### Relationships and Object Behaviour

- Association, Aggregation, and Composition
- Practice (Composition)
- Object Cloning
- Practice (Object Cloning)

### Advance Programming in OOPS

- Exception Handling
- Generics
- File Handling

### OOP Design and Lifecycle Management

- Design Principles
- Object Lifecycle

## Low Level Design (LLD)

### Introduction to LLD

- Introduction to Low Level Design
- Software Design Principles

### Solid Principles

- Single Responsibility Principle (SRP)
- Open Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)

### UML

- Unified Modeling Language (UML)
- Class UML diagrams

### Creational Design Patterns

- Introduction to Design Patterns
- Singleton Design Pattern
- Factory Method
- Builder Pattern
- Abstract Factory
- Prototype Pattern

### Structural Design Patterns

- Adapter Pattern
- Decorator Pattern
- Facade Pattern
- Composite Pattern
- Proxy Pattern
- Bridge Pattern
- Flyweight Pattern

### Behavioural Design Patterns

- Iterator Pattern
- Observer Pattern
- Strategy Pattern
- Command Pattern
- Template Method
- State Pattern
- Chain of Responsibility
- Visitor Pattern
- Mediator Pattern
- Memento Pattern

### Multithreading and Concurrency

- Multithreading and Concurrency
- Creating and Managing Threads
- Thread Pools and Executors
- Thread Safety and Synchronization
- Locks and Synchronization Mechanism
- Deadlock and Prevention Techniques
- Producer Consumer Problem

### Dependency Injection

- Dependency Injection

### Exceptions and Error Handling

- Exception Handling (LLD)
- Building Resilient Systems

### Best practices in LLD

- All About API's
- Database Design and Integration
- How to approach a LLD Interview

### Interview Problems (Part-1)

- Parking Lot (Design)
- Parking Lot (Code)
- Logging Framework (Design)
- Logging Framework (Code)
- Traffic Signal System (Design)
- Traffic Signal System (Code)
- Vending Machine Design
- Vending Machine Code
- Task Management System Design
- Task Management System Code

### Interview Problems (Part-2)

- PubSub System Design
- PubSub System Code
- ATM Machine Design
- ATM Machine Code
- Hotel Management System Design
- Hotel Management System Code

### Interview Problems (Part-3)

- Elevator System Design
- Elevator System Code
- Digital Wallet Design
- Types of Locking Mechanism
- Digital Wallet Code
- Ride Booking App Design
- Ride Booking App Code
- Music Streaming Platform Design
- Streaming Protocols
- Music Streaming Platform Code

# Data Engineering

## SQL - Basic to Production Engineering

### Getting Started

#### Foundational Overview of SQL

- Introduction to SQL

#### Theoretical Breakdown of Databases

- Why SQL Exists
- How Databases Work
- Database Systems

#### SQL Setup Guide

- Installation and Tools

### Core Foundations

#### Database Fundamentals

- Database & Table Basics

#### Breakdown of Table Basics

- SQL Basics and Commands
- Working with Databases in SQL
- SQL Data Types
- Creating and Managing Tables in SQL
- Primary Key
- Foreign Key
- Constraints in SQL
- NULL vs 0 vs Empty String
- DDL vs DML
- Query Lifecycle
- Indexing in SQL

### Querying Essentials

#### Data Retrieval Fundamentals

- Query Fundamentals

#### Data Selection Protocols

- SELECT AND FROM
- WHERE
- Comparison Operators
- Logical Operators
- Arithmetic Operators
- ORDER BY and LIMIT
- DISTINCT and AS (Aliases)

#### Problems Level 1 (Query Fundamentals)

- Big Countries
- Profitable Customers in 2021
- Odd Non-Boring Movies

#### Advanced Filtering Techniques

- Filtering Essentials

#### Conceptual Breakdown of Filters

- IS NULL vs. IS NOT NULL, IN, and NOT IN
- BETWEEN and NOT BETWEEN
- LIKE and NOT LIKE

#### Problem Level 1 (Filtering Essentials)

- Filter Records Excluding a Specific Pattern
- Find Records Excluding a Given Set of Values
- Find Salaries Outside the Expected Range
- Non-Referred Customers

### Aggregation and Analysis

#### Data Aggregation & Summarization

- Data Summarization

#### Conceptual Breakdown of Aggregates

- Fundamentals of GROUP BY
- Basic Aggregate Functions (MIN, MAX, SUM, AVG)
- COUNT Functions
- HAVING Clause (Basics, HAVING with COUNT)

#### Problems Level 1 (Data Summarization)

- First Login Analysis
- Employee Work Time Summary
- Unique Subjects per Teacher
- User Follower Count
- CRM Automotive Sales Analysis
- Highest Order Placing Customer

#### Problems Level 2 (Data Summarization)

- Frequent Actor-Director Duos
- Large Classes
- Email Duplicates

### Functions (Math and Conditional)

#### Scalar & Conditional Functions

- Numeric and NULL Functions

#### Numeric and Null Logic

- ROUND() and ABS()
- GREATEST(), LEAST(), and IF NULL()
- NULL Handling in SQL: IS NULL, IS NOT NULL, IF NULL(), and COALESCE()

#### Problems Level 1 (Numeric and NULL Functions)

- Call Count Between Pairs

#### Logic & Conditions

- Case Conditional Logic

#### Boolean and Branching Logic

- CASE Basics
- CASE Practical Examples
- Advanced CASE Usage

#### Problems Level 1 (Case Conditional Logic)

- Valid Triangle Check
- Instant Food Delivery
- Special Bonus Calculation
- Node Classification
- Apples vs Oranges
- Query Quality Analysis

#### Text & Strings

- String Functions

#### String & Pattern Mechanics

- CONCAT() vs. CONCAT_WS()
- LOWER() / UPPER()
- TRIM() / LTRIM() / RTRIM()
- LENGTH() vs CHAR_LENGTH()
- LEFT() / RIGHT() / SUBSTRING()
- LOCATE() / INSTR()
- REPLACE()
- Pattern Matching with LIKE

#### Problems Level 1 (String Functions)

- Exceeding Tweet Length

### Data Modification and Schema Evolution

#### Data Manipulation

- Editing Data and Tables

#### Table Alteration Commands

- INSERT
- UPSERT
- UPDATE
- DELETE
- ALTER
- TRUNCATE
- DELETE vs. TRUNCATE vs. DROP

#### Problems Level 1 (Editing Data and Tables)

- System Settings
- Employee Salary

### Set Operations

#### Set Theory & Result Merging

- Merging Query Results

#### Conceptual Breakdown of Unions

- UNION
- UNION ALL
- Difference Between UNION and UNION ALL
- Intersection

#### Problems Level 1 (Merging Query Results)

- Combine Active and Archived Users
- Merge Recent Orders from Multiple Sources
- Combine Sales Records Without Deduplication
- Reshape Products Data

### SQL Joins

#### Join Fundamentals

- Joins Deep Dive

#### Conceptual breakdown of Joins

- RIGHT JOIN
- ON vs. WHERE
- LEFT JOIN
- INNER JOIN
- FULL OUTER JOIN
- CROSS JOIN
- IMPLICIT JOIN
- SELF JOIN
- NATURAL JOIN

#### Problems Level 1 (Joins Deep Dive)

- Employees and Their Departments
- Customer Orders Overview
- Employees With Confirmed Salary Records
- Generate All Possible User-Category Pairs
- Employees With or Without Salary Records
- Match Employees With Their Salaries
- Employees Earning More Than Their Manager
- Students Enrolled in Courses

#### Problems Level 2 (Joins Deep Dive)

- Sales Analysis
- Minimum Distance Between Points
- Suspended Accounts
- Find Team Size for Each Employee
- Average Experience by Project
- Warehouse Stock Manager

#### Problems Level 3 (Joins Deep Dive)

- Table Join Operation
- Inactive Customers
- Students Enrolled in Non-Existent Departments
- Low Bonus Employees
- Available Seat Streaks
- Visitors Without Transactions
- A & B Buyers Without C
- Product Selling Price Report
- Updated Bank Balances
- Most Frequent Travellers
- Suggested Pages

### Transactions and Access Control

#### Access Control Part 1

- Permissions and Transactions Part-1

#### Breakdown of Transactions and Access Part 1

- Privileges and Roles
- GRANTS
- GRANT ALL and WITH GRANT OPTION
- ALTER USER
- REVOKE

#### Access Control Part 2

- Permissions and Transactions Part-2

#### Breakdown of Transactions and Access Part 2

- Connection, Connection Pool and Commit
- Rollback
- Savepoint
- Internal Working of Transactions, Timeout and Deadlock

### Subqueries

#### Mastering Subqueries

- Everything about Subqueries

#### Conceptual Breakdown of Nested Logic

- Introduction to Subqueries (IN)
- EXISTS and NOT EXISTS
- Correlated Subqueries

#### Problems Level 1 (Everything about Subqueries)

- Contest Participation Rate
- High-Report Managers
- All-Product Buyers
- Highest Non-Repeating Number
- Find the First Device Logged In by Each Player
- Salespersons Without RED Orders

#### Problems Level 2 (Everything about Subqueries)

- Employees with the Highest Salary in Each Department
- Find the Most Recent Order for Each Product
- Find Transactions with Maximum Amount Per Day
- Incomplete Employee Records
- Find Quiet Students in All Exams
- Top Grade per Student

#### Problems Level 3 (Everything about Subqueries)

- Swap Consecutive Seats
- Safe Investment Countries
- Tennis Grand Slam Winners
- Football Team Scores
- Order Count per Customer
- Boolean Expression Evaluator
- Immediate First Orders Percentage
- Find All Employees Reporting to the Head of the Company
- Orphan Employees

### CTEs and Temp Structures

#### Working with CTEs

- CTEs and Temporary Tables

#### Conceptual Breakdown of CTEs

- WITH and AS (CTEs)
- Non-Recursive CTEs
- Recursive CTEs for Hierarchies

#### Problems Level 1 (CTEs and Temporary Tables)

- Most Frequently Ordered Product(s) for Each Customer
- Find Missing Subtasks for Each Task

### Dates and Time

#### Working with Dates

- Dates: Functions and Filtering

#### Conceptual Breakdown of Date and Time

- Date and Time Part Extraction Using YEAR(), MONTH(), DAY(), HOUR(), MINUTE(), and SECOND()
- Filtering with Date Ranges
- Finding First and Latest Events
- Calculating Date Differences (DATEDIFF, TIMESTAMPDIFF)
- Current Date and Time

#### Problem Level 1 (Dates Functions and Filtering)

- Latest 2020 Login
- Kid-Friendly Movies in Last Month
- Warmer Days
- Restaurant Payment Trends
- Inactive Sellers

### Window Functions

#### Mastering Window Functions

- Everything about Window Functions

#### Breakdown of SQL Window Functions

- Core Mental Model (OVER, PARTITION BY, ORDER BY)
- Ranking Functions
- Offset Functions
- Window Frames
- Value Window Functions
- Distribution Helpers
- Named Windows
- Real-Life Use Cases

#### Problem Level 1 (Window Functions)

- Follow-up Game Activity
- Track Continuous Periods of Task Failures and Successes
- Find the Largest Window Between User Visits
- Top 3 Salaries per Department
- Top Ratings in Feb 2020
- Find Continuous Ranges in Logs
- Most Experienced Employees in Each Project
- Most Recent Three Orders for Each Customer

### JSON

#### Working with JSON

- JSON in SQL

#### Breakdown of JSON in SQL

- Dummy Data Setup
- JSON Insertion + Data Loading
- JSON Read / Query Commands
- JSON Arrays and Search
- JSON Updates
- JSON Output Builders
- Performance and Indexing
- Upsert Power Features

### Database Design

#### Principles of Data Modeling & Database Design

- Database Design Fundamentals

#### Conceptual Breakdown of DB Design

- Importance, Raw Data and Pain
- Core Concepts (Overview)
- Mental Model (First Principle)
- Schema Design
- Entity and Attributes
- Relationships, Cardinality and Optionality
- Everything About Keys
- Normalisation and their Forms

### Query Performance

#### Performance Engineering

- Performance & Debugging

#### Breakdown of Performance & Debugging

- Raw Data Setup and Stored Procedures
- Debugging Queries with EXPLAIN
- Query Performance
- Debugging Correctness

### Data Storage, Keys, and Query Optimization

#### How Storage and Keys Impact Queries

- Storage, Keys and Query Performance

#### Breakdown of Storage, Keys, and Query Performance

- Where Rows Actually Live
- How a B+ Tree Is Built with Data
- Why the Wrong Primary Key Can Quietly Destroy You
- Index Strategy at Scale

### Database Scaling and Production Systems

#### Production Scaling Fundamentals

- Scaling And Production Operations

#### Breakdown of Scaling And Production Operations

- Scaling Reads
- Sharding
- Distributed IDs
- Zero-Downtime Schema Changes
- Partitioning & Data Lifecycle

### Interview Situational Questions (Easy)

- Introduction to Situation-Based Questions
- Situation-1
- Situation-2
- Situation-3
- Situation-4
- Situation-5

### Interview Situational Questions (Medium)

- Situation-6
- Situation-7
- Situation-8
- Situation-9
- Situation-10

### Interview Situational Questions (Hard)

- Situation-11
- Situation-12
- Situation-13
- Situation-14
- Situation-15

## SQL - 75

### Querying and Filtering

- Big Countries
- Profitable Customers in 2021
- Odd Non-Boring Movies
- Non-Referred Customers
- Exceeding Tweet Length

### Aggregation and Grouping

- First Login Analysis
- Employee Work Time Summary
- Unique Subjects per Teacher
- User Follower Count
- Highest Order Placing Customer
- Frequent Actor-Director Duos
- Large Classes
- Email Duplicates
- Highest Non-Repeating Number

### Conditional Logic and Calculations

- Valid Triangle Check
- Special Bonus Calculation
- Instant Food Delivery
- Query Quality Analysis
- Apples vs Oranges
- Contest Participation Rate
- Call Count Between Pairs
- Swap Consecutive Seats

### Joins and Aggregation

- Table Join Operation
- Sales Analysis
- Low Bonus Employees
- Average Experience by Project
- Warehouse Stock Manager
- Most Frequent Travellers
- Updated Bank Balances

### Self Joins and Relationship Queries

- Employees Earning More Than Their Manager
- High-Report Managers
- Minimum Distance Between Points
- Boolean Expression Evaluator
- Suggested Pages
- Suspended Accounts

### Subqueries and Missing Records

- Inactive Customers
- Students Enrolled in Non-Existent Departments
- Visitors Without Transactions
- Salespersons Without RED Orders
- Orphan Employees
- A & B Buyers Without C
- All-Product Buyers
- Inactive Sellers
- Find Quiet Students in All Exams

### Set Operations and Combined Results

- Reshape Products Data
- Incomplete Employee Records
- Tennis Grand Slam Winners
- Football Team Scores
- Safe Investment Countries
- Top Ratings in Feb 2020

### Date and Time Analysis

- Latest 2020 Login
- Kid-Friendly Movies in Last Month
- Warmer Days
- Product Selling Price Report
- Order Count per Customer
- Immediate First Orders Percentage

### Ranking and Top N Queries

- Employees with the Highest Salary in Each Department
- Top Grade per Student
- Most Experienced Employees in Each Project
- Find the First Device Logged In by Each Player
- Find the Most Recent Order for Each Product
- Find Transactions with Maximum Amount Per Day
- Most Recent Three Orders for Each Customer
- Most Frequently Ordered Product(s) for Each Customer
- Top 3 Salaries per Department

### Window Functions

- Find Team Size for Each Employee
- Follow-up Game Activity
- Restaurant Payment Trends
- Find the Largest Window Between User Visits

### Consecutive Sequences and Ranges

- Available Seat Streaks
- Find Continuous Ranges in Logs
- Track Continuous Periods of Task Failures and Successes

### CTEs and Hierarchies

- Node Classification
- Find All Employees Reporting to the Head of the Company
- Find Missing Subtasks for Each Task
