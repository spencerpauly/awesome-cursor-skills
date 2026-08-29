# Java Code Review Checklist (English Edition)

> Condensed from the official English *Alibaba Java Coding Guidelines* (5 sections, **124 Mandatory / 57 Recommended / 24 For Reference** rules), for **self-check while writing code** and **item-by-item review of Java code**.
> Full rules, positive/counter examples and notes: see [`java-coding-guidelines-en.md`](./java-coding-guidelines-en.md).
> Usage: tick each item during review; record violations as `file:line - rule violated - suggested fix`, then report them all together at the end.

## Legend

- `[M]` = **[Mandatory]** (blocking for merge)
- `[R]` = **[Recommended]** (high-value improvement)
- `[F]` = **[For Reference]** (adopt as appropriate)

## 1. Programming Specification

### Naming Conventions

- [ ] **[M]** 1. Names should not start or end with an underline or a dollar sign.
- [ ] **[M]** 2. Using Chinese, Pinyin, or Pinyin-English mixed spelling in naming is strictly prohibited. Accurate English spelling and grammar will make the code readable, understandable, and maintainable.
- [ ] **[M]** 3. Class names should be nouns in UpperCamelCase except domain models: DO, BO, DTO, VO, etc.
- [ ] **[M]** 4. Method names, parameter names, member variable names, and local variable names should be written in lowerCamelCase.
- [ ] **[M]** 5. Constant variable names should be written in upper characters separated by underscores. These names should be semantically complete and clear.
- [ ] **[M]** 6. Abstract class names must start with *Abstract* or *Base*. Exception class names must end with *Exception*. Test case names shall start with the class names to be tested and end with *Test*.
- [ ] **[M]** 7. Brackets are a part of an Array type. The definition could be: *String[] args;*
- [ ] **[M]** 8. Do not add 'is' as prefix while defining Boolean variable, since it may cause a serialization exception in some Java frameworks.
- [ ] **[M]** 9. A package should be named in lowercase characters. There should be only one English word after each dot. Package names are always in singular format while class names can be in plural format if necessary.
- [ ] **[M]** 10. Uncommon abbreviations should be avoided for the sake of legibility.
- [ ] **[R]** 11. The pattern name is recommended to be included in the class name if any design pattern is used.
- [ ] **[R]** 12. Do not add any modifier, including `public`, to methods in interface classes for coding simplicity. Please add valid *Javadoc* comments for methods. Do not define any variables in the interface except for the common constants of the application.
    - [ ] **[M]** 1) All *Service* and *DAO* classes must be interfaces based on SOA principle. Implementation class names should end with *Impl*.
    - [ ] **[R]** 2) If the interface name is to indicate the ability of the interface, then its name should be an adjective.
- [ ] **[F]** 14. An Enumeration class name should end with *Enum*. Its members should be spelled out in upper case words, separated by underlines.
- [ ] **[F]** 15. Naming conventions for different package layers:

### Constant Conventions

- [ ] **[M]** 1. Magic values, except for predefined, are forbidden in coding.
- [ ] **[M]** 2. 'L' instead of 'l' should be used for long or Long variable because 'l' is easily to be regarded as number 1 in mistake.
- [ ] **[R]** 3. Constants should be placed in different constant classes based on their functions. For example, cache related constants could be put in `CacheConsts` while configuration related constants could be kept in `ConfigConsts`.
- [ ] **[R]** 4. Constants can be shared in the following 5 different layers: *shared in multiple applications; shared inside an application; shared in a sub-project; shared in a package; shared in a class*.
- [ ] **[R]** 5. Use an enumeration class if values lie in a fixed range or if the variable has attributes. The following example shows that extra information (which day it is) can be included in enumeration:

### Formatting Style

