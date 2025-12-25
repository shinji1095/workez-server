import './App.css'

const navItems = [
  { label: 'ダッシュボード', href: '#dashboard' },
  { label: 'ユーザー管理', href: '#users' },
  { label: 'デバイス', href: '#devices' },
  { label: '収穫トレンド', href: '#trends' },
  { label: '売上分析', href: '#revenue' },
  { label: '不良分析', href: '#defects' },
  { label: '目標設定', href: '#targets' },
  { label: 'プロフィール', href: '#profile' },
]

const stats = [
  {
    label: 'デバイス総数',
    value: '128',
    meta: 'オンライン121 / オフライン7',
    badge: '+6',
    tone: 'ok',
  },
  {
    label: '本日の収穫量',
    value: '32,480 kg',
    meta: '目標: 30,000 kg',
    badge: '+8%',
    tone: 'ok',
  },
  {
    label: 'アクティブアラーム',
    value: '12',
    meta: '重大3 / 警告9',
    badge: '注意',
    tone: 'danger',
  },
]

const quickAccess = [
  { label: 'デバイス', detail: 'デバイスの登録と監視' },
  { label: '収穫トレンド', detail: '日次・週次・月次の推移' },
  { label: '売上分析', detail: '予測と価格' },
  { label: '不良分析', detail: '件数と比率' },
]

const users = [
  { id: 'U001', name: '山田 太郎', email: 'taro@example.com', role: '管理者' },
  { id: 'U002', name: '佐藤 花子', email: 'hanako@example.com', role: 'マネージャー' },
  { id: 'U003', name: '鈴木 一郎', email: 'ichiro@example.com', role: 'オペレーター' },
  { id: 'U004', name: '高橋 美咲', email: 'misaki@example.com', role: '閲覧者' },
]

const devices = [
  { id: 'DEV001', battery: '85%', alarm: '正常', tone: 'ok' },
  { id: 'DEV002', battery: '62%', alarm: '警告', tone: 'warning' },
  { id: 'DEV003', battery: '94%', alarm: '正常', tone: 'ok' },
  { id: 'DEV004', battery: '28%', alarm: '重大', tone: 'danger' },
  { id: 'DEV005', battery: '71%', alarm: '正常', tone: 'ok' },
]

const pricing = [
  { category: '大', price: '$5.00' },
  { category: '中', price: '$3.50' },
  { category: '小', price: '$2.00' },
]

const buildConicGradient = (slices: { value: number; color: string }[]) => {
  let total = 0
  const segments = slices.map((slice) => {
    const start = total
    total += slice.value
    return `${slice.color} ${start}% ${total}%`
  })
  return `conic-gradient(${segments.join(', ')})`
}

const harvestAmount = [
  { label: '月', value: 58, display: '28k' },
  { label: '火', value: 76, display: '33k' },
  { label: '水', value: 62, display: '29k' },
  { label: '木', value: 88, display: '36k' },
  { label: '金', value: 70, display: '31k' },
  { label: '土', value: 94, display: '39k' },
  { label: '日', value: 66, display: '30k' },
]

const revenueSummary = [
  { label: '1月', value: 62, display: '$112k' },
  { label: '2月', value: 54, display: '$98k' },
  { label: '3月', value: 70, display: '$124k' },
  { label: '4月', value: 60, display: '$110k' },
  { label: '5月', value: 82, display: '$138k' },
  { label: '6月', value: 68, display: '$121k' },
]

const defectCounts = [
  { label: '大', value: 100, count: 48 },
  { label: '中', value: 76, count: 36 },
  { label: '小', value: 54, count: 25 },
  { label: 'その他', value: 32, count: 14 },
]

const defectRatio = [
  { label: '大', value: 42, color: '#4f8a5b' },
  { label: '中', value: 28, color: '#8bb174' },
  { label: '小', value: 18, color: '#f3c66f' },
  { label: 'その他', value: 12, color: '#f1a45b' },
]

const defectRatioGradient = buildConicGradient(defectRatio)

