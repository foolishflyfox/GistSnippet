
## Ignoring Files

```
# ignore files whose suffix is .o or .a
*.[oa]

# you can negate a pattern by starting it with an exclation point(!)
!hello.o

# ignore files whose names end with a tilde, which is used by many text editors to mark temporary files
*~

# you can start patterns with a forward slash (/) to avoid recursivity
# follow line means just ignore .log in current directory
/.log

# you can end patterns with a forward slash (/) to specify a directory
# ignore entire models directory
models/

# ignore all .pdf files in the doc/ directory and any of its subdirectories
doc/**/*.pdf
```

Standard glob patterns work in gitignore, glob is very simple: 
- `*`: matches zero or more characters
- `[abc]`: matches any character insidethe brackets
- `?`: matches a single character
- `[0-5]`: matches 0,1,2,3,4
- `a/**/z`: matches a/z, a/b/z, a/b/c/z and so on

.gitignore example for dozens of projects and languages at <https://github.com/github/gitignore>





