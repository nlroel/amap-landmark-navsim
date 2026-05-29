# Landmark NavSim 实施计划

本文档将项目拆分为 10 个可验收阶段。每个 Phase 都包含目标、需要新增或修改的模块路径、CLI 行为、测试文件与验收命令，便于按阶段实现、测试与评审。

## Phase 1：项目骨架

### 目标

- 建立 Python 包的基础目录结构与工程配置。
- 明确源码、测试、模拟数据和运行产物的默认位置。
- 配置基础开发工具入口，为后续模块迭代提供统一约束。

### 需要新增/修改的模块路径

- `pyproject.toml`：定义项目元信息、依赖、Typer CLI entry point、pytest、ruff、mypy 配置。
- `src/landmark_nav/__init__.py`：包初始化与版本号。
- `src/landmark_nav/cli.py`：预留 Typer app。
- `tests/`：测试目录骨架与共享 fixtures。
- `data/mock/`：模拟路线、POI、逆地理编码响应数据。
- `outputs/.gitkeep`：保留输出目录。

### CLI 行为

- `landmark-nav --help` 能显示 Typer 应用帮助信息。
- 暂不提供完整业务命令，仅保留后续 `run-mock` 命令挂载位置。

### 测试文件

- `tests/test_cli.py`：验证 CLI help 正常返回。
- `tests/conftest.py`：提供临时目录、mock data 路径等 fixtures。

### 验收命令

- `python -m pytest`
- `ruff check .`
- `mypy src`

## Phase 2：`AmapClient` 与 `MockAmapClient`

### 目标

- 抽象高德地图客户端接口，屏蔽真实 API 与 mock 数据源差异。
- 覆盖路线规划、POI 周边搜索、逆地理编码三类能力。
- 为离线开发和测试提供稳定的 `MockAmapClient`。

### 需要新增/修改的模块路径

- `src/landmark_nav/clients/base.py`：定义 `AmapClientProtocol` 或抽象基类。
- `src/landmark_nav/clients/amap.py`：实现真实 `AmapClient`，封装请求参数、鉴权、错误处理。
- `src/landmark_nav/clients/mock.py`：实现 `MockAmapClient`，从 `data/mock/` 读取响应。
- `src/landmark_nav/clients/errors.py`：定义 API、网络、数据格式相关异常。
- `data/mock/routes/*.json`：路线规划 mock 响应。
- `data/mock/pois/*.json`：POI 周边搜索 mock 响应。
- `data/mock/regeocode/*.json`：逆地理编码 mock 响应。

### CLI 行为

- `landmark-nav debug route --mock --origin ... --destination ...` 可打印 mock 路线摘要。
- `landmark-nav debug pois --mock --location ...` 可打印指定位置周边 POI 数量。
- `landmark-nav debug regeocode --mock --location ...` 可打印逆地理编码结果。

### 测试文件

- `tests/test_clients_mock.py`：验证 mock 客户端读取三类数据并返回统一结构。
- `tests/test_clients_amap.py`：使用请求 mock 验证真实客户端参数、错误处理与响应解析。

### 验收命令

- `python -m pytest tests/test_clients_mock.py tests/test_clients_amap.py`
- `ruff check src/landmark_nav/clients tests/test_clients_mock.py tests/test_clients_amap.py`
- `mypy src/landmark_nav/clients`

## Phase 3：路线解析与 Pydantic 模型

### 目标

- 将高德路线响应解析为内部强类型模型。
- 定义 route、step、polyline、maneuver 等核心数据结构。
- 统一经纬度、距离、耗时、道路名称和导航指令字段。

### 需要新增/修改的模块路径

- `src/landmark_nav/models/geo.py`：定义 `LngLat`、`Polyline`、距离计算辅助字段。
- `src/landmark_nav/models/route.py`：定义 `Route`、`RouteLeg`、`RouteStep`、`ManeuverType`。
- `src/landmark_nav/parsers/route_parser.py`：把 Amap 响应转换为内部模型。
- `src/landmark_nav/parsers/polyline.py`：解析高德 polyline 字符串并校验坐标。

