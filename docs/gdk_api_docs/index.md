---
title: What is GDK for?
order: 1
---

GDK（Genie Development Kit）是为Genie机器人及其相关产品提供的开发工具包。它的主要作用是为用户和开发者提供丰富的二次开发接口，方便用户根据自身需求快速实现机器人在移动、感知、操作等方面的定制化功能。

通过GDK，用户可以：

- 快速集成和调用机器人的底层控制能力，如运动控制、传感器数据获取、任务调度等；
- 利用C++、Python、ROS2等多种主流开发语言进行开发，满足不同开发者的技术栈需求；
- 实现机器人与外部系统的高效对接，比如与VR、仿真、云端等模块的集成；
- 便捷地进行算法验证、功能扩展和系统集成，加速产品落地和迭代。

GDK适用于教育、科研、工业、服务等多种场景，是机器人开发者和行业用户提升开发效率、降低开发门槛的重要工具。

### 示例场景

以下是GDK可能用到的一些典型场景：

- **教育与科研**：高校、研究机构可利用GDK快速搭建机器人实验平台，进行算法验证、课程教学、学术研究等。
- **工业自动化**：在工厂、仓储等场景下，开发者可基于GDK实现机器人自动搬运、巡检、分拣等功能。
- **服务机器人**：如酒店、医院、商场等公共场所的服务机器人，通过GDK实现定制化的人机交互、导航、物品递送等。
- **智能家居**：家庭服务机器人可通过GDK集成语音、视觉等多模态感知，实现智能清扫、安防巡逻等。
- **多机器人协作**：GDK支持多机器人系统的开发，便于实现机器人之间的协同作业、信息共享与任务分配。
- **感知与导航算法开发**：开发者可基于GDK快速接入传感器数据，进行SLAM、目标检测、路径规划等算法的开发与测试。
- **远程运维与监控**：通过GDK实现机器人远程控制、状态监测、故障诊断和远程升级。
- **二次开发与系统集成**：企业或个人可基于GDK进行功能扩展，将机器人与云平台、物联网、第三方系统无缝集成。

这些场景仅为部分示例，GDK的灵活性和开放性使其能够适应更多创新应用场景，助力机器人行业的快速发展。

---

<div id="version-info" style="font-size: 0.85rem; color: var(--md-default-fg-color--lighter); padding-top: 1rem; border-top: 1px solid var(--md-default-fg-color--lightest);">
<script>
fetch('/version.txt')
  .then(r => r.text())
  .then(text => {
    const info = {};
    text.split(/\r?\n/).forEach(line => {
      const trimmed = line.trim();
      if (trimmed && trimmed.includes(':')) {
        const parts = trimmed.split(':');
        if (parts.length >= 2) {
          const key = parts[0].trim();
          const value = parts.slice(1).join(':').trim();
          if (key && value) {
            info[key] = value;
          }
        }
      }
    });
    const version = info['Version'] || info['version'];
    const buildTime = info['BuildTime'] || info['buildtime'];
    if (version) {
      let html = '<strong>文档版本:</strong> ' + version;
      if (buildTime) {
        html += ' | <strong>构建时间:</strong> ' + buildTime;
      }
      document.getElementById('version-info').innerHTML = html;
    }
  })
  .catch(() => {});
</script>
</div>