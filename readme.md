# git 学习

## 1、初始化一个Git仓库

使用 `git init`命令。

## 2、添加文件到Git仓库，分两步：

使用命令 `git add file`，注意，可反复多次使用，添加多个文件；
使用命令 `git commit -m ""` ，完成。

## 3、`git status`命令可以让我们时刻掌握仓库当前的状态

## 4、`git diff`顾名思义就是查看difference

## 5.`git log`命令显示从最近到最远的提交日志

## 6、版本回退

* `HEAD`指向的版本就是当前版本，因此，Git允许我们在版本的历史之间穿梭，使用命令 `git reset --hard commit_id`。
* 穿梭前，用 `git log`可以查看提交历史，以便确定要回退到哪个版本。
* 要重返未来，用 `git reflog`查看命令历史，以便确定要回到未来的哪个版本。

## 7、撤销修改

场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令 `git checkout -- file`。

场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想丢弃修改，分两步，第一步用命令 `git reset HEAD <file>`，就回到了场景1，第二步按场景1操作。

```
git reset --hard 1094a
```


场景3：已经提交了不合适的修改到版本库时，想要撤销本次提交，参考[版本回退](https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192)一节，不过前提是没有推送到远程库。

## 8、删除文件

一是确实要从版本库中删除该文件，那就用命令 `git rm`删掉，并且 `git commit`

先手动删除文件，然后使用 `git rm `和git add `file>`效果是一样的。

另一种情况是删错了，因为版本库里还有呢，所以可以很轻松地把误删的文件恢复到最新版本

`git checkout`其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原”。

注意：从来没有被添加到版本库就被删除的文件，是无法恢复的！

9、远程仓库github

```
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:619040924/pyexcel.git
git push -u origin main
```

要关联一个远程库，使用命令 `git remote add origin git@server-name:path/repo-name.git`；

关联一个远程库时必须给远程库指定一个名字，`origin`是默认习惯命名；

关联后，使用命令 `git push -u origin master`第一次推送master分支的所有内容；

此后，每次本地提交后，只要有必要，就可以使用命令 `git push origin master`推送最新修改；

分布式版本系统的最大好处之一是在本地工作完全不需要考虑远程库的存在，也就是有没有联网都可以正常工作，而SVN在没有联网的时候是拒绝干活的！当有网络的时候，再把本地提交推送一下就完成了同步

## 10、删除远程库

如果添加的时候地址写错了，或者就是想删除远程库，可以用 `git remote rm <name>`命令。使用前，建议先用 `git remote -v`查看远程库信息

## 11、克隆远程仓库

要克隆一个仓库，首先必须知道仓库的地址，然后使用 `git clone`命令克隆。

## 12、创建与分支合并

一开始的时候，`master`分支是一条线，Git用 `master`指向最新的提交，再用 `HEAD`指向 `master`，就能确定当前分支，以及当前分支的提交点：

```ascii
                  HEAD
                    │
                    │
                    ▼
                 master
                    │
                    │
                    ▼
┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘
```

每次提交，`master`分支都会向前移动一步，这样，随着你不断提交，`master`分支的线也越来越长。

当我们创建新的分支，例如 `dev`时，Git新建了一个指针叫 `dev`，指向 `master`相同的提交，再把 `HEAD`指向 `dev`，就表示当前分支在 `dev`上：

```ascii
                 master
                    │
                    │
                    ▼
┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘
                    ▲
                    │
                    │
                   dev
                    ▲
                    │
                    │
                  HEAD
```

你看，Git创建一个分支很快，因为除了增加一个 `dev`指针，改改 `HEAD`的指向，工作区的文件都没有任何变化！

不过，从现在开始，对工作区的修改和提交就是针对 `dev`分支了，比如新提交一次后，`dev`指针往前移动一步，而 `master`指针不变：

```ascii
                 master
                    │
                    │
                    ▼
┌───┐    ┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘    └───┘
                             ▲
                             │
                             │
                            dev
                             ▲
                             │
                             │
                           HEAD
```

假如我们在 `dev`上的工作完成了，就可以把 `dev`合并到 `master`上。Git怎么合并呢？最简单的方法，就是直接把 `master`指向 `dev`的当前提交，就完成了合并：

```ascii
                           HEAD
                             │
                             │
                             ▼
                          master
                             │
                             │
                             ▼
┌───┐    ┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘    └───┘
                             ▲
                             │
                             │
                            dev
```

所以Git合并分支也很快！就改改指针，工作区内容也不变！

合并完分支后，甚至可以删除 `dev`分支。删除 `dev`分支就是把 `dev`指针给删掉，删掉后，我们就剩下了一条 `master`分支：

```ascii
                           HEAD
                             │
                             │
                             ▼
                          master
                             │
                             │
                             ▼
┌───┐    ┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘    └───┘
```

Git鼓励大量使用分支：

查看分支：`git branch`

创建分支：`git branch <name>`

切换分支：`git checkout <name>`或者 `git switch <name> 切换分支这个动作，用   git  switch` `更科学`

创建+切换分支：`git checkout -b <name>`或者 `git switch -c <name>`

注意：

`git checkout`命令加上 `-b`参数表示创建并切换，相当于以下两条命令：

```
$ git branch dev
$ git checkout dev
```

合并某分支到当前分支：`git merge <name>  git merge命令用于合并指定分支到当前分支。`

删除分支：`git branch -d <name>`

## 13、解决冲突

分支冲突

当Git无法自动合并分支时，就必须首先解决冲突。解决冲突后，再提交，合并完成。

解决冲突就是把Git合并失败的文件手动编辑为我们希望的内容，再提交。

用 `git log --graph`命令可以看到分支合并图。

## 14、分支策略



在实际开发中，我们应该按照几个基本原则进行分支管理：

首先，`master`分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；

那在哪干活呢？干活都在 `dev`分支上，也就是说，`dev`分支是不稳定的，到某个时候，比如1.0版本发布时，再把 `dev`分支合并到 `master`上，在 `master`分支发布1.0版本；

你和你的小伙伴们每个人都在 `dev`分支上干活，每个人都有自己的分支，时不时地往 `dev`分支上合并就可以了。

所以，团队合作的分支看起来就像这样：

![git-br-policy](https://www.liaoxuefeng.com/files/attachments/919023260793600/0)

合并分支时，加上 `--no-ff`参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并，而 `fast forward`合并就看不出来曾经做过合并。

## 15、创建标签


* 命令 `git tag <tagname>`用于新建一个标签，默认为 `HEAD`，也可以指定一个commit id；
* 命令 `git tag -a <tagname> -m "blablabla..."`可以指定标签信息；
* 命令 `git tag`可以查看所有标签。


* 命令 `git push origin <tagname>`可以推送一个本地标签；
* 命令 `git push origin --tags`可以推送全部未推送过的本地标签；
* 命令 `git tag -d <tagname>`可以删除一个本地标签；
* 命令 `git push origin :refs/tags/<tagname>`可以删除一个远程标签。

测试标签回滚
