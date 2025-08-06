# Solution to Prof. Zhang Peng's Lecture

Q1: Please explain each term in the following formular:  

$$
I^{ch}(v^*, \theta) = B(v^*, T_s)\tau_s(v^*, p_s, \theta) + \int_{\ln p_s}^{\ln p_\infty} B(v^*, T(p)) \frac{\partial \tau(v^*, p, \theta)}{\partial \ln p} d(\ln p)
$$

A1 大气辐射传播方程（Radiative Transfer Equation, RTE）中各部分的意意义为：

- $I^{ch}(v^*, \theta)$: 卫星传感器在大气层顶（TOA）观测到的辐射亮度（Channel Radiance）
  - $ch$: （通常代表）特定的仪器通道（Channel），每个通道对特定频率范围的辐射敏感度不同。
  - $v^*$: 波频
  - $\theta$：观测角度，卫星观测天顶角（Satellite Viewing Zenith Angle）。
  
- $B(v^*, T_s)\tau_s(v^*, p_s, \theta)$: 地表提供的辐射亮度
  - $B(v^*, T_s)$: 普朗克黑体辐射函数（Planck Function）, 将地表认为是黑体，在温度为 $T$ 时在波长 $v^*$ 处的辐射亮度。
  - $\tau_s(v^*, p_s, \theta)$：地面反射率（Surface Reflectance)，气压为 $p_s$ 和观测角度 $\theta$ 时，地表对于波长为 $v^*$ 的波的反射系数。$p_s$ 是地表气压（Surface Pressure）。
- $\int_{\ln p_s}^{\ln p_\infty} B(v^*, T(p)) \dfrac{\partial \tau(v^*, p, \theta)}{\partial \ln p} d(\ln p)$: 大气路径辐射贡献，对流层从地面（$p_s$）到顶层（$p_\infty$）各高度层的辐射贡献积分
  - $B(v^*, T(p))$：普朗克函数在气压层 $p$ 对应的大气温度 $T(p)$ 和频率 $v^*$ 下的值
  - $T(p)$: 大气温度廓线（Atmospheric Temperature Profile）。表示大气温度随气压（或高度） $p$ 的变化。
  - $\dfrac{\partial \tau(v^*, p, \theta)}{\partial \ln p}$：整层大气透过率（Total Atmospheric Transmittance）,气压为 $p$ 的大气在观测方向 $\theta$ 下对于频率 $v^*$的波的透光率。

Q2: Please briefly explain the principle of infrared remote sensing for the temperature profile and humidity profile inversion.

A2: 红外遥感反演大气温度廓线和湿度廓线的核心原理是利用不同波长的红外辐射对大气成分的吸收特性差异，结合辐射传输方程和统计学方法等，通过卫星传感器接收到的辐射值反推大气状态。  

温度廓线反演原理
-
大气中的 $\ce{CO_2}$（15 μm波段） 和 $\ce{O2}$（4.3 μm波段）存在强且分布均匀的吸收带，因其浓度在大气中高度均一，辐射信号的变化主要反映温度引起的吸收系数变化，故该波段对大气温度剖面敏感。卫星在这些波段测量的是 气自身发射的热辐射辐射强度直接取决于所在层的温度 $T(p)$。此外，窗区波段如（11 μm）大气吸收较弱，辐射主要来自地表和近地边界层，对地表温度与低层大气状态敏感，常用于地表参数反演与云检测。不同红外通道的辐射主要来自特定气压层：高频通道（如13-15 μm）：权重函数峰值高（平流层），反演高层温度；低频通道（如4-5 μm）：权重函数峰值低（对流层），反演低层温度。一般需选取多个 $\ce{CO_2}$ / $\ce{O2}$ 吸收通道，每个通道对应一个权重函数峰值高度。

湿度廓线反演原理
-
水蒸气在6–8 μm具有显著吸收，其垂直分布高度不均，辐射信号直接响应水汽浓度变化，因此适用于湿度反演。水汽浓度越高，大气透过率越低，卫星接收的辐射主要来自更高层（更冷区域）。结合大气窗区的地表辐射信息，约束低层湿度。

