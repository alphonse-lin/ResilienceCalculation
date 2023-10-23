# Simulation
- 基于asc生成淹没轨迹,0,1矩阵集
- 执行先淹先开的状态
- 一旦确定后续开始有0出现了，那么过2个小时后，打开该部分道路

## Basic Inundate Rules
我现在有一个淹没规则，如果知道这条道路的水位深度大于0.3米，该道路过了600s之后，容量比例变为0。当知道不再降雨之后（该值可求得，同时该事件与淹没深度成正相关，即降雨时长+淹没深度*600s），该道路容量比例变成0.5。再过1200s之后，容量变为1。同时，由于这些道路会有一个空间结构的影响，因此需要 考虑道路的空间结构性质 ，

## Variables
$T$: The time rain starts\
$Dl$：The depth of the water level that cannot be passed. \
$Bt$：The time required to open up or close roads\
$Bc$：The time required to recover the capacity of roads\
$Tc$：The temporary capacity value of roads\
$Rst$：The duration of rainfall at time $t$. \
$Ret$：The duration of rainfall at time $t$. \
$H(t)$：The depth of the road water level at time $t$. \
$Cr(t)$：The capacity ratio of the road at time $t$. \
$B(v)$：The influencing factor of the spatial structure of the road at node $v$.

## Hypothesis
### Static Strategy
**Main**: First Close, First Open-Up\
For $CapacityRatio$ of Road Based on $t$ \
$Dl=0.3 $ \
$Bt=600 $ \
$Bc=1200 $ \
$Tc=0.5 $ \
需要解释T和depth的关系\
$Cr(t) = 1, \quad H(t) <= Dl \quad and \quad t<=T$\
$Cr(t) = 0, \quad H(t) > Dl \quad and \quad t < R(t) + H(t)$ \
$Cr(t) = Tc / Bt * (t - R(t) - H(t) * Bt), \quad t \in [R(t) + H(t) * Bt, R(t) + H(t) * Bt + Bc]$ \
$Cr(t) = Tc + (1-Tc) / Bt * (t - R(t) - H(t) * Bt - Bt), \quad t \in [R(t) + H(t) * Bt + Bc, R(t) + H(t) * Bt + 2Bc]$ 


For $Travel Time$ or $People Stuck on Road$ Based on $t$ and $Capacity$ \
每小时只能修100条，那如何选择这100条路就变得很重要
是按照他们被关闭的 时间修，还是按照他们的



### Dynamic Strategy
**Main**: close and open up based on dynamic importance
$Dl=0.3 $ \
$Bt=600 $ \
$Bc=1200 $ \
$Tc=0.5 $ \
缺一个\
$Cr(t) = 0, \quad H(t) > Dl \quad and \quad t < R(t) + H(t) * Bt$ \
$Cr(t) = Tc / Bt * (t - R(t) - H(t) * Bt), \quad t \in [R(t) + H(t) * Bt, R(t) + H(t) * Bt + Bc]$ \
$Cr(t) = Tc + (1-Tc) / Bt * (t - R(t) - H(t) * Bt - Bt), \quad t \in [R(t) + H(t) * Bt + Bc, R(t) + H(t) * Bt + 2Bc]$ 
$B(v) = \sum_{s,t\in v} \frac{σ(s,t|v)}{σ(s,t)}$

$dQ_e/dt = Σ_od [F_od(e) - Q_e/C_e(d(x, t))]$

为了更简洁地表达 \(Cr_{t}\) 和 \(Cr_{t-1}\) 之间的关系，我们首先需要使用给定的速度公式来对每一个时刻的速度进行展开。

已知:
$[ v_{t} = 0.0009 \times (\theta \times w_{t-1})^2 - 0.5529 \times \theta \times w_{t-1} + 86.9448 ]$

\[ v_{t-1} = 0.0009 \times w_{t-1}^2 - 0.5529 \times w_{t-1} + 86.9448 \]

根据 \(Cr = \frac{L}{v}\) ，我们有:

\[ Cr_{t} = \frac{L}{0.0009 \times (\theta \times w_{t-1})^2 - 0.5529 \times \theta \times w_{t-1} + 86.9448} \]

\[ Cr_{t-1} = \frac{L}{0.0009 \times w_{t-1}^2 - 0.5529 \times w_{t-1} + 86.9448} \]

要表示 \(Cr_{t}\) 和 \(Cr_{t-1}\) 之间的关系，我们可以整理上述等式，将它们组合到一个公式中。如果需要找到它们之间的比例关系，可以建立以下公式:

\[ \frac{Cr_{t}}{Cr_{t-1}} = \frac{\frac{L}{0.0009 \times (\theta \times w_{t-1})^2 - 0.5529 \times \theta \times w_{t-1} + 86.9448}}{\frac{L}{0.0009 \times w_{t-1}^2 - 0.5529 \times w_{t-1} + 86.9448}} \]

进一步简化，L将会被抵消掉，你会得到:

\[ \frac{Cr_{t}}{Cr_{t-1}} = \frac{0.0009 \times w_{t-1}^2 - 0.5529 \times w_{t-1} + 86.9448}{0.0009 \times (\theta \times w_{t-1})^2 - 0.5529 \times \theta \times w_{t-1} + 86.9448} \]

这个比值公式清晰地展示了 \(Cr_{t}\) 和 \(Cr_{t-1}\) 之间的关系，具体依赖于 \(w_{t-1}\) 和 \(\theta\)。


| Author(s)                                     | Metric Name & Description |
|-----------------------------------------------|---------------------------|
| Twumasi-Boakye and Sobanjo [103]              | Degradation of system quality over time. Measures system resilience based on the ability to reduce failure probabilities, consequences, and recovery time. |
| Liao et al. [101]                             | Time-dependent ratio of recovery to loss. This indicator treats resilience as a dynamic property of systems and is consistent with the original definition of resilience, i.e. the ability to bounce back. |
| Chen and Miller-Hooks [56]                    | Expected fraction of demand satisfied in post-disaster network using specific recovery costs. It considers the resilience of freight transportation systems with stochastic arc capacities. |
| Bocchini and Frangopol [18], [21]             | Uses degradation of system quality over time for road networks, optimizing the restoration sequence of damaged bridges. |
| Adjetey-Bahun et al. [69]                     | Used the degradation metric for railway systems, with passenger load and passenger delay as measures of system quality. |
| Cox et al. [65]                               | Definition of economic resilience with a resilience indicator based on the maximum and expected percentage change in system performance due to disasters. |
| Omer et al. [83], Faturechi and Miller-Hooks [26], Bhavathrathan and Patil [29] | System travel time as an indicator of performance with three similar resilience metrics. |
| Chan and Schofer [71]                         | Lost Service Days (LSD) to measure rail transit resilience, considering revenue vehicles miles per day under normal and disrupted states. |
| Vugrin et al. [80]                            | Metric considering both the ability to maintain function under disruption and the time/resources required for recovery. It accounts for traffic flows, costs on links, unsatisfied traffic demand, repair tasks, and associated costs. |