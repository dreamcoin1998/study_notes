[toc]

# 综述

CI/CD是通过在应用开发阶段引入自动化来频繁向客户交付应用的方法。

CI/CD的核心概念是**持续集成、持续交付、持续部署**

# CI是什么

**CI**始终指持续集成，属于开发人员的自动化流程，成功的CI意味着应用代码会成功构建、测试并合并到共享存储库中。

*一旦开发人员对应用所做的更改被合并，系统就会自动通过构建应用并运行不同级别的自动化测试来验证这些更改，确保这些更改没有对应用造成破坏，如果自动化测试发现现有代码和新代码发生冲突，CI就可以更加轻松的快速修复这些错误。*

CI工作流的变化取决于开发工具、编程语言、项目和许多其他因素，通常包含以下步骤：

- 推送到代码存储库
- 静态分析
  - 确保代码没有可能的错误并符合标准的格式和样式
- 部署前测试
- 打包和部署到测试环境
- 部署后测试

*在网易的实习项目当中，在项目发布中，所做的实际上是CI的流程。*

# CD是什么

**CD**指的是持续交付和/或持续部署

- 持续交付：*通常是指开发人员对应用的更改会自动测试并上传到共享存储库中，然后由运维团队将代码发布到生产环境中*
  - 持续交付的目标是拥有一个可随时部署到生产环境的代码库，在流程结束时，运维团队可以快速、轻松地将应用部署到生产环境中
- 持续部署：*自动将开发人员的更改从存储库发布到生产环境中*
  - 持续部署可以将应用发布到生产环境中

![](https://www.redhat.com/cms/managed-files/ci-cd-flow-mobile_0.png)

**总而言之，CI/CD就是指应用开发过程中的高度持续自动化和持续监控**

