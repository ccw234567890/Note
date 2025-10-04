
# 《电路分析与设计》Lecture 4（逐页精读讲解，无目录）

---

## 第 1 页：封面与课程说明
![[Lecture 4.pdf#page=1]]

- 课程：Circuit Analysis and Design（2025/2026 学年）。
- 讲师与邮箱列出；学术诚信提示。
- 本讲核心：**信号函数复习**（$\delta, u, r, e^{-at}$，rect/tri），**等效电阻**，**分压法**，**分流法**，以及要点总结。

---

## 第 2 页：议程（学习路径与目标）
![[Lecture 4.pdf#page=2]]

- 先复习连续时间信号的基本“基元”，再进入电阻网络的化简与比例法（分压/分流）。
- **学习策略**：看图→写式→**化简网络**→**分压/分流**→**回代展开**→功率守恒自检。

---

## 第 3 页：斜坡函数 $r(t)$（定义/性质/直觉）
![[Lecture 4.pdf#page=3]]

**定义**
$$
r(t) = t\,u(t)
$$

**与阶跃的关系**
$$
r(t)=\int_{-\infty}^{t}u(\lambda)\,d\lambda,\qquad \frac{d}{dt}r(t)=u(t)
$$

**直觉**  
把“分段线性”波形拆成若干**移位斜坡** $(t-a)u(t-a)$ 的叠加；每个“开启点”会改变当前**斜率**。

---

## 第 4 页：例 1.9（用移位斜坡合成分段线性）
![[Lecture 4.pdf#page=4]]

**题目**
$$
f(t)=2t\,u(t)-4(t-1)u(t-1)+4(t-3)u(t-3)-4(t-5)u(t-5)+2(t-6)u(t-6)
$$

**区间斜率**
- $t<0$: $f=0$
- $0\le t<1$: 斜率 $2$
- $1\le t<3$: 斜率 $-2$
- $3\le t<5$: 斜率 $2$
- $5\le t<6$: 斜率 $-2$
- $t\ge 6$: $f=0$

**讲解**  
把每一项看成“从 $t=a$ 起加入一条固定斜率的直线”，累计得到目标折线。

---

## 第 5 页：课堂练习（从图形反推公式）
![[Lecture 4.pdf#page=5]]

**步骤法**
1. 找出所有折点 $a_i$；  
2. 为每个折点写 $\pm(t-a_i)u(t-a_i)$；  
3. 令区间斜率=当前**已开启**项系数之和；  
4. 如需整体抬升/下移，加常数项修正。

---

## 第 6 页：指数衰减与阻尼振荡
![[Lecture 4.pdf#page=6]]

**单边指数**
$$
f(t)=e^{-a t}u(t),\quad a>0
$$

**阻尼余弦/正弦**
$$
f(t)=e^{-a t}\cos(bt)\,u(t),\qquad f(t)=e^{-a t}\sin(bt)\,u(t)\quad (a>0)
$$

**提示**：$a$ 控制包络衰减；$b$ 控制振荡频率。常见于 RLC 暂态与滤波器响应。

---

## 第 7 页：矩形/三角脉冲（rect/tri）
![[Lecture 4.pdf#page=7]]

**定义**
$$
\text{矩形：}\quad f(t)=A\,\mathrm{rect}\!\Big(\frac{t}{\tau}\Big)
$$
$$
\text{三角：}\quad f(t)=A\,\mathrm{tri}\!\Big(\frac{t}{\tau}\Big)
$$

**要领**：中心在 $t=0$；通过**平移/缩放/加权**叠加，拼出复杂脉冲序列。

---

## 第 8 页：例 1.11（多矩形叠加）
![[Lecture 4.pdf#page=8]]

**讲义给出的结构（解读）**
- 3 个矩形脉冲：中心分别在 $t=-1,1,3.5$，高度 $1,3,-2$，宽度 $2,2,3$。  
- 负系数代表“挖去”一段矩形；线性叠加得到目标波形。

---

## 第 9 页：例 1.12（多三角叠加）
![[Lecture 4.pdf#page=9]]

**思路**  
把三角看作“上升斜坡 + 下降斜坡”，可直接套用第 3–5 页的**移位斜坡分解**法；三个等底三角（正、负、正）在 $t=-2,0,2$ 处对称分布，叠加后中部被“削低”。

---

## 第 10 页：题 2.39（等效电阻）
![[Lecture 4.pdf#page=10]]

**策略**
1. 先识别**纯并联/纯串联**子块并化简；  
2. 桥式或对称网络，优先找“好算对”（相等值、明显串/并顺序）；  
3. 求端口 $R_\text{eq}$ 后再回代求流/压/功率；用功率守恒作终检。

---

## 第 11–13 页：例 2.12（等效 + 电压/电流/功率守恒）
![[Lecture 4.pdf#page=12]]
![[Lecture 4.pdf#page=13]]

**关键计算（讲义给出）**
- $R_a=R_3\parallel R_4=4\,\text{k}\Omega$；$R_\text{eq}=R_1+R_2+R_a=9\,\text{k}\Omega$  
- $I=\dfrac{V_s}{R_\text{eq}}=1\,\text{mA}$，$V_1=2\,\text{V}$，$V_2=3\,\text{V}$，$V_3=4\,\text{V}$  
- $I_1=0.8\,\text{mA}$，$I_2=0.2\,\text{mA}$  
- 功率：$P_{R1}=2\,\text{mW}$，$P_{R2}=3\,\text{mW}$，$P_{R3}=3.2\,\text{mW}$，$P_{R4}=0.8\,\text{mW}$；源释放 $9\,\text{mW}$，电阻吸收合计 $9\,\text{mW}$。

**要点**：**等效→求总量→回代拆分**，并用 $\sum P_\text{元件}=P_\text{源}$ 检查。

---

## 第 14 页：复杂混合等效（示例 2.14 提示）
![[Lecture 4.pdf#page=14]]

- 按“**先并后串**”减少分支：如 $R_8=R_1\parallel R_2$，$R_9=R_3+R_8$，$R_a=R_4\parallel R_9$ 等；  
- 得 $R_\text{eq}=R_a\parallel R_b$ 后，利用节点电压求各支电流；讲义给出一系列中间值可核对。

---

## 第 15 页：分压法（两电阻串联）
![[Lecture 4.pdf#page=15]]

**电流**
$$
I=\frac{V_s}{R_1+R_2}
$$

**分压**
$$
V_{R1}=V_s\frac{R_1}{R_1+R_2},\qquad
V_{R2}=V_s\frac{R_2}{R_1+R_2}
$$

> 串联**同流**，电压按阻值比例分配。

---

## 第 16 页：分压法（$n$ 个电阻串联）
![[Lecture 4.pdf#page=16]]

**电流**
$$
I=\frac{V_s}{\sum_{k=1}^n R_k}
$$

**第 $i$ 个电阻电压**
$$
V_i=V_s\frac{R_i}{\sum_{k=1}^n R_k}
$$

---

## 第 17–18 页：题 2.47 与解
![[Lecture 4.pdf#page=17]]
![[Lecture 4.pdf#page=18]]

**直接代入分压式（讲义数据）**
$$
V_1=V_s\frac{R_1}{R_1+R_2}=5\,\text{V},\qquad
V_2=V_s\frac{R_2}{R_1+R_2}=15\,\text{V}
$$

**技巧**：遇到整比（如 $1:3$），先心算再精算，能快速排除选项。

---

## 第 19–20 页：分压综合（先等效再分压）
![[Lecture 4.pdf#page=19]]
![[Lecture 4.pdf#page=20]]

**示例等效（讲义给出）**  
$R_a=R_1\parallel R_2=1.2\,\text{k}\Omega,\; R_b=R_3\parallel R_4=1.5\,\text{k}\Omega,\;
R_c=R_5\parallel R_6\approx 2.3\,\text{k}\Omega$

**节点电压（分压）**  
$V_a=2.4\,\text{V},\;V_b=3.0\,\text{V},\;V_c=4.6\,\text{V}$

**套路**：把并支**吸收为主链**→主链一次分压出所有关键节点电压→回代到原并支求支路电流/功率。

---

## 第 21–22 页：题 2.52 与详细解
![[Lecture 4.pdf#page=21]]
![[Lecture 4.pdf#page=22]]

**化简顺序（讲义）**
- $R_a=R_7\parallel R_6+R_5=9\,\text{k}\Omega$  
- $R_b=R_a\parallel R_4+R_3=10\,\text{k}\Omega$  
- $R_\text{eq}=R_b\parallel R_2+R_1=12\,\text{k}\Omega$

**逐级分压**
$$
V_1=16\,\text{V},\qquad V_2=9.6\,\text{V},\qquad V_3\approx 4.267\,\text{V}
$$

**要点**：混合层**内并外串**时，始终保持“**源—地**”分压视角，防止分母写错。

---

## 第 23–25 页：例 2.15 / 2.16（串并组合 + 分压）
![[Lecture 4.pdf#page=23]]
![[Lecture 4.pdf#page=24]]
![[Lecture 4.pdf#page=25]]

**例 2.15（讲义结果）**  
$R_a=R_2\parallel R_3=2.4\,\text{k}\Omega$；主链分压：
$V_1=2.4\,\text{V},\;V_2=4.8\,\text{V},\;V_3=6.8\,\text{V}$

**例 2.16（讲义步骤）**  
$R_a=R_1\parallel(R_2+R_3)=18.2\,\text{k}\Omega,\; R_b=R_4\parallel(R_5+R_6)=22.8\,\text{k}\Omega$；  
分压后回代可得到 $11.4\,\text{V}, 9.1\,\text{V}, 6\,\text{V}$ 等中间节点值自检。

---

## 第 26 页：分流法（两电阻并联）
![[Lecture 4.pdf#page=26]]

**等效**
$$
R_\parallel=\frac{R_1R_2}{R_1+R_2}
$$

**同压（由源或上层等效确定）**
$$
V=I_s\,R_\parallel
$$

**分流（总电流 $I_s$ 进入并联）**
$$
I_1=I_s\frac{R_2}{R_1+R_2},\qquad
I_2=I_s\frac{R_1}{R_1+R_2}
$$

> 电流按**导纳**（$G=1/R$）比例分配，阻越小电流越大。

---

## 第 27–31 页：题 2.58 / 分流（$n$ 支）/ 题 2.59 / 综合
![[Lecture 4.pdf#page=28]]
![[Lecture 4.pdf#page=29]]
![[Lecture 4.pdf#page=30]]
![[Lecture 4.pdf#page=31]]

**题 2.58（讲义数值）**  
$I_s=10\text{ mA}$，代入两支分流式得：$I_1=6\text{ mA},\ I_2=4\text{ mA}$

**$n$ 支并联分流**
$$
I_i = I_s\,\frac{\tfrac{1}{R_i}}{\sum_{k=1}^{n}\tfrac{1}{R_k}}=I_s\,\frac{G_i}{\sum_k G_k}
$$

**题 2.59（讲义数值）**  
按上式得 $I_1/I_2/I_3=12/8/6\text{ mA}$（示例参数）。

**综合题（第 31 页）**  
先求等效与总电流，再**逐层回代**分配到各支；遇串并层叠，先把同层并联缩为块再向下分流。

---

## 第 32–34 页：例 2.17（多支路分流）
![[Lecture 4.pdf#page=32]]
![[Lecture 4.pdf#page=33]]
![[Lecture 4.pdf#page=34]]

**方法**  
- 先由源与上层等效确定并层节点压 $V$，再用 $I_k=\dfrac{V}{R_k}$ 一次得到全部支流。  
- 讲义给出若干电流占比（如 $I_5=4/6/12\text{ mA}$ 选项），可与分流比例快速对照。

---

## 第 35–37 页：例 2.18（层级并联 + 迭代分流）
![[Lecture 4.pdf#page=35]]
![[Lecture 4.pdf#page=36]]
![[Lecture 4.pdf#page=37]]

**流程**  
1) 把下层两两并联合成 $R_a,R_b$；  
2) 与上层做并/串合并得顶层结构；  
3) 顶层先分流，再把分到 $R_a/R_b$ 的电流**向下**按并联比例继续分配；  
4) 多处中间数（如 $7.5\,\text{mA}, 3\,\text{mA}, 2\,\text{mA}$ 等）用于自检。

---

## 第 38–41 页：周结（Weeks 2–3）
![[Lecture 4.pdf#page=38]]
![[Lecture 4.pdf#page=39]]
![[Lecture 4.pdf#page=40]]
![[Lecture 4.pdf#page=41]]

**电阻/电导/欧姆定律**
$$
V=IR,\qquad I=\frac{V}{R},\qquad R=\frac{V}{I},\qquad G=\frac{1}{R}
$$

**KCL（节点电流定律）**
- 进入某节点的电流代数和=流出代数和；或写作“进入之和为 0 / 流出之和为 0”。

**KVL（回路电压定律）**
- 任一闭合回路电压代数和为 0。

**等效电阻**
$$
\text{串联: }R_\text{eq}=\sum_i R_i,\qquad
\text{并联(两支): }R_\text{eq}=\frac{R_1R_2}{R_1+R_2},\qquad
\text{并联(}n\text{支): }\frac{1}{R_\text{eq}}=\sum_i\frac{1}{R_i}
$$

**分压法**
$$
V_i=V_s\frac{R_i}{\sum R_k}
$$

**分流法**
$$
I_i=I_s\frac{1/R_i}{\sum_k 1/R_k}=I_s\frac{G_i}{\sum_k G_k}
$$

---

## 第 42 页：下次预告


- 预计将把**化简+比例法则**与**网络定理**（叠加、戴维南、诺顿等）打通，提升复杂网络求解效率。
