# Distributed Transactions and Coordination

A local transaction can commit several changes inside one database together. If one action spans two independent databases, or a database and a message broker, there is no shared `COMMIT` by default. A crash between steps can leave one side changed and the other side unchanged. The design needs a way to decide, record, and recover the outcome.

## Two-phase commit

Two-phase commit, or **2PC**, uses a coordinator and participants:

1. **Prepare:** the coordinator asks each participant to make its local work durable and promise it can commit later. A participant votes yes or no.
2. **Decision:** if all vote yes, the coordinator records a commit decision and tells them to commit. Otherwise it tells them to roll back.

If a participant says no before the commit decision, the group can abort. If all have prepared but the coordinator disappears, prepared participants may have to wait for its durable decision. They can hold locks and storage while waiting. A coordinator must recover its decision log and finish the same decision after restart. A timeout alone is not proof that it is safe to roll back a prepared participant.

PostgreSQL has `PREPARE TRANSACTION`, `COMMIT PREPARED`, and `ROLLBACK PREPARED` for an external transaction manager. The feature is disabled by default through `max_prepared_transactions = 0`. PostgreSQL warns against leaving prepared transactions open because they retain locks and can block vacuum cleanup. These commands are not a replacement for a coordinator. Do not use them as ordinary application transaction commands.

## A long workflow is different

Suppose an order service reserves a seat, then a payment service charges a card. A **saga** breaks this into local transactions and records the workflow state. If payment fails, it can ask the seat service to release the reservation. That release is a new action, called a **compensation**, not a database rollback across both services. A refund may also be needed if a later step fails after a charge. Compensations can fail, so the workflow needs retries, a way to inspect stuck work, and a clear final state.

| Step | Local result | If the next step fails |
| --- | --- | --- |
| Reserve seat for request `R7`. | Seat is held for a limited time. | Release the same reservation. |
| Charge payment for `R7`. | Payment provider reports an outcome. | Check the provider's recorded outcome before retrying. |
| Confirm order `R7`. | Customer sees one confirmed order. | Reconcile the order with reservation and payment records. |

The request ID matters. A network timeout after charging does not tell the client whether the charge happened. A retry with the same idempotency key should return the same outcome instead of charging twice, if the payment provider supports that contract. A compensation may have business limits: a sent parcel or email cannot simply be unsent.

## Keep an event with its local write

A service often must save an order and later publish `OrderCreated`. Sending the message before commit may announce an order that rolls back. Sending it after commit may be skipped if the process crashes. A **transactional outbox** saves the event in the same database transaction as the order. A separate worker publishes stored events later.

This PostgreSQL example uses ordinary tables in a scratch database so the outbox row is durable after commit. Remove the two tables when finished.

```sql
CREATE TABLE lesson_orders (
    order_id INTEGER PRIMARY KEY,
    status TEXT NOT NULL
);
CREATE TABLE lesson_outbox (
    event_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES lesson_orders(order_id),
    event_type TEXT NOT NULL
);

BEGIN;
INSERT INTO lesson_orders VALUES (7, 'created');
INSERT INTO lesson_outbox VALUES (70, 7, 'OrderCreated');
COMMIT;

SELECT o.order_id, o.status, e.event_type
FROM lesson_orders AS o
JOIN lesson_outbox AS e ON e.order_id = o.order_id;
```

The result is `(7, created, OrderCreated)`. If either insert fails and the transaction rolls back, neither row remains. The relay may publish event `70`, crash before recording success, and publish it again. The receiver must recognize the event ID or otherwise handle duplicates. The outbox joins the **local database write** to the promise to publish; it does not make the broker and database one transaction.

## Try it yourself

1. Why can a prepared participant not simply decide to abort when it loses contact with the coordinator?
2. Why is releasing a seat a compensation instead of a rollback of the payment service's database?
3. What does the outbox example guarantee, and what does it leave to the relay and receiver?
4. What should happen when a payment request times out after it may have charged the card?

## References

- [PostgreSQL prepared transactions](https://www.postgresql.org/docs/current/sql-prepare-transaction.html)
- [PostgreSQL prepared-transaction setting](https://www.postgresql.org/docs/current/runtime-config-resource.html)
- [Original Sagas paper](https://www.cs.princeton.edu/techreports/1987/070.pdf)
- [Transactional outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html)