- [ ] **[M]** 1. Rules for braces. If there is no content, simply use *{}* in the same line. Otherwise:
- [ ] **[M]** 2. No space is used between the '(' character and its following character. Same for the ')' character and its preceding character. Refer to the *Positive Example* at the 5th rule.
- [ ] **[M]** 3. There must be one space between keywords, such as if/for/while/switch, and parentheses.
- [ ] **[M]** 4. There must be one space at both left and right side of operators, such as '=', '&&', '+', '-', *ternary operator*, etc.
- [ ] **[M]** 5. Each time a new block or block-like construct is opened, the indent increases by four spaces. When the block ends, the indent returns to the previous indent level. Tab characters are not used for indentation.
- [ ] **[M]** 6. Java code has a column limit of 120 characters. Except import statements, any line that would exceed this limit must be line-wrapped as follows:
- [ ] **[M]** 7. There must be one space between a comma and the next parameter for methods with multiple parameters.
- [ ] **[M]** 8. The charset encoding of text files should be *UTF-8* and the characters of line breaks should be in *Unix* format, instead of *Windows* format.
- [ ] **[R]** 9. It is unnecessary to align variables by several spaces.
- [ ] **[R]** 10. Use a single blank line to separate sections with the same logic or semantics.

### OOP Rules

- [ ] **[M]** 1. A static field or method should be directly referred to by its class name instead of its corresponding object name.
- [ ] **[M]** 2. An overridden method from an interface or abstract class must be marked with `@Override` annotation.
- [ ] **[M]** 3. *varargs* is recommended only if all parameters are of the same type and semantics. Parameters with `Object` type should be avoided.
- [ ] **[M]** 4. Modifying the method signature is forbidden to avoid affecting the caller. A `@Deprecated` annotation with an explicit description of the new service is necessary when an interface is deprecated.
- [ ] **[M]** 5. Using a deprecated class or method is prohibited.
- [ ] **[M]** 6. Since `NullPointerException` can possibly be thrown while calling the *equals* method of `Object`, *equals* should be invoked by a constant or an object that is definitely not *null*.
- [ ] **[M]** 7. Use the `equals` method, rather than reference equality `==`, to compare primitive wrapper classes.
- [ ] **[M]** 8. To judge the equivalence of floating-point numbers, `==` cannot be used for primitive types, while `equals` cannot be used for wrapper classes.
- [ ] **[M]** 9. Rules for using primitive data types and wrapper classes:
    - [ ] **[R]** 3) Local variables should be primitive data types.
- [ ] **[M]** 10. While defining POJO classes like DO, DTO, VO, etc., do not assign any default values to the members.
- [ ] **[M]** 11. To avoid a deserialization failure, do not change the *serialVersionUID* when a serialized class needs to be updated, such as adding some new members. If a completely incompatible update is needed, change the value of *serialVersionUID* in case of a confusion when deserialized.
- [ ] **[M]** 12. Business logic in constructor methods is prohibited. All initializations should be implemented in the `init` method.
- [ ] **[M]** 13. The `toString` method must be implemented in a POJO class. The `super.toString` method should be called in in the beginning of the implementation if the current class extends another POJO class.
- [ ] **[R]** 14. When accessing an array generated by the split method in String using an index, make sure to check the last separator whether it is null to avoid `IndexOutOfBoundException`.
- [ ] **[R]** 15. Multiple constructor methods or homonymous methods in a class should be put together for better readability.
- [ ] **[R]** 16. The order of methods declared within a class is:
- [ ] **[R]** 17. For a *setter* method, the argument name should be the same as the field name. Implementations of business logics in *getter/setter* methods, which will increase difficulties of the troubleshooting, are not recommended.
- [ ] **[R]** 18. Use the `append` method in `StringBuilder` inside a loop body when concatenating multiple strings.
- [ ] **[R]** 19. Keyword *final* should be used in the following situations:
- [ ] **[R]** 20. Be cautious to copy an object using the `clone` method in `Object`.
- [ ] **[R]** 21. Define the access level of members in class with severe restrictions:

### Collection