----

在数据处理前进行预处理。云检测与晴空像素筛选是确保反演算法有效性的前提条件。射定标是确保观测数据物理一致性的关键步骤，包含两个核心技术环节：传感器响应非线性校正与光谱响应函数匹配。辐射偏差校正是提升反演精度的核心环节，其必要性源于仪器校准误差、光谱响应不确定性、大气廓线先验误差及辐射传输模型本身的近似性。这些预处理算法存在一些局限，但共同决定了后续物理反演的可靠性与精度。  
星基红外遥感反演大气温度与湿度剖面的核心在于从卫星观测的热红外辐射中解译出大气垂直结构。现多为采用统计回归与物理反演相结合的两步式算法架构，旨在兼顾计算效率与反演精度。该架构首先通过统计回归生成初猜场，随后在物理反演阶段利用正则化方法对其进行优化，形成一种兼具经验建模效率与物理一致性约束的混合策略。传统统计回归方法因其计算高效、稳定性强，广泛应用于全球业务系统，但在湿润与多云条件下表现受限。物理反演虽能显著提升精度，但计算成本较高，难以满足实时业务需求。新兴神经网络方法（如BP与CNN）展现出优异的非线性建模能力和计算效率，特别是在空间相关性建模方面表现出显著优势。然而，其泛化能力仍受限于训练样本的时空代表性，未来需进一步优化模型结构与数据增强策略。

----

English Version

A1: The meanings of each part in the Radiative Transfer Equation (RTE) are as follows:  

- $I^{ch}(v^*, \theta)$: The radiance observed by the satellite sensor at the top of the atmosphere (TOA).
  - $ch$: A specific instrument channel, each channel has different sensitivity to radiation within a specific frequency range.
  - $v^*$: Wavelength.
  - $\theta$: Observation angle, the satellite viewing zenith angle。
- $B(v^*, T_s)\tau_s(v^*, p_s, \theta)$: The radiance provided by the surface
  - $B(v^*, T_s)$: Planck Function, which considers the surface as a blackbody and represents the radiance at wavelength $v^*$ when the temperature is $T$.
  - $\tau_s(v^*, p_s, \theta)$: Surface Reflectance, the reflection coefficient of the surface for the wave with wavelength $v^*$ when the surface pressure is $p_s$ and the observation angle is $\theta$. $p_s$ is the surface pressure.
- $\int_{\ln p_s}^{\ln p_\infty} B(v^*, T(p)) \dfrac{\partial \tau(v^*, p, \theta)}{\partial \ln p} d(\ln p)$: Atmospheric path radiance contribution, the integral of the radiance contribution at each height layer from the surface ($p_s$) to the top layer ($p_\infty$) in the troposphere.
  - $B(v^*, T(p))$: The value of the Planck function at the atmospheric temperature $T(p)$ corresponding to the pressure layer $p$ and frequency $v^*$.
  - $T(p)$: Atmospheric Temperature Profile, indicating the variation of atmospheric temperature with pressure (or height) $p$.
  - $\dfrac{\partial \tau(v^*, p, \theta)}{\partial \ln p}$: Total Atmospheric Transmittance, the transmittance of the entire atmospheric layer for the wave with frequency $v^*$ in the observation direction $\theta$ when the pressure is $p$.

A2：The core principle underlying the retrieval of atmospheric temperature and humidity profiles via infrared remote sensing is to capitalize on the disparities in the absorption characteristics of infrared radiation at various wavelengths by different atmospheric components. By integrating radiative transfer equations and statistical methodologies, it becomes possible to deduce the atmospheric state from the radiation values detected by satellite sensors.