### CLI 行为

- `landmark-nav debug parse-route --mock --route-id ...` 输出 route、step 数量、总距离和总耗时。
- 支持 `--format json` 输出内部模型 JSON，便于人工检查。

### 测试文件

- `tests/test_models_route.py`：验证 Pydantic 模型校验、序列化与非法坐标报错。
- `tests/test_route_parser.py`：验证 mock Amap 响应可解析为内部 route 模型。
- `tests/test_polyline.py`：验证 polyline 字符串拆分、坐标顺序和边界校验。

### 验收命令

- `python -m pytest tests/test_models_route.py tests/test_route_parser.py tests/test_polyline.py`
- `ruff check src/landmark_nav/models src/landmark_nav/parsers tests/test_models_route.py tests/test_route_parser.py tests/test_polyline.py`
- `mypy src/landmark_nav/models src/landmark_nav/parsers`

## Phase 4：模拟 GPS

### 目标

- 基于路线 polyline 生成可重复的模拟轨迹点。
- 支持按固定距离或固定时间间隔采样。
- 为每个轨迹点补充速度、时间戳、所属 step 等上下文。

### 需要新增/修改的模块路径

- `src/landmark_nav/sim/gps.py`：实现轨迹采样器与 GPS 点生成逻辑。
- `src/landmark_nav/models/gps.py`：定义 `GpsPoint`、`GpsTrace`。
- `src/landmark_nav/geo/distance.py`：实现 haversine、bearing、插值等地理计算。

### CLI 行为

- `landmark-nav debug simulate-gps --mock --interval-meters 20` 输出轨迹点数量与首尾点。
- 支持 `--output outputs/trace.json` 将模拟轨迹写入 JSON 文件。

### 测试文件

- `tests/test_geo_distance.py`：验证距离、方位角和线段插值计算。
- `tests/test_gps_simulator.py`：验证轨迹点生成数量、顺序、step 归属和可重复性。

### 验收命令

- `python -m pytest tests/test_geo_distance.py tests/test_gps_simulator.py`
- `ruff check src/landmark_nav/sim src/landmark_nav/geo src/landmark_nav/models tests/test_geo_distance.py tests/test_gps_simulator.py`
- `mypy src/landmark_nav/sim src/landmark_nav/geo src/landmark_nav/models`

## Phase 5：导航事件触发

### 目标

- 根据模拟 GPS 轨迹和路线 step 识别导航事件。
- 覆盖转弯、靠左、靠右、到达、进入道路、驶出道路等事件。
- 支持提前触发距离阈值，避免事件过晚出现。

### 需要新增/修改的模块路径

- `src/landmark_nav/models/events.py`：定义 `NavigationEvent`、`EventType`、触发位置和关联 step。
- `src/landmark_nav/events/detector.py`：实现基于路线和 GPS 的事件检测器。
- `src/landmark_nav/events/rules.py`：维护 maneuver 到事件类型的规则映射。

### CLI 行为

- `landmark-nav debug detect-events --mock --trigger-distance 80` 输出事件列表。
- 支持 `--output outputs/events.json` 写出事件 JSON。

### 测试文件

- `tests/test_event_rules.py`：验证 maneuver 与事件类型映射。
- `tests/test_event_detector.py`：验证转弯、靠左、靠右、到达事件触发顺序与距离阈值。

### 验收命令

- `python -m pytest tests/test_event_rules.py tests/test_event_detector.py`
- `ruff check src/landmark_nav/events src/landmark_nav/models tests/test_event_rules.py tests/test_event_detector.py`
- `mypy src/landmark_nav/events src/landmark_nav/models`

## Phase 6：地标候选与排序

### 目标

