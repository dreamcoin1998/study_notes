[toc]

# /tmp目录自动清理

在/tmp文件夹下的文件是会被清理、删除的。主要是作业里面会自动调动tmpwatch来删除那些一段时间内没有访问的文件。

tmpwatch是一个命令或者说一个包

修改tmpwatch配置在 ```/usr/sbin/tmpwatch```

**以上是在Redhat里面**

**以下是Ubuntu**

**在Ubuntu14.04之前**，/tmp的清理工作由upstart脚本完成，/etc/init/mounted-tmp.conf，这个脚本每次在/tmp挂载的时候运行，也就是每次系统启动的时候。清理逻辑是如果/tmp文件少于所配置的变量$TMPTIME天，将会被删除。$TMPTIME是一个定义在/etc/default/rcS文件里面的变量。

**Ubuntu 14.04**

由tmpreader脚本运行删除，日常被```/etc/cron.daily```脚本调用，可以在```/etc/default/rcS```中和```/etc/tmpreader.conf```中配置。

**Ubuntu 16.10**

```/etc/default/rcS```不再起作用，tmp中的文件将通过重新启动来删除，不再使用tmpreader。

在```/etc/tmpfiles.d/```文件夹下面由一个配置文件来控制是否删除 /tmp 。

格式大致如下：

```shell
#/etc/tmpfiles.d/tmp.conf

d /tmp 1777 root root 20d
```

通过这样的设置，即使不重新引导系统，文件清理仍可运行。

