- [ ] **[M]** 1. The usage of *hashCode* and *equals* should follow:
- [ ] **[M]** 2. Do not add elements to collection objects returned by `keySet()`/`values()`/`entrySet()`, otherwise `UnsupportedOperationException` will be thrown.
- [ ] **[M]** 3. Do not add nor remove to/from immutable objects returned by methods in `Collections`, e.g. `emptyList()`/`singletonList()`.
- [ ] **[M]** 4. Do not cast *subList* in class `ArrayList`, otherwise `ClassCastException` will be thrown: `java.util.RandomAccessSubList` cannot be cast to `java.util.ArrayList`.
- [ ] **[M]** 5. When using *subList*, be careful when modifying the size of original list. It might cause `ConcurrentModificationException` when performing traversing, adding or deleting on the *subList*.
- [ ] **[M]** 6. Use `toArray(T[] array)` to convert a list to an array. The input array type should be the same as the list whose size is `list.size()`.
- [ ] **[M]** 7. Do not use methods which will modify the list after using `Arrays.asList` to convert array to list, otherwise methods like *add/remove/clear* will throw `UnsupportedOperationException`.
- [ ] **[M]** 8. Method `add` cannot be used for generic wildcard with `<? Extends T>`, method `get` cannot be used with `<? super T>`, which probably goes wrong.
- [ ] **[M]** 9. Do not remove or add elements to a collection in a *foreach* loop. Please use `Iterator` to remove an item. `Iterator` object should be synchronized when executing concurrent operations.
- [ ] **[M]** 10. In JDK 7 and above version, `Comparator` should meet the three requirements listed below, otherwise `Arrays.sort` and `Collections.sort` will throw `IllegalArgumentException`.
- [ ] **[R]** 11. Set a size when initializing a collection if possible.
- [ ] **[R]** 12. Use `entrySet` instead of `keySet` to traverse KV maps.
- [ ] **[R]** 13. Carefully check whether a *k/v collection* can store *null* value, refer to the table below:
- [ ] **[F]** 14. Properly use sort and order of a collection to avoid negative influence of unsorted and unordered one.
- [ ] **[F]** 15. Deduplication operations could be performed quickly since set stores unique values only. Avoid using method *contains* of `List` to perform traverse, comparison and de-duplication.

### Concurrency

- [ ] **[M]** 1. Thread-safe should be ensured when initializing singleton instance, as well as all methods in it.
- [ ] **[M]** 2. A meaningful thread name is helpful to trace the error information, so assign a name when creating threads or thread pools.
- [ ] **[M]** 3. Threads should be provided by thread pools. Explicitly creating threads is not allowed.
- [ ] **[M]** 4. A thread pool should be created by `ThreadPoolExecutor` rather than `Executors`. These would make the parameters of the thread pool understandable. It would also reduce the risk of running out of system resource.
- [ ] **[M]** 5. `SimpleDateFormat` is unsafe, do not define it as a *static* variable. If have to, lock or `DateUtils` class must be used.
- [ ] **[M]** 6. `remove()` method must be implemented by `ThreadLocal` variables, especially when using thread pools in which threads are often reused. Otherwise, it may affect subsequent business logic and cause unexpected problems such as memory leak.
- [ ] **[M]** 7. In highly concurrent scenarios, performance of `Lock` should be considered in synchronous calls. A block lock is better than a method lock. An object lock is better than a class lock.
- [ ] **[M]** 8. When adding locks to multiple resources, tables in the database and objects at the same time, locking sequence should be kept consistent to avoid deadlock.
- [ ] **[M]** 9. When getting a lock by blocking methods, such as waiting in the blocking queue, lock() implemented from Lock must be put outside the try block. Besides, make sure no method between the lock() and try block in case that the lock won't be released in the finally block.
- [ ] **[M]** 10. A lock needs to be used to avoid update failure when modifying one record concurrently. Add lock either in application layer, in cache, or add optimistic lock in the database by using version as update stamp.
- [ ] **[M]** 11. Run multiple `TimeTask` by using `ScheduledExecutorService` rather than `Timer` because `Timer` will kill all running threads in case of failing to catch exceptions.
- [ ] **[R]** 12. When using `CountDownLatch` to convert asynchronous operations to synchronous ones, each thread must call `countdown` method before quitting. Make sure to catch any exception during thread running, to let `countdown` method be executed. If main thread cannot reach `await` method, program will return until timeout.
- [ ] **[R]** 13. Avoid using `Random` instance by multiple threads. Although it is safe to share this instance, competition on the same seed will damage performance.
- [ ] **[R]** 14. In concurrent scenarios, one easy solution to optimize the lazy initialization problem by using double-checked locking (referred to The Double-checked locking is broken Declaration), is to declare the object type as `volatile`.
- [ ] **[F]** 15. `volatile` is used to solve the problem of invisible memory in multiple threads. *Write-Once-Read-Many* can solve variable synchronization problem. But *Write-Many* cannot settle thread safe problem. For `count++`, use below example:
- [ ] **[F]** 16. Resizing `HashMap` when its capacity is not enough might cause dead link and high CPU usage because of high-concurrency. Avoid this risk in development.
- [ ] **[F]** 17. `ThreadLocal` cannot solve update problems of shared object. It is recommended to use a *static* `ThreadLocal` object which is shared by all operations in the same thread.