- 从 POI 周边搜索结果中筛选导航可用地标候选。
- 结合 POI 距离、类别、名称质量、相对方向和事件类型进行打分。
- 输出每个导航事件的最佳地标及候选解释信息。

### 需要新增/修改的模块路径

- `src/landmark_nav/models/poi.py`：定义 `Poi`、`PoiCategory`、`LandmarkCandidate`。
- `src/landmark_nav/landmarks/candidates.py`：从 POI 结果生成候选。
- `src/landmark_nav/landmarks/scoring.py`：实现距离、类别、方向、名称质量打分。
- `src/landmark_nav/landmarks/ranker.py`：聚合候选并输出排序结果。

### CLI 行为

- `landmark-nav debug rank-landmarks --mock --event-id ...` 输出候选地标排序表。
- 支持 `--top-k 5` 控制展示候选数量。
- 支持 `--output outputs/landmarks.json` 写出地标候选与分数明细。

### 测试文件

- `tests/test_poi_models.py`：验证 POI 与候选模型校验。
- `tests/test_landmark_scoring.py`：验证距离、类别、方向等打分因子。
- `tests/test_landmark_ranker.py`：验证候选排序稳定性和解释字段。

### 验收命令

- `python -m pytest tests/test_poi_models.py tests/test_landmark_scoring.py tests/test_landmark_ranker.py`
- `ruff check src/landmark_nav/landmarks src/landmark_nav/models tests/test_poi_models.py tests/test_landmark_scoring.py tests/test_landmark_ranker.py`
- `mypy src/landmark_nav/landmarks src/landmark_nav/models`

## Phase 7：路标化转写

### 目标

- 将普通导航指令改写为自然、简洁的地标化语句。
- 在可用地标缺失时保留原始导航指令作为 fallback。
- 支持不同事件类型的模板化表达。

### 需要新增/修改的模块路径

- `src/landmark_nav/rewrite/templates.py`：定义转弯、靠左、靠右、到达等模板。
- `src/landmark_nav/rewrite/landmark_rewriter.py`：根据事件和地标生成路标化语句。
- `src/landmark_nav/models/instructions.py`：定义 `Instruction`、`LandmarkInstruction`。

### CLI 行为

- `landmark-nav debug rewrite --mock` 输出原始指令与地标化指令对照表。
- 支持 `--output outputs/instructions.json` 保存转写结果。

### 测试文件

- `tests/test_rewrite_templates.py`：验证不同事件类型模板渲染。
- `tests/test_landmark_rewriter.py`：验证有地标、无地标、多候选地标时的转写结果。

### 验收命令

- `python -m pytest tests/test_rewrite_templates.py tests/test_landmark_rewriter.py`
- `ruff check src/landmark_nav/rewrite src/landmark_nav/models tests/test_rewrite_templates.py tests/test_landmark_rewriter.py`
- `mypy src/landmark_nav/rewrite src/landmark_nav/models`

## Phase 8：一键 run pipeline

### 目标

- 串联 mock 路线、路线解析、GPS 模拟、事件触发、地标排序和指令转写。
- 提供 Typer CLI 命令 `landmark-nav run-mock`。
- 将关键中间产物和最终结果输出到 `outputs/`。

### 需要新增/修改的模块路径

- `src/landmark_nav/pipeline/mock_pipeline.py`：实现一键 mock pipeline 编排。
- `src/landmark_nav/pipeline/artifacts.py`：统一管理输出文件路径和 JSON 写入。
- `src/landmark_nav/cli.py`：注册 `run-mock` 命令和参数。

### CLI 行为

- `landmark-nav run-mock --origin ... --destination ...` 使用 mock 数据完成全流程。
- 支持 `--output-dir outputs/` 指定输出目录。
- 支持 `--interval-meters`、`--trigger-distance`、`--top-k` 调整 pipeline 参数。
- 运行结束后打印生成的 route、trace、events、landmarks、instructions 文件路径。

### 测试文件

