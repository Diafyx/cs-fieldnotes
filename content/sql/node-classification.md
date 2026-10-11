# Node Classification

A tree node is a root when it has no parent, a leaf when it has no children, and an inner node when it has both a parent and a child. `CASE` can choose one label for each node.

## The question

`parent_id` points to another row's `id`. The rows form a valid tree with one root. Return every ID and its type, sorted by ID.

```sql
CREATE TEMP TABLE tree_nodes (
  id integer PRIMARY KEY,
  parent_id integer
);

INSERT INTO tree_nodes (id, parent_id) VALUES
  (1, NULL),
  (2, 1),
  (3, 1),
  (4, 2);
```

## A solution

```sql
SELECT n.id,
       CASE
         WHEN n.parent_id IS NULL THEN 'Root'
         WHEN EXISTS (
           SELECT 1
           FROM tree_nodes AS child
           WHERE child.parent_id = n.id
         ) THEN 'Inner'
         ELSE 'Leaf'
       END AS node_type
FROM tree_nodes AS n
ORDER BY n.id;
```

The output is `(1, Root)`, `(2, Inner)`, `(3, Leaf)`, and `(4, Leaf)`. The `EXISTS` query asks whether at least one child points to the current node. It does not need to count every child.

Check the root first. A root with children would also satisfy the child test, but it should still be labelled `Root`. A tree with only one node also works: that node has no parent and is labelled `Root`.

If the data contains an invalid parent reference or more than one root, this query still assigns labels. It does not prove that the rows form a valid tree; that must be checked separately.

## Check your understanding

1. Why is node 2 an inner node?
2. Why must the root rule come before the child rule?
3. What does `EXISTS` test for in this query?

## Further reading

- [LeetCode Tree Node](https://leetcode.com/problems/tree-node/)
- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
