# Java 代码评审检查清单

> 精炼自《Java 开发手册（黄山版）》v1.7.1（327 条规约，其中【强制】193 /【推荐】97 /【参考】37），用于**代码编写自查**与**代码评审逐项核对**。
> 完整规约、正反例与说明见 [`java-coding-guidelines.md`](./java-coding-guidelines.md)（按章节全文引用）。
> 用法：评审时逐项勾选；发现违规记录为 `文件:行号 - 违反条款 - 建议修复`，评审结束后统一反馈。

## 一、编程规约

### 1. 命名风格

- [ ] 类名 UpperCamelCase（DO/PO/DTO/BO/VO/UID 等除外）；方法、参数、成员/局部变量 lowerCamelCase；常量全大写 + 下划线分隔
- [ ] 命名不以 `_` / `$` 开头或结尾；不使用拼音与英文混写、不使用中文命名
- [ ] 包名全小写、单数；类型与中括号紧挨（`String[] args` 而非 `String args[]`）
- [ ] POJO 布尔属性不加 `is` 前缀（如 `Boolean deleted` 而非 `isDeleted`）
- [ ] 抽象类以 `Abstract` / `Base` 开头，异常类以 `Exception` 结尾，测试类以被测类名开头、`Test` 结尾
- [ ] 避免子父类成员变量 / 局部变量完全同名；杜绝不规范英文缩写
- [ ] 代码与注释中不出现种族歧视性、侮辱性词语（含黑名单单词）

### 2. 常量定义

- [ ] 禁止魔法值直出代码（数字/字符串必须预先定义常量）
- [ ] `long` 数值后缀用大写 `L`；浮点后缀统一大写 `D` / `F`

### 3. 代码格式

- [ ] 4 空格缩进，禁止 Tab；行宽 ≤ 120 字符；UTF-8 + Unix 换行
- [ ] 运算符两侧空格；`if/for/while/switch/do` 与括号间空格；左大括号前空格；强制转换右括号后无空格
- [ ] 多参数逗号后必须空格；注释 `//` 后一个空格
- [ ] 空代码块 `{}` 不换行；非空代码块大括号换行规则按手册

### 4. OOP 规约

- [ ] 覆写方法必须加 `@Override`；不用过时类/方法；对外接口签名不可修改，过时接口加 `@Deprecated`
- [ ] 通过类名访问静态成员，不用对象引用
- [ ] `equals` 用常量或确定非空对象调用（`"str".equals(x)`）；整型包装类比较一律 `equals`
- [ ] 浮点等值判断禁用 `==` / `equals`，使用 `BigDecimal`；`BigDecimal` 等值用 `compareTo`
- [ ] 禁止 `new BigDecimal(double)` 构造；金额以最小货币单位整型存储
- [ ] POJO 不设属性默认值；DO 属性类型与数据库字段类型匹配
- [ ] POJO 必须写 `toString()`（继承场景含 `super.toString()`）；禁止同一 POJO 同时有 `isXxx()` 与 `getXxx()`
- [ ] 序列化类新增属性不改 `serialVersionUID`；构造方法禁止业务逻辑（放 `init` 方法）

### 5. 日期时间

- [ ] 一律使用 `java.time`（LocalDate/LocalDateTime/Instant）；禁止 `java.sql.Date/Time/Timestamp`
- [ ] 年份 pattern 用小写 `y`；区分 `M`/`m`、`H`/`h`；获取毫秒用 `System.currentTimeMillis()`
- [ ] 禁止写死 365 天（闰年）；日期格式化器用线程安全的 `DateTimeFormatter`

### 6. 集合处理

- [ ] `equals` 重写必须同步重写 `hashCode`；集合判空用 `isEmpty()` 不用 `size()==0`
- [ ] 指定初始容量（`new HashMap<>(16)` 等）；`ArrayList` 大批量插入预估容量
- [ ] `toMap()` 必须传 `mergeFunction`（防 key 冲突抛异常）；`toList()`/`toSet()` 等 stream 收集注意空元素
- [ ] `Collections` 返回的不可变集合（`emptyList`/`singletonList`）不可再增删
- [ ] `Arrays.asList()` 转的集合不可 `add`/`remove`；`subList` 不可直接强转 `ArrayList`
- [ ] foreach 中禁止 `add`/`remove`（用迭代器 `remove` 或 `removeIf`）；`HashSet` 元素须实现 `hashCode/equals`
- [ ] `Map` 遍历用 `entrySet()` 而非重复 `get(key)`；`Map.getOrDefault` 等默认值方法慎用于会产生对象的方法
- [ ] 使用 `ConcurrentHashMap` 替代 `Hashtable`/`Collections.synchronizedMap` 场景；`CopyOnWriteArrayList` 只读多写少