Principle of Temperature Profile Inversion
--
In the atmosphere, $\ce{CO_2}$ (in the 15 - μm band) and $\ce{O2}$ (in the 4.3 - μm band) exhibit strong and homogeneously distributed absorption bands. Given that their concentrations remain relatively uniform throughout the atmosphere, fluctuations in the radiation signal predominantly mirror the alterations in the absorption coefficient induced by temperature variations. Consequently, these bands are highly sensitive to the atmospheric temperature profile. When the satellite measures in these bands, it detects the thermal radiation emitted by the gas itself, and the intensity of this radiation is directly proportional to the temperature $T(p)$ of the layer in which the gas resides.

Moreover, the window region, such as the 11 - μm band, experiences relatively weak atmospheric absorption. In this case, the radiation primarily emanates from the Earth's surface and the near - surface boundary layer. As a result, it is highly responsive to the surface temperature and the state of the lower atmosphere, and is frequently employed for surface parameter retrieval and cloud detection. The radiation in different infrared channels is mainly sourced from specific pressure levels: for high - frequency channels (e.g., 13 - 15 μm), the peak of the weighting function is located at a higher altitude (in the stratosphere), enabling the inversion of upper - layer temperatures; for low - frequency channels (e.g., 4 - 5 μm), the peak of the weighting function is at a lower altitude (in the troposphere), facilitating the inversion of lower - layer temperatures. Typically, multiple $\ce{CO_2}$ / $\ce{O2}$ absorption channels are selected, with each channel corresponding to a specific peak height of the weighting function.

Principle of Humidity Profile Inversion
--
Water vapor demonstrates significant absorption within the 6 - 8 μm range. Its vertical distribution is characterized by non - uniformity in altitude. The radiation signal is directly responsive to changes in water vapor concentration, rendering it suitable for humidity retrieval. As the water vapor concentration increases, the atmospheric transmittance decreases. Consequently, the radiation received by the satellite predominantly originates from higher (and colder) regions. By integrating the surface radiation information within the atmospheric window region, the humidity in the lower layers can be effectively constrained.

Preprocessing
--
Prior to data processing, preprocessing steps are essential. Cloud detection and the selection of clear - sky pixels serve as fundamental prerequisites for ensuring the effectiveness of the inversion algorithm. Radiometric calibration, a crucial step in guaranteeing the physical consistency of the observed data, encompasses two core technical aspects: the correction of sensor response non - linearity and the matching of spectral response functions. Radiometric bias correction, a central element in enhancing the inversion accuracy, is indispensable due to factors such as instrument calibration errors, uncertainties in spectral response, prior errors in atmospheric profiles, and the approximations inherent in the radiative transfer model. Although these preprocessing algorithms have certain limitations, they collectively determine the reliability and accuracy of subsequent physical inversion processes.

The essence of satellite - based infrared remote sensing for retrieving atmospheric temperature and humidity profiles lies in deciphering the vertical structure of the atmosphere from the thermal infrared radiation observed by satellites. Currently, a two - step algorithm framework that integrates statistical regression and physical inversion is commonly adopted. This approach aims to strike a balance between computational efficiency and inversion accuracy. Initially, an initial guess field is generated through statistical regression. Subsequently, during the physical inversion phase, regularization methods are employed to optimize this field, resulting in a hybrid strategy that combines the efficiency of empirical modeling with the constraints of physical consistency.

Traditional statistical regression methods, renowned for their high computational efficiency and robust stability, are extensively utilized in global operational systems. However, their performance is somewhat constrained under humid and cloudy conditions. While physical inversion can substantially enhance accuracy, its high computational cost poses challenges in meeting real - time operational demands. Emerging neural network methods, such as Backpropagation (BP) and Convolutional Neural Networks (CNN), have demonstrated remarkable non - linear modeling capabilities and computational efficiency, particularly in capturing spatial correlations. Nevertheless, their generalization ability remains limited by the spatiotemporal representativeness of the training samples. Thus, further optimization of the model structure and data augmentation strategies is imperative in the future. 

**感谢张老师精彩而令人印象深刻的讲座，让我更深入地了解了我国风云系列气象卫星和前沿的反演方法**。本人不才，如果作业解答中有误，还望多多指教。再次感谢张老师！