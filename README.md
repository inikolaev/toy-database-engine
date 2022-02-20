# Toy Database Engine

A toy in-memory relational database engine for educational purposes in order to better understand what are the basic primitives needed to implement a database engine.

SQL is not supported, but implemented lower level API can be used to implement some basic SQL support. 

## Running

You need to have Python 3.10 installed in order to run it. The main and only executable file is `main.py`. There's nothing fancy, it's just runs a predefined query against two tables which should be equvalent to the following SQL:

```sql
select "left".id id
     , "left".name name
  from employees "left" 
  left outer join tasks "right"
    on "left".id = "right".employee_id
 where "right".employee_id is null   
```