### 7. 并发处理

- [ ] 线程池禁止用 `Executors` 快捷方法（`newFixedThreadPool` 等），用 `ThreadPoolExecutor` 显式指定队列与拒绝策略
- [ ] 高并发下避免 `new Date()` 取时间（用 `System.currentTimeMillis()`）；`SimpleDateFormat` 非线程安全
- [ ] `volatile` 不保证原子性；`synchronized` 锁对象不可用 `this` 的 `String` 常量/缓存对象
- [ ] 并发修改同一记录加锁；`ThreadLocal` 用后 `remove()`（线程池复用场景）
- [ ] 多线程资源竞争优先用 `ReentrantLock` 可中断/超时获取；锁的粒度要小
- [ ] 异步任务传递上下文用 `TransmittableThreadLocal`（阿里 TTL）；禁止在主线程中 `Thread.sleep` 等待子线程

### 8. 控制语句

- [ ] 禁止在 `if/else`、`for/while`、`do` 后不加大括号；卫语句优先（条件先行 return/throw）
- [ ] `switch` 每个分支要么 `break`/`return` 要么注释说明；`switch` 必须有 `default`
- [ ] 高并发场景避免使用 `"=="` 判断字符串（用 `equals`）；`if` 中禁止复杂表达式副作用
- [ ] 循环内禁止拼接字符串（用 `StringBuilder`）；`for` 循环变量作用域最小化

### 9. 注释规约

- [ ] 类、类属性、类方法必须加 Javadoc（`/** */`），且 `@author` 等标签规范
- [ ] 注释内容与代码一致，修改代码同步修改注释；注释掉的代码必须删除
- [ ] 枚举字段、特殊用途代码必须注释说明；对外接口必须说明参数/返回值/异常

### 10. 前后端规约

- [ ] 禁止在代码或文档中出现「黑人」「白色」等歧视性用语（1.7.0 起约定）
- [ ] 前后端数据交互统一使用 JSON；字段命名统一 camelCase（后端）与对应格式
- [ ] 涉及敏感操作（转账、删除等）日志需保存六个月以上

### 11. 其他

- [ ] 禁止使用不推荐/废弃的 API（`Date` 构造等）；`System.out.println` 仅限本地调试
- [ ] 避免在循环中做 IO、远程调用等耗时操作

## 二、异常日志

### 1. 错误码

- [ ] 错误码按 A（系统）/B（业务）/C（第三方）分类规范定义，见附3 错误码列表
- [ ] 错误码统一管理、禁止重复；接口返回必须包含错误码与错误描述

### 2. 异常处理

- [ ] 禁止用异常做流程控制（如 `try/catch` 包裹正常逻辑）；`catch` 后必须处理（记录日志 + 抛出/降级），禁止吞异常
- [ ] 捕获异常不要用 `catch (Exception e)` 后 `printStackTrace` 了事；需区分可恢复/不可恢复异常
- [ ] 方法签名声明异常与内部抛出异常一致；禁止捕获后不抛出也不记录
- [ ] 事务方法中 `catch` 异常后需要重新抛出，否则事务不生效（回滚失效）
- [ ] 不要在 `finally` 中 `return`；`finally` 中释放资源；使用 try-with-resources
- [ ] 异常信息要包含上下文（业务数据），便于排查；禁止 `e.getMessage()` 为空时的裸抛

### 3. 日志规约

- [ ] 日志必须使用占位符 `{}`，禁止字符串拼接；禁止 `System.out` 输出日志
- [ ] 日志分级正确：`debug` 记录调试、`info` 记录关键流程、`warn` 潜在问题、`error` 异常
- [ ] 禁止记录敏感信息（密码、token、身份证、银行卡等）；日志需脱敏
- [ ] 避免日志刷屏（高频循环内减少日志）；应用必须有 `traceId`/请求链路标识

## 三、单元测试

