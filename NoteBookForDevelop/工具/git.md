# 忽略规则 .gitignore 
忽略的语法规则：
```
(#)表示注释
(*)  表示任意多个字符; 
(?) 代表一个字符;
 ([abc]) 代表可选字符范围
如果名称最前面是路径分隔符 (/) ，表示忽略的该文件在此目录下。
如果名称的最后面是 (/) ，表示忽略整个目录，但同名文件不忽略。
通过在名称前面加 (!) ，代表不忽略。
例子如下：

# 这行是注释
*.a                   # 忽略所有 .a 伟扩展名的文件
!lib.a                # 但是 lib.a 不忽略，即时之前设置了忽略所有的 .a
/TODO            # 只忽略此目录下 TODO 文件，子目录的 TODO 不忽略 
build/               # 忽略所有的 build/ 目录下文件
doc/*.txt           # 忽略如 doc/notes.txt, 但是不忽略如 doc/server/arch.txt
```

# 其他
* [git cheat sheet](https://github.com/flyhigher139/Git-Cheat-Sheet)
* ![git-flow-commands-without-flow](https://github.com/flyhigher139/Git-Cheat-Sheet/raw/master/Img/git-flow-commands-without-flow.png)