- `tests/test_mock_pipeline.py`：验证 pipeline 返回完整产物并写出预期文件。
- `tests/test_cli_run_mock.py`：使用 Typer runner 验证 `run-mock` 命令参数和输出。

### 验收命令

- `python -m pytest tests/test_mock_pipeline.py tests/test_cli_run_mock.py`
- `ruff check src/landmark_nav/pipeline src/landmark_nav/cli.py tests/test_mock_pipeline.py tests/test_cli_run_mock.py`
- `mypy src/landmark_nav/pipeline src/landmark_nav/cli.py`

## Phase 9：GeoJSON / HTML 可视化

### 目标

- 将路线、GPS 轨迹、导航事件和地标候选导出为 GeoJSON。
- 生成可本地打开的 HTML 可视化页面。
- 默认输出到 `outputs/`，便于演示和调试。

### 需要新增/修改的模块路径

- `src/landmark_nav/viz/geojson.py`：生成 route、trace、events、landmarks 的 GeoJSON FeatureCollection。
- `src/landmark_nav/viz/html.py`：生成包含地图图层和说明面板的 HTML。
- `src/landmark_nav/pipeline/mock_pipeline.py`：在 pipeline 中增加可视化产物输出。
- `outputs/`：保存 `route.geojson`、`trace.geojson`、`events.geojson`、`landmarks.geojson`、`index.html`。

### CLI 行为

- `landmark-nav run-mock --visualize` 额外生成 GeoJSON 和 HTML。
- `landmark-nav debug export-geojson --mock` 仅导出 GeoJSON 产物。
- 运行结束后打印 `outputs/index.html` 的本地路径。

### 测试文件

- `tests/test_viz_geojson.py`：验证 GeoJSON 结构、坐标顺序和属性字段。
- `tests/test_viz_html.py`：验证 HTML 包含必要图层引用、标题和产物路径。
- `tests/test_pipeline_visualize.py`：验证 `run-mock --visualize` 生成所有可视化文件。

### 验收命令

- `python -m pytest tests/test_viz_geojson.py tests/test_viz_html.py tests/test_pipeline_visualize.py`
- `ruff check src/landmark_nav/viz src/landmark_nav/pipeline tests/test_viz_geojson.py tests/test_viz_html.py tests/test_pipeline_visualize.py`
- `mypy src/landmark_nav/viz src/landmark_nav/pipeline`

## Phase 10：测试与评估

### 目标

- 完善单元测试、集成测试和端到端验收测试。
- 统一 pytest、ruff、mypy 的项目级验收命令。
- 增加评估脚本，衡量事件触发、地标排序和转写质量。

### 需要新增/修改的模块路径

- `tests/test_end_to_end.py`：覆盖 mock pipeline 端到端行为。
- `tests/fixtures/`：存放评估用路线、POI、期望事件与期望指令。
- `src/landmark_nav/eval/metrics.py`：定义事件召回、候选命中率、指令覆盖率等指标。
- `src/landmark_nav/eval/run_eval.py`：执行评估并输出报告。
- `pyproject.toml`：补充覆盖率、ruff、mypy 严格度配置。

### CLI 行为

- `landmark-nav eval --mock --fixtures tests/fixtures` 输出评估指标摘要。
- 支持 `--output outputs/eval_report.json` 保存评估报告。
- `landmark-nav run-mock --strict` 可在缺失关键产物或指标不达标时返回非零退出码。

### 测试文件

- `tests/test_eval_metrics.py`：验证指标计算逻辑。
- `tests/test_eval_cli.py`：验证评估 CLI 参数、输出和退出码。
- `tests/test_end_to_end.py`：验证全流程产物、事件、地标和指令满足基本质量门槛。

### 验收命令

- `python -m pytest`
- `ruff check .`
- `mypy src`
- `landmark-nav run-mock --visualize --output-dir outputs/`
- `landmark-nav eval --mock --fixtures tests/fixtures --output outputs/eval_report.json`