### Flow Control Statements

- [ ] **[M]** 1. In a `switch` block, each case should be finished by *break/return*. If not, a note should be included to describe at which case it will stop. Within every `switch` block, a default statement must be present, even if it is empty.
- [ ] **[M]** 2. Braces are used with *if*, *else*, *for*, *do* and *while* statements, even if the body contains only a single statement. Avoid using the following example:
- [ ] **[R]** 3. Use `else` as less as possible, `if-else` statements could be replaced by:
- [ ] **[R]** 4. Do not use complicated statements in conditional statements (except for frequently used methods like *getXxx/isXxx*). Use *boolean* variables to store results of complicated statements temporarily will increase the code's readability.
- [ ] **[R]** 5. Performance should be considered when loop statements are used. The following operations are better to be processed outside the loop statement, including object and variable declaration, database connection, `try-catch` statements.
- [ ] **[R]** 6. Size of input parameters should be checked, especially for batch operations.
- [ ] **[F]** 7. Input parameters should be checked in following scenarios:
- [ ] **[F]** 8. Cases that input parameters do not require validation:

### Code Comments

- [ ] **[M]** 1. *Javadoc* should be used for classes, class variables and methods. The format should be '/\*\* comment \*\*/', rather than '// xxx'.
- [ ] **[M]** 2. Abstract methods (including methods in interface) should be commented by *Javadoc*. *Javadoc* should include method instruction, description of parameters, return values and possible exceptions.
- [ ] **[M]** 3. Every class should include information of author(s) and date.
- [ ] **[M]** 4. Single line comments in a method should be put above the code to be commented, by using `//` and multiple lines by using `/* */`. Alignment for comments should be noticed carefully.
- [ ] **[M]** 5. All enumeration type fields should be commented as *Javadoc* style.
- [ ] **[R]** 6. Local language can be used in comments if English cannot describe the problem properly. Keywords and proper nouns should be kept in English.
- [ ] **[R]** 7. When code logic changes, comments need to be updated at the same time, especially for the changes of parameters, return value, exception and core logic.
- [ ] **[F]** 8. Notes need to be added when commenting out code.
- [ ] **[F]** 9. Requirements for comments:
- [ ] **[F]** 10. Proper naming and clear code structure are self-explanatory. Too many comments need to be avoided because it may cause too much work on updating if code logic changes.
- [ ] **[F]** 11. Tags in comments (e.g. TODO, FIXME) need to contain author and time. Tags need to be handled and cleared in time by scanning frequently. Sometimes online breakdown is caused by these unhandled tags.