const monthlyRevenue = [
  { label: '1週', value: 56, display: '$24k' },
  { label: '2週', value: 78, display: '$33k' },
  { label: '3週', value: 68, display: '$29k' },
  { label: '4週', value: 86, display: '$37k' },
  { label: '5週', value: 62, display: '$27k' },
]

const defectWeekly = [
  { label: '1週', value: 58, display: '18' },
  { label: '2週', value: 74, display: '24' },
  { label: '3週', value: 64, display: '21' },
  { label: '4週', value: 82, display: '27' },
  { label: '5週', value: 48, display: '16' },
]

function App() {
  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">WH</div>
          <div>
            <p className="brand-title">IoT 収穫管理</p>
            <p className="brand-subtitle">運用コンソール</p>
          </div>
        </div>
        <div className="topbar-actions">
          <button className="btn ghost" type="button">
            プロフィール
          </button>
          <button className="btn ghost" type="button">
            ログアウト
          </button>
        </div>
      </header>

      <div className="page">
        <aside className="sidebar">
          <div className="sidebar-header">
            <p className="sidebar-title">ナビゲーション</p>
            <span className="pill ok">稼働中</span>
          </div>
          <nav className="nav">
            {navItems.map((item, index) => (
              <a
                key={item.label}
                className={`nav-item${index === 0 ? ' active' : ''}`}
                href={item.href}
              >
                <span className="nav-title">{item.label}</span>
                <span className="nav-meta">運用</span>
              </a>
            ))}
          </nav>
          <div className="sidebar-card">
            <p className="card-title">システム状況</p>
            <div className="status-row">
              <span>ゲートウェイ</span>
              <span className="pill ok">オンライン</span>
            </div>
            <div className="status-row">
              <span>ストレージ</span>
              <span className="pill warning">78%</span>
            </div>
            <div className="progress">
              <span className="progress-bar" style={{ width: '78%' }} />
            </div>
            <p className="muted">使用容量 78%</p>
          </div>
        </aside>

        <main className="content">
          <section className="section" id="dashboard">
            <div className="section-header">
              <div>
                <p className="section-kicker">概要</p>
                <h1 className="section-title">ダッシュボード</h1>
                <p className="note">最終同期: 5分前</p>
              </div>
              <div className="section-actions">
                <button className="btn outline" type="button">
                  エクスポート
                </button>
                <button className="btn primary" type="button">
                  レポート作成
                </button>
              </div>
            </div>

            <div className="stat-grid">
              {stats.map((stat) => (
                <div className="stat-card" key={stat.label}>
                  <p className="stat-label">{stat.label}</p>
                  <div className="stat-row">
                    <span className="stat-value">{stat.value}</span>
                    <span className={`pill ${stat.tone}`}>{stat.badge}</span>
                  </div>
                  <p className="stat-meta">{stat.meta}</p>
                </div>
              ))}
            </div>

            <div className="chart-grid">
              <div className="chart-card">
                <div className="card-header">
                  <h3>収穫サマリー</h3>
                  <span className="pill neutral">日次</span>
                </div>
                <div className="chart-surface large">
                  <svg
                    className="chart-svg"
                    viewBox="0 0 260 120"
                    role="img"
                    aria-label="収穫サマリーの折れ線グラフ"
                  >
                    <path
                      className="chart-area"
                      d="M0 86 L30 70 L60 76 L90 54 L120 62 L150 46 L180 52 L210 32 L240 38 L260 28 L260 120 L0 120 Z"
                    />
                    <polyline
                      className="chart-line"
                      points="0,86 30,70 60,76 90,54 120,62 150,46 180,52 210,32 240,38 260,28"
                    />
                    <polyline
                      className="chart-line muted"
                      points="0,98 30,88 60,92 90,78 120,84 150,70 180,74 210,60 240,64 260,56"
                    />
                  </svg>
                  <div className="chart-foot">
                    <div className="chart-metrics">
                      <div className="metric">
                        <p className="metric-label">日平均</p>
                        <p className="metric-value">31.2k kg</p>
                      </div>
                      <div className="metric">
                        <p className="metric-label">最高日</p>
                        <p className="metric-value">39.1k kg</p>
                      </div>
                    </div>
                    <span className="pill ok">+9%</span>
                  </div>
                </div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>売上サマリー</h3>
                  <span className="pill neutral">月次</span>
                </div>
                <div className="chart-surface large">
                  <div className="bar-chart compact">
                    {revenueSummary.map((item) => (
                      <div className="bar-item" key={item.label}>
                        <span className="bar-value">{item.display}</span>
                        <div className="bar-track">
                          <span className="bar-fill" style={{ height: `${item.value}%` }} />
                        </div>
                        <span className="bar-label">{item.label}</span>
                      </div>
                    ))}
                  </div>
                  <div className="chart-foot">
                    <span className="muted">平均売上: $117k</span>
                    <span className="pill ok">前月比 +12%</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="quick-access">
              <p className="block-title">クイックアクセス</p>
              <div className="quick-grid">
                {quickAccess.map((item) => (
                  <button className="quick-button" key={item.label} type="button">
                    <span>{item.label}</span>
                    <span className="muted">{item.detail}</span>
                  </button>
                ))}
              </div>
            </div>
          </section>

          <section className="section" id="users">
            <div className="section-header">
              <div>
                <p className="section-kicker">管理</p>
                <h2 className="section-title">ユーザー管理</h2>
                <p className="note">管理者のみ - 役割変更と削除が可能</p>
              </div>
              <button className="btn primary" type="button">
                ユーザー追加
              </button>
            </div>
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">ユーザーID</th>
                    <th scope="col">名前</th>
                    <th scope="col">メール</th>
                    <th scope="col">権限</th>
                    <th scope="col">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id}>
                      <td>{user.id}</td>
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>{user.role}</td>
                      <td>
                        <div className="table-actions">
                          <button className="btn ghost" type="button">
                            権限変更
                          </button>
                          <button className="btn danger" type="button">
                            削除
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="section" id="devices">
            <div className="section-header">
              <div>
                <p className="section-kicker">フリート</p>
                <h2 className="section-title">デバイス</h2>
                <p className="note">管理者のみ - 登録と削除が可能</p>
              </div>
              <button className="btn primary" type="button">
                デバイス登録
              </button>
            </div>
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">デバイスID</th>
                    <th scope="col">バッテリー</th>
                    <th scope="col">アラーム</th>
                    <th scope="col">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {devices.map((device) => (
                    <tr key={device.id}>
                      <td>{device.id}</td>
                      <td>{device.battery}</td>
                      <td>
                        <span className={`pill ${device.tone}`}>{device.alarm}</span>
                      </td>
                      <td>
                        <div className="table-actions">
                          <button className="btn ghost" type="button">
                            アラーム詳細
                          </button>
                          <button className="btn danger" type="button">
                            削除
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="section" id="trends">
            <div className="section-header">
              <div>
                <p className="section-kicker">分析</p>
                <h2 className="section-title">収穫トレンド</h2>
                <p className="note">カテゴリ値は管理者が編集可能</p>
              </div>
            </div>
            <div className="block">
              <p className="block-title">期間</p>
              <div className="tab-list">
                <button className="tab active" type="button">
                  日次
                </button>
                <button className="tab" type="button">
                  週次
                </button>
                <button className="tab" type="button">
                  月次
                </button>
              </div>
            </div>
            <div className="chart-card">
              <div className="card-header">
                <h3>収穫量</h3>
              </div>
              <div className="chart-surface xl">
                <div className="bar-chart tall">
                  {harvestAmount.map((item) => (
                    <div className="bar-item" key={item.label}>
                      <span className="bar-value">{item.display}</span>
                      <div className="bar-track">
                        <span className="bar-fill" style={{ height: `${item.value}%` }} />
                      </div>
                      <span className="bar-label">{item.label}</span>
                    </div>
                  ))}
                </div>
                <div className="chart-foot">
                  <div className="chart-metrics">
                    <div className="metric">
                      <p className="metric-label">目標</p>
                      <p className="metric-value">210k kg</p>
                    </div>
                    <div className="metric">
                      <p className="metric-label">実績</p>
                      <p className="metric-value">224k kg</p>
                    </div>
                  </div>
                  <span className="pill ok">+6%</span>
                </div>
              </div>
            </div>
            <div className="block">
              <p className="block-title">カテゴリ / サイズ</p>
              <div className="filter-list">
                <button className="filter active" type="button">
                  全て
                </button>
                <button className="filter" type="button">
                  大
                </button>
                <button className="filter" type="button">
                  中
                </button>
                <button className="filter" type="button">
                  小
                </button>
              </div>
            </div>
            <div className="chart-grid">
              <div className="chart-card">
                <div className="card-header">
                  <h3>不良数</h3>
                  <span className="pill neutral">週次</span>
                </div>
                <div className="chart-surface">
                  <div className="bar-list">
                    {defectCounts.map((item) => (
                      <div className="bar-row" key={item.label}>
                        <span className="bar-label">{item.label}</span>
                        <div className="bar-line">
                          <span className="bar-progress" style={{ width: `${item.value}%` }} />
                        </div>
                        <span className="bar-value">{item.count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>不良率</h3>
                  <span className="pill neutral">週次</span>
                </div>
                <div className="chart-surface">
                  <div className="pie-layout">
                    <div className="pie-chart" style={{ background: defectRatioGradient }}>
                      <div className="pie-hole" />
                      <span className="pie-center">比率</span>
                    </div>
                    <ul className="chart-legend">
                      {defectRatio.map((item) => (
                        <li className="legend-item" key={item.label}>
                          <span className="legend-swatch" style={{ background: item.color }} />
                          <span>{item.label}</span>
                          <span className="legend-value">{item.value}%</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="section" id="revenue">
            <div className="section-header">
              <div>
                <p className="section-kicker">収益</p>
                <h2 className="section-title">売上分析</h2>
                <p className="note">予測と価格管理</p>
              </div>
            </div>
            <div className="chart-grid triple">
              <div className="chart-card">
                <div className="card-header">
                  <h3>月次収穫予測</h3>
                </div>
                <div className="chart-surface">
                  <svg
                    className="chart-svg"
                    viewBox="0 0 260 120"
                    role="img"
                    aria-label="月次収穫予測"
                  >
                    <path
                      className="chart-area"
                      d="M0 90 L40 78 L80 66 L120 58 L160 46 L200 38 L240 30 L260 26 L260 120 L0 120 Z"
                    />
                    <polyline
                      className="chart-line"
                      points="0,90 40,78 80,66 120,58 160,46"
                    />
                    <polyline
                      className="chart-line dashed"
                      points="160,46 200,38 240,30 260,26"
                    />
                  </svg>
                  <div className="chart-foot">
                    <div className="chart-metrics">
                      <div className="metric">
                        <p className="metric-label">予測</p>
                        <p className="metric-value">+14%</p>
                      </div>
                      <div className="metric">
                        <p className="metric-label">ピーク予測</p>
                        <p className="metric-value">8月22日</p>
                      </div>
                    </div>
                    <span className="pill ok">順調</span>
                  </div>
                </div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>月次売上</h3>
                </div>
                <div className="chart-surface">
                  <div className="bar-chart compact">
                    {monthlyRevenue.map((item) => (
                      <div className="bar-item" key={item.label}>
                        <span className="bar-value">{item.display}</span>
                        <div className="bar-track">
                          <span className="bar-fill" style={{ height: `${item.value}%` }} />
                        </div>
                        <span className="bar-label">{item.label}</span>
                      </div>
                    ))}
                  </div>
                  <div className="chart-foot">
                    <span className="muted">平均 $30k</span>
                    <span className="pill ok">+8%</span>
                  </div>
                </div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>年次売上</h3>
                </div>
                <div className="chart-surface">
                  <svg
                    className="chart-svg"
                    viewBox="0 0 260 120"
                    role="img"
                    aria-label="年次売上の比較"
                  >
                    <polyline
                      className="chart-line muted"
                      points="0,88 40,80 80,72 120,68 160,62 200,56 240,50 260,46"
                    />
                    <polyline
                      className="chart-line"
                      points="0,96 40,86 80,76 120,66 160,52 200,40 240,32 260,28"
                    />
                  </svg>
                  <ul className="chart-legend inline">
                    <li className="legend-item">
                      <span className="legend-swatch muted" />
                      <span>前年</span>
                    </li>
                    <li className="legend-item">
                      <span className="legend-swatch" />
                      <span>今年</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div className="section-header compact">
              <div>
                <h3 className="section-subtitle">価格管理</h3>
                <p className="note">管理者のみ - 追加・編集・削除が可能</p>
              </div>
              <button className="btn outline" type="button">
                カテゴリ追加
              </button>
            </div>
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">カテゴリ</th>
                    <th scope="col">単価</th>
                    <th scope="col">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {pricing.map((item) => (
                    <tr key={item.category}>
                      <td>{item.category}</td>
                      <td>{item.price}</td>
                      <td>
                        <div className="table-actions">
                          <button className="btn ghost" type="button">
                            編集
                          </button>
                          <button className="btn danger" type="button">
                            削除
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="section" id="defects">
            <div className="section-header">
              <div>
                <p className="section-kicker">品質</p>
                <h2 className="section-title">不良分析</h2>
                <p className="note">件数と比率の変化を監視</p>
              </div>
            </div>
            <div className="block">
              <p className="block-title">期間</p>
              <div className="tab-list">
                <button className="tab active" type="button">
                  週次
                </button>
                <button className="tab" type="button">
                  月次
                </button>
              </div>
            </div>
            <div className="chart-grid">
              <div className="chart-card">
                <div className="card-header">
                  <h3>不良数</h3>
                </div>
                <div className="chart-surface">
                  <div className="bar-chart compact">
                    {defectWeekly.map((item) => (
                      <div className="bar-item" key={item.label}>
                        <span className="bar-value">{item.display}</span>
                        <div className="bar-track">
                          <span className="bar-fill alt" style={{ height: `${item.value}%` }} />
                        </div>
                        <span className="bar-label">{item.label}</span>
                      </div>
                    ))}
                  </div>
                  <div className="chart-foot">
                    <span className="muted">平均 21/週</span>
                    <span className="pill warning">+3%</span>
                  </div>
                </div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>不良率（%）</h3>
                </div>
                <div className="chart-surface">
                  <svg
                    className="chart-svg"
                    viewBox="0 0 260 120"
                    role="img"
                    aria-label="不良率の推移"
                  >
                    <polyline
                      className="chart-line secondary"
                      points="0,84 40,72 80,78 120,64 160,70 200,58 240,62 260,54"
                    />
                    <polyline
                      className="chart-line secondary dashed"
                      points="160,70 200,58 240,62 260,54"
                    />
                  </svg>
                  <div className="chart-foot">
                    <span className="muted">平均比率: 3.2%</span>
                    <span className="pill ok">安定</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="section" id="targets">
            <div className="section-header">
              <div>
                <p className="section-kicker">目標</p>
                <h2 className="section-title">収穫目標</h2>
                <p className="note">管理者のみ</p>
              </div>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label htmlFor="daily-target">日次目標（kg）</label>
                <input id="daily-target" placeholder="入力" type="text" />
              </div>
              <div className="form-field">
                <label htmlFor="weekly-target">週次目標（kg）</label>
                <input id="weekly-target" placeholder="入力" type="text" />
              </div>
              <div className="form-field">
                <label htmlFor="monthly-target">月次目標（kg）</label>
                <input id="monthly-target" placeholder="入力" type="text" />
              </div>
              <button className="btn primary" type="button">
                目標を保存
              </button>
            </div>
          </section>

          <section className="section" id="profile">
            <div className="section-header">
              <div>
                <p className="section-kicker">アカウント</p>
                <h2 className="section-title">プロフィール</h2>
                <p className="note">個人情報を更新</p>
              </div>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label htmlFor="profile-name">名前</label>
                <input id="profile-name" placeholder="入力" type="text" />
              </div>
              <div className="form-field">
                <label htmlFor="profile-email">メール</label>
                <input id="profile-email" placeholder="入力" type="email" />
              </div>
              <div className="form-field">
                <label htmlFor="profile-password">パスワード</label>
                <input id="profile-password" placeholder="入力" type="password" />
              </div>
              <button className="btn primary" type="button">
                変更を保存
              </button>
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
