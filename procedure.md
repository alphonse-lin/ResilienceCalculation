# Running Procedures

## Run HiPIMS
- [construct basic files](./001_floodsim/prepare.py)
- [construct config](./001_floodsim/read.py)

## Run Matsim
- 第1步：路网转换
[xml to geojson](./001_floodsim/networkXML2Geojson.py)

- 第2步：生成连续淹没图
[generate continuous flood map](./001_floodsim/createSeqInundateMap.py)

- 第3步：生成连续道路调控事件
[generate events](./001_floodsim/generateSeqEvent.py)

- 第4步：重构数据
[reconstruct data](./001_floodsim/resetScore.py)

- 第4.1步：运行matsim
[run java]()

## Analyze Results
- 第5步：整合matsim结果
[integrate matsim result](./001_floodsim/sotrMatsimResult.py)

- 第6步：对于输出的count_excel进行整合
[generate time series](./001_floodsim/sortOutputExcel.py)

- 第6.1步：读取link stats 文件
[read link stats](./001_floodsim/readStat.py)

- 第6.1步：按照时间间隔，提取车辆数目（读取xml文件）
[extract vehicle number](./001_floodsim/matsimAnalysis.py)

- 第7步：整合 choice 数值
[merge choice](./001_floodsim/dupScore.py)

- 第8步：组合matsim和choice的数据
[combine matsim and choice](./001_floodsim/combineMatsimAndChoice.py)

- 第8.1步：对于输出的count_excel进行整合
[merge time-interval link_count with choice](./001_floodsim/matsimIntersect.py)

- 第9步：对于输出的count_excel进行整合,然后用dtw进行pattern匹配
[merge count and dtw](./001_floodsim/dtwMatching.py)

- 第10步：添加risk flag
[add risk flag](./001_floodsim/addRiskFlag2.py)

- 第11步：与常规数据进行对比
[compare with baseline](./001_floodsim/matsimWithSelectedPattern.py)

## Extra
- 生成时间序列
[Generate time series](./001_floodsim/generateTimeSeries.py)

- 把秒转换成具体时刻
[Convert seconds to time](./001_floodsim/convertSecondsToTime.py)

- 给列表添加ID
[Add ID to list](./001_floodsim/attachValue.py)

- 测试生成事件
[Generate events](./001_floodsim/generateEvent.py)

- 测试生成淹没图
[Generate continuous flood map](./001_floodsim/createInundateMap.py)