### Other

- [ ] **[M]** 1. When using regex, precompile needs to be done in order to increase the matching performance.
- [ ] **[M]** 2. When using attributes of POJO in velocity, use attribute names directly. Velocity engine will invoke `getXxx()` of POJO automatically. In terms of *boolean* attributes, velocity engine will invoke `isXxx()` (Do not use *is* as prefix when naming boolean attributes).
- [ ] **[M]** 3. Variables must add exclamatory mark when passing to velocity engine from backend, like \$!{var}.
- [ ] **[M]** 4. The return type of `Math.random()` is double, value range is *0<=x<1* (0 is possible). If a random integer is required, do not multiply x by 10 then round the result. The correct way is to use `nextInt` or `nextLong` method which belong to Random Object.
- [ ] **[M]** 5. Use `System.currentTimeMillis()` to get the current millisecond. Do not use `new Date().getTime()`.
- [ ] **[R]** 6. It is better not to contain variable declaration, logical symbols or any complicated logic in velocity template files.
- [ ] **[R]** 7. Size needs to be specified when initializing any data structure if possible, in order to avoid memory issues caused by unlimited growth.
- [ ] **[R]** 8. Codes or configuration that is noticed to be obsoleted should be resolutely removed from projects.

## 2. Exception and Logs

### Exception

- [ ] **[M]** 1. Do not catch *Runtime* exceptions defined in *JDK*, such as `NullPointerException` and `IndexOutOfBoundsException`. Instead, pre-check is recommended whenever possible.
- [ ] **[M]** 2. Never use exceptions for ordinary control flow. It is ineffective and unreadable.
- [ ] **[M]** 3. It is irresponsible to use a try-catch on a big chunk of code. Be clear about the stable and unstable code when using try-catch. The stable code that means no exception will throw. For the unstable code, catch as specific as possible for exception handling.
- [ ] **[M]** 4. Do not suppress or ignore exceptions. If you do not want to handle it, then re-throw it. The top layer must handle the exception and translate it into what the user can understand.
- [ ] **[M]** 5. Make sure to invoke the rollback if a method throws an Exception.
- [ ] **[M]** 6. Closeable resources (stream, connection, etc.) must be handled in *finally* block. Never throw any exception from a *finally* block.
- [ ] **[M]** 7. Never use *return* within a *finally* block. A *return* statement in a *finally* block will cause exceptions or result in a discarded return value in the *try-catch* block.
- [ ] **[M]** 8. The *Exception* type to be caught needs to be the same class or superclass of the type that has been thrown.
- [ ] **[R]** 9. The return value of a method can be *null*. It is not mandatory to return an empty collection or object. Specify in *Javadoc* explicitly when the method might return *null*. The caller needs to make a *null* check to prevent `NullPointerException`.
- [ ] **[R]** 10. One of the most common errors is `NullPointerException`. Pay attention to the following situations:
- [ ] **[R]** 11. Use "throw exception" or "return error code". For HTTP or open API providers, "error code" must be used. It is recommended to throw exceptions inside an application. For cross-application RPC calls, result is preferred by encapsulating *isSuccess*, *error code* and brief error messages.
- [ ] **[R]** 12. Do not throw `RuntimeException`, `Exception`, or `Throwable` directly. It is recommended to use well defined custom exceptions such as `DAOException`, `ServiceException`, etc.
- [ ] **[F]** 13. Avoid duplicate code (Do not Repeat Yourself, also known as DRY principle).

### Logs