- [ ] 测试类与被测类同包、命名 `XxxTest`；测试方法 `testXxx_条件_期望`
- [ ] 单元测试必须可重复执行（不依赖环境、时间、随机）；禁止用 `Thread.sleep` 等待
- [ ] 断言用具体值而非 `true`（`assertEquals(期望, 实际)`）；覆盖正常/异常/边界三路径
- [ ] 有数据库操作必须有事务回滚或清理；测试数据不污染生产
- [ ] 构造测试数据用工厂方法/构建器，避免测试代码与业务代码耦合过深

## 四、安全规约

- [ ] 用户请求必须鉴权；接口防越权（水平/垂直越权都要校验）
- [ ] SQL 禁止字符串拼接（防注入），用参数绑定/MyBatis `#{}`
- [ ] 文件上传校验类型/大小/内容；下载路径防目录穿越；不信任前端传的文件名
- [ ] 密码存储用加盐哈希（BCrypt 等），禁止 MD5/SHA 明文存储；敏感数据加密传输
- [ ] XSS：前端输出转义、后端校验过滤；CSRF：写操作校验 token/同源
- [ ] 日志/错误信息不泄露堆栈细节给终端用户；越权访问返回 403 而非泄露资源存在性

## 五、MySQL 数据库

### 1. 建表规约

- [ ] 表名/字段名小写下划线，禁止驼峰与保留字；表必须有主键 `id`（自增或雪花）
- [ ] 字段必须有注释；`is_xxx` 表示布尔；金额用 `decimal`，禁止 `float/double`
- [ ] 时间用 `datetime`（非 timestamp，避免 2038 问题与时区坑）；`varchar` 需设计长度
- [ ] 每张表必须有 `create_time`/`update_time`；删除用逻辑删除（`deleted` 字段）
- [ ] 禁止三张以上表 join；大表必须分库分表规划；字段数量控制（单表字段不宜过多）

### 2. SQL 语句

- [ ] 禁止 `SELECT *`；必须带 `WHERE`（update/delete 尤其）；`LIMIT` 分页必带
- [ ] 禁止对索引列做函数/隐式转换（`WHERE DATE(create_time)=...` 禁止）
- [ ] 禁止 `count(*)` 大数据量统计；禁止 `!=`/`NOT IN` 导致索引失效的场景
- [ ] 大批量数据更新分批处理（`LIMIT 1000` 循环）；禁止循环内单条 SQL 插入

### 3. 索引规约

- [ ] 唯一索引命名 `uk_`、普通索引 `idx_`；索引字段顺序最左前缀匹配
- [ ] 禁止冗余索引（联合索引可覆盖单列时不再建单列索引）；`like '%xxx%'` 不走索引
- [ ] 索引区分度：选择度低的列（性别、状态）不适合单独建索引

### 4. ORM 映射

- [ ] `@Transactional` 只加在需要的方法上；禁止加在类/接口上；回滚指定异常
- [ ] 禁止在事务中做远程调用/耗时操作；查询用 DTO 不返回实体全字段
- [ ] MyBatis `#{}` 与 `${}` 区分（`${}` 禁止用于用户输入）；批量操作使用 batch
- [ ] 实体字段与表字段映射必须显式、类型匹配；`delete` 数据前检查外键引用

## 六、工程结构

- [ ] 应用分层：`controller → service → dao`，禁止跨层调用（controller 直连 dao 禁止）
- [ ] 二方库依赖统一管理版本（BOM），禁止依赖冲突；禁止循环依赖模块
- [ ] 服务器：JVM 参数统一（`-Xms`=`-Xmx`、`-Dfile.encoding=UTF-8`）；禁止硬编码端口/环境
- [ ] 配置外置：环境差异（dev/test/prod）走配置文件，禁止代码内 `if(环境)` 分支
- [ ] 日志文件滚动策略（按天/按大小），保留期限明确；禁止日志无限增长

## 七、设计规约

- [ ] 需求评审必须设计先行：数据库设计、接口设计、异常设计、幂等设计
- [ ] 接口设计遵循单一职责；对外接口必须幂等（防重复提交）
- [ ] 禁止过度设计；抽象合理性（不为了模式而模式）
- [ ] 新老系统兼容：灰度发布、双写、回滚方案；不兼容变更必须有迁移方案

---

## 评审结论模板

```markdown
### 评审结论
- 整体结论：通过 / 有条件通过 / 不通过
- 强制违规：N 处（必须修复）
- 推荐改进：N 处（建议修复）
- 主要问题：
  1. `文件:行号` - 违反条款 - 说明
- 遗留风险：……
```