- [ ] **[M]** 1. Do not use API in log system (Log4j, Logback) directly. API in log framework SLF4J is recommended to use instead, which uses *Facade* pattern and is conducive to keep log processing consistent.
- [ ] **[M]** 2. Log files need to be kept for at least 15 days because some kinds of exceptions happen weekly.
- [ ] **[M]** 3. Naming conventions of extended logs of an Application (such as RBI, temporary monitoring, access log, etc.):
- [ ] **[M]** 4. Logs at *TRACE / DEBUG / INFO* levels must use either conditional outputs or placeholders.
- [ ] **[M]** 5. Ensure that additivity attribute of a Log4j logger is set to *false*, in order to avoid redundancy and save disk space.
- [ ] **[M]** 6. The exception information should contain two types of information: the context information and the exception stack. If you do not want to handle the exception, re-throw it.
- [ ] **[R]** 7. Carefully record logs. Use *Info* level selectively and do not use *Debug* level in production environment. If *Warn* is used to record business behavior, please pay attention to the size of logs. Make sure the server disk is not over-filled, and remember to delete these logs in time.
- [ ] **[R]** 8. Level *Warn* should be used to record invalid parameters, which is used to track data when problem occurs. Level *Error* only records the system logic error, abnormal and other important error messages.

## 3. MySQL Rules

### Table Schema Rules

- [ ] **[M]** 1. Columns expressing the concept of *True* or *False*, must be named as *is_xxx*, whose data type should be *unsigned tinyint* (1 is *True*, 0 is *False*).
- [ ] **[M]** 2. Names of tables and columns must consist of lower case letters, digits or underscores. Names starting with digits and names which contain only digits (no other characters) in between two underscores are not allowed. Columns should be named cautiously, as it is costly to change column names and cannot be released in pre-release environment.
- [ ] **[M]** 3. Plural nouns are not allowed as table names.
- [ ] **[M]** 4. Keyword, such as *desc*, *range*, *match*, *delayed*, etc., should not be used. It can be referenced from MySQL official document.
- [ ] **[M]** 5. The name of primary key index should be prefixed with *pk\_*, followed by column name; Unique index should be named by prefixing its column name with *uk\_*; And normal index should be formatted as *idx_[column_name]*.
- [ ] **[M]** 6. Decimals should be typed as *decimal*. *float* and *double* are not allowed.
- [ ] **[M]** 7. Use *char* if lengths of information to be stored in that column are almost the same.
- [ ] **[M]** 8. The length of *varchar* should not exceed 5000, otherwise it should be defined as `text`. It is better to store them in a separate table in order to avoid its effect on indexing efficiency of other columns.
- [ ] **[M]** 9. A table must include three columns as following: *id*, *gmt_create* and *gmt_modified*.
- [ ] **[R]** 10. It is recommended to define table name as *[table_business_name]_[table_purpose]*.
- [ ] **[R]** 11. Try to define database name same with the application name.
- [ ] **[R]** 12. Update column comments once column meaning is changed or new possible status values are added.
- [ ] **[R]** 13. Some appropriate columns may be stored in multiple tables redundantly to improve search performance, but consistency must be concerned. Redundant columns should not be:
- [ ] **[R]** 14. Database sharding may only be recommended when there are more than 5 million rows in a single table or table capacity exceeds 2GB.
- [ ] **[F]** 15. Appropriate *char* column length not only saves database and index storing space, but also improves query efficiency.

### Index Rules

- [ ] **[M]** 1. Unique index should be used if business logic is applicable.
- [ ] **[M]** 2. *JOIN* is not allowed if more than three tables are involved. Columns to be joined must be with absolutely similar data types. Make sure that columns to be joined are indexed.
- [ ] **[M]** 3. Index length must be specified when adding index on *varchar* columns. The index length should be set according to the distribution of data.
- [ ] **[M]** 4. *LIKE '%...'* or *LIKE '%...%'* are not allowed when searching with pagination. Search engine can be used if it is really needed.
- [ ] **[R]** 5. Make use of the index order when using *ORDER BY* clauses. The last columns of *ORDER BY* clauses should be at the end of a composite index. The reason is to avoid the *file_sort* issue, which affects the query performance.
- [ ] **[R]** 6. Make use of *Covering Index* for query to avoid additional query after searching index.
- [ ] **[R]** 7. Use *late join* or *sub-query* to optimize scenarios with many pages.
- [ ] **[R]** 8. The target of SQL performance optimization is that the result type of *EXPLAIN* reaches *REF* level, or *RANGE* at least, or CONSTS if possible.
- [ ] **[R]** 9. Put the most discriminative column to the left most when adding a composite index.
- [ ] **[F]** 10. Avoid listed below misunderstandings when adding index:

### SQL Rules

- [ ] **[M]** 1. Do not use COUNT(column_name) or COUNT(constant_value) in place of COUNT(\*). COUNT(\*) is *SQL92* defined standard syntax to count the number of rows. It is not database specific and has nothing to do with *NULL* and *non-NULL*.
- [ ] **[M]** 2. COUNT(distinct column) calculates number of rows with distinct values in this column, excluding *NULL* values. Please note that COUNT(distinct column1, column2) returns *0* if all values of one of the columns are *NULL*, even if the other column contains distinct *non-NULL* values.
- [ ] **[M]** 3. When all values of one column are *NULL*, COUNT(column) returns *0*, while SUM(column) returns *NULL*, so pay attention to `NullPointerException` issue when using SUM().
- [ ] **[M]** 4. Use *ISNULL()* to check *NULL* values. Result will be *NULL* when comparing *NULL* with any other values.
- [ ] **[M]** 5. When coding on DB query with paging logic, it should return immediately once count is *0*, to avoid executing paging query statement followed.
- [ ] **[M]** 6. *Foreign key* and *cascade update* are not allowed. All foreign key related logic should be handled in application layer.
- [ ] **[M]** 7. Stored procedures are not allowed. They are difficult to debug, extend and not portable.
- [ ] **[M]** 8. When correcting data, delete and update DB records, *SELECT* should be done first to ensure data correctness.
- [ ] **[R]** 9. *IN* clause should be avoided. Record set size of the *IN* clause should be evaluated carefully and control it within 1000, if it cannot be avoided.
- [ ] **[F]** 10. For globalization needs, characters should be represented and stored with *UTF-8*, and be cautious of character number counting.
- [ ] **[F]** 11. *TRUNCATE* is not recommended when coding, even if it is faster than *DELETE* and uses less system, transaction log resource. Because *TRUNCATE* does not have transaction nor trigger DB *trigger*, problems might occur.

### ORM Rules

- [ ] **[M]** 1. Specific column names should be specified during query, rather than using \*.
- [ ] **[M]** 2. Name of *Boolean* property of *POJO* classes cannot be prefixed with *is*, while DB column name should prefix with *is*. A mapping between properties and columns is required.
- [ ] **[M]** 3. Do not use *resultClass* as return parameters, even if all class property names are the same as DB columns, corresponding DO definition is needed.
- [ ] **[M]** 4. Be cautious with parameters in xml configuration. Do not use `${}` in place of `#{}`, `#param#`. SQL injection may happen in this way.
- [ ] **[M]** 5. *iBatis* built in *queryForList(String statementName, int start, int size)* is not recommended.
- [ ] **[M]** 6. Do not use *HashMap* or *HashTable* as DB query result type.
- [ ] **[M]** 7. *gmt_modified* column should be updated with current timestamp simultaneously with DB record update.
- [ ] **[R]** 8. Do not define a universal table updating interface, which accepts POJO as input parameter, and always update table set *c1=value1, c2=value2, c3=value3, ...* regardless of intended columns to be updated. It is better not to update unrelated columns, because it is error prone, not efficient, and increases *binlog* storage.
- [ ] **[F]** 9. Do not overuse *@Transactional*. Because transaction affects QPS of DB, and relevant rollbacks may need be considered, including cache rollback, search engine rollback, message making up, statistics adjustment, etc.
- [ ] **[F]** 10. *compareValue* of *\<isEqual>* is a constant (normally a number) which is used to compared with property value. *\<isNotEmpty>* means executing corresponding logic when property is not empty and not null. *\<isNotNull>* means executing related logic when property is not null.

## 4. Project Specification

### Application Layers

- [ ] **[R]** 1. The upper layer depends on the lower layer by default. Arrow means direct dependent. For example: Open Interface can depend on Web Layer, it can also directly depend on Service Layer, etc.:
- [ ] **[F]** 2. Many exceptions in the *DAO Layer* cannot be caught by using a fine-grained exception class. The recommended way is to use `catch (Exception e)`, and `throw new DAOException(e)`. In these cases, there is no need to print the log because the log should have been caught and printed in *Manager Layer/Service Layer*.
- [ ] **[F]** 3. Layers of Domain Model:

### Library Specification

- [ ] **[M]** 1. Rules of defining GAV:
- [ ] **[M]** 2. Library naming convention: `prime version number`.`secondary version number`.`revision number`
- [ ] **[M]** 3. Online applications should not depend on *SNAPSHOT* versions (except for security packages); Official releases must be verified from central repository, to make sure that the RELEASE version number has continuity. Version numbers are not allowed to be overridden.
- [ ] **[M]** 4. When adding or upgrading libraries, remain the versions of dependent libraries unchanged if not necessary. If there is a change, it must be correctly assessed and checked. It is recommended to use command *dependency:resolve* to compare the information before and after. If the result is identical, find out the differences with the command *dependency:tree* and use *\<excludes\>* to eliminate unnecessary libraries.
- [ ] **[M]** 5. Enumeration types can be defined or used for parameter types in libraries, but cannot be used for interface return types (POJO that contains enumeration types is also not allowed).
- [ ] **[M]** 6. When a group of libraries are used, a uniform version variable need to be defined to avoid the inconsistency of version numbers.
- [ ] **[M]** 7. For the same *GroupId* and *ArtifactId*, *Version* must be the same in sub-projects.
- [ ] **[R]** 8. The declaration of dependencies in all *POM* files should be placed in *\<dependencies\>* block. Versions of dependencies should be specified in *\<dependencyManagement\>* block.
- [ ] **[R]** 9. It is recommended that libraries do not include configuration, at least do not increase the configuration items.
- [ ] **[F]** 10. In order to avoid the dependency conflict of libraries, the publishers should follow the principles below:

### Server Specification

- [ ] **[R]** 1. It is recommended to reduce the *time_wait* value of the *TCP* protocol for high concurrency servers.
- [ ] **[R]** 2. Increase the maximum number of *File Descriptors* supported by the server.
- [ ] **[R]** 3. Set `-XX:+HeapDumpOnOutOfMemoryError` parameter for *JVM*, so *JVM* will output dump information when *OOM* occurs.
- [ ] **[F]** 4. Use *forward* for internal redirection and URL assembly tools for external redirection. Otherwise there will be problems about URL maintaining inconsistency and potential security risks.

## 5. Security Specification

- [ ] **[M]** 1. User-owned pages or functions must be authorized.
- [ ] **[M]** 2. Direct display of user sensitive data is not allowed. Displayed data must be desensitized.
- [ ] **[M]** 3. *SQL* parameter entered by users should be checked carefully or limited by *METADATA*, to prevent *SQL* injection. Database access by string concatenation *SQL* is forbidden.
- [ ] **[M]** 4. Any parameters input by users must go through validation check.
- [ ] **[M]** 5. It is forbidden to output user data to *HTML* page without security filtering or proper escaping.
- [ ] **[M]** 6. Form and *AJAX* submission must be filtered by *CSRF* security check.
- [ ] **[M]** 7. It is necessary to use the correct anti-replay restrictions, such as number restriction, fatigue control, verification code checking, to avoid abusing of platform resources, such as text messages, e-mail, telephone, order, payment.
- [ ] **[R]** 8. In scenarios when users generate content (e.g., posting, comment, instant messages), anti-scam word filtering and other risk control strategies must be applied.
