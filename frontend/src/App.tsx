import './App.css'

const navItems = [
  { label: 'Dashboard', href: '#dashboard' },
  { label: 'User Management', href: '#users' },
  { label: 'Devices', href: '#devices' },
  { label: 'Harvest Trends', href: '#trends' },
  { label: 'Revenue Analytics', href: '#revenue' },
  { label: 'Defect Analytics', href: '#defects' },
  { label: 'Target Settings', href: '#targets' },
  { label: 'Profile', href: '#profile' },
]

const stats = [
  {
    label: 'Total Devices',
    value: '128',
    meta: '121 online, 7 offline',
    badge: '+6',
    tone: 'ok',
  },
  {
    label: "Today's Harvest",
    value: '32,480 kg',
    meta: 'Target: 30,000 kg',
    badge: '+8%',
    tone: 'ok',
  },
  {
    label: 'Active Alarms',
    value: '12',
    meta: '3 critical, 9 warning',
    badge: 'Watch',
    tone: 'danger',
  },
]

const quickAccess = [
  { label: 'Devices', detail: 'Register and monitor devices' },
  { label: 'Harvest Trends', detail: 'Daily, weekly, monthly views' },
  { label: 'Revenue Analytics', detail: 'Forecasts and pricing' },
  { label: 'Defect Analytics', detail: 'Counts and ratios' },
]

const users = [
  { id: 'U001', name: 'John Doe', email: 'john@example.com', role: 'Admin' },
  { id: 'U002', name: 'Jane Smith', email: 'jane@example.com', role: 'Manager' },
  { id: 'U003', name: 'Bob Wilson', email: 'bob@example.com', role: 'Operator' },
  { id: 'U004', name: 'Alice Brown', email: 'alice@example.com', role: 'Viewer' },
]

const devices = [
  { id: 'DEV001', battery: '85%', alarm: 'Normal', tone: 'ok' },
  { id: 'DEV002', battery: '62%', alarm: 'Warning', tone: 'warning' },
  { id: 'DEV003', battery: '94%', alarm: 'Normal', tone: 'ok' },
  { id: 'DEV004', battery: '28%', alarm: 'Critical', tone: 'danger' },
  { id: 'DEV005', battery: '71%', alarm: 'Normal', tone: 'ok' },
]

const pricing = [
  { category: 'Large', price: '$5.00' },
  { category: 'Medium', price: '$3.50' },
  { category: 'Small', price: '$2.00' },
]

function App() {
  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">WH</div>
          <div>
            <p className="brand-title">IoT Harvest Management</p>
            <p className="brand-subtitle">Operations Console</p>
          </div>
        </div>
        <div className="topbar-actions">
          <button className="btn ghost" type="button">
            Profile
          </button>
          <button className="btn ghost" type="button">
            Logout
          </button>
        </div>
      </header>

      <div className="page">
        <aside className="sidebar">
          <div className="sidebar-header">
            <p className="sidebar-title">Navigation</p>
            <span className="pill ok">Live</span>
          </div>
          <nav className="nav">
            {navItems.map((item, index) => (
              <a
                key={item.label}
                className={`nav-item${index === 0 ? ' active' : ''}`}
                href={item.href}
              >
                <span className="nav-title">{item.label}</span>
                <span className="nav-meta">Operations</span>
              </a>
            ))}
          </nav>
          <div className="sidebar-card">
            <p className="card-title">System Status</p>
            <div className="status-row">
              <span>Gateway</span>
              <span className="pill ok">Online</span>
            </div>
            <div className="status-row">
              <span>Storage</span>
              <span className="pill warning">78%</span>
            </div>
            <div className="progress">
              <span className="progress-bar" style={{ width: '78%' }} />
            </div>
            <p className="muted">78% capacity used</p>
          </div>
        </aside>

        <main className="content">
          <section className="section" id="dashboard">
            <div className="section-header">
              <div>
                <p className="section-kicker">Overview</p>
                <h1 className="section-title">Dashboard</h1>
                <p className="note">Last sync: 5 minutes ago</p>
              </div>
              <div className="section-actions">
                <button className="btn outline" type="button">
                  Export
                </button>
                <button className="btn primary" type="button">
                  Create Report
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
                  <h3>Harvest Summary</h3>
                  <span className="pill neutral">Daily</span>
                </div>
                <div className="chart-placeholder large">Harvest Summary Chart</div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>Revenue Summary</h3>
                  <span className="pill neutral">Monthly</span>
                </div>
                <div className="chart-placeholder large">Revenue Summary Chart</div>
              </div>
            </div>

            <div className="quick-access">
              <p className="block-title">Quick Access</p>
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
                <p className="section-kicker">Administration</p>
                <h2 className="section-title">User Management</h2>
                <p className="note">Admin only - role change and delete actions</p>
              </div>
              <button className="btn primary" type="button">
                Add User
              </button>
            </div>
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">User ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Role</th>
                    <th scope="col">Actions</th>
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
                            Edit Role
                          </button>
                          <button className="btn danger" type="button">
                            Delete
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
                <p className="section-kicker">Fleet</p>
                <h2 className="section-title">Devices</h2>
                <p className="note">Admin only - register device and delete actions</p>
              </div>
              <button className="btn primary" type="button">
                Register Device
              </button>
            </div>
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">Device ID</th>
                    <th scope="col">Battery Status</th>
                    <th scope="col">Alarm Status</th>
                    <th scope="col">Actions</th>
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
                            View Alarm Details
                          </button>
                          <button className="btn danger" type="button">
                            Delete
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
                <p className="section-kicker">Analytics</p>
                <h2 className="section-title">Harvest Trends</h2>
                <p className="note">Category values editable by Admin</p>
              </div>
            </div>
            <div className="block">
              <p className="block-title">Period</p>
              <div className="tab-list">
                <button className="tab active" type="button">
                  Daily
                </button>
                <button className="tab" type="button">
                  Weekly
                </button>
                <button className="tab" type="button">
                  Monthly
                </button>
              </div>
            </div>
            <div className="chart-card">
              <div className="card-header">
                <h3>Harvest Amount</h3>
              </div>
              <div className="chart-placeholder xl">Harvest Amount Chart</div>
            </div>
            <div className="block">
              <p className="block-title">Category / Size</p>
              <div className="filter-list">
                <button className="filter active" type="button">
                  All
                </button>
                <button className="filter" type="button">
                  Large
                </button>
                <button className="filter" type="button">
                  Medium
                </button>
                <button className="filter" type="button">
                  Small
                </button>
              </div>
            </div>
            <div className="chart-grid">
              <div className="chart-card">
                <div className="card-header">
                  <h3>Defect Count</h3>
                  <span className="pill neutral">Weekly</span>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>Defect Ratio</h3>
                  <span className="pill neutral">Weekly</span>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
            </div>
          </section>

          <section className="section" id="revenue">
            <div className="section-header">
              <div>
                <p className="section-kicker">Financials</p>
                <h2 className="section-title">Revenue Analytics</h2>
                <p className="note">Forecasts and price management</p>
              </div>
            </div>
            <div className="chart-grid triple">
              <div className="chart-card">
                <div className="card-header">
                  <h3>Monthly Harvest Forecast</h3>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>Monthly Revenue</h3>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>Yearly Revenue</h3>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
            </div>
            <div className="section-header compact">
              <div>
                <h3 className="section-subtitle">Price Management</h3>
                <p className="note">Admin only - add, edit, and delete actions</p>
              </div>
              <button className="btn outline" type="button">
                Add Category
              </button>
            </div>
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">Category</th>
                    <th scope="col">Unit Price</th>
                    <th scope="col">Actions</th>
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
                            Edit
                          </button>
                          <button className="btn danger" type="button">
                            Delete
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
                <p className="section-kicker">Quality</p>
                <h2 className="section-title">Defect Analysis</h2>
                <p className="note">Monitor count and ratio changes</p>
              </div>
            </div>
            <div className="block">
              <p className="block-title">Period</p>
              <div className="tab-list">
                <button className="tab active" type="button">
                  Weekly
                </button>
                <button className="tab" type="button">
                  Monthly
                </button>
              </div>
            </div>
            <div className="chart-grid">
              <div className="chart-card">
                <div className="card-header">
                  <h3>Defect Count</h3>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
              <div className="chart-card">
                <div className="card-header">
                  <h3>Defect Ratio (%)</h3>
                </div>
                <div className="chart-placeholder">Chart</div>
              </div>
            </div>
          </section>

          <section className="section" id="targets">
            <div className="section-header">
              <div>
                <p className="section-kicker">Targets</p>
                <h2 className="section-title">Harvest Targets</h2>
                <p className="note">Admin only</p>
              </div>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label htmlFor="daily-target">Daily Target (kg)</label>
                <input id="daily-target" placeholder="Input Field" type="text" />
              </div>
              <div className="form-field">
                <label htmlFor="weekly-target">Weekly Target (kg)</label>
                <input id="weekly-target" placeholder="Input Field" type="text" />
              </div>
              <div className="form-field">
                <label htmlFor="monthly-target">Monthly Target (kg)</label>
                <input id="monthly-target" placeholder="Input Field" type="text" />
              </div>
              <button className="btn primary" type="button">
                Save Targets
              </button>
            </div>
          </section>

          <section className="section" id="profile">
            <div className="section-header">
              <div>
                <p className="section-kicker">Account</p>
                <h2 className="section-title">Profile</h2>
                <p className="note">Update your personal details</p>
              </div>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label htmlFor="profile-name">Name</label>
                <input id="profile-name" placeholder="Input Field" type="text" />
              </div>
              <div className="form-field">
                <label htmlFor="profile-email">Email</label>
                <input id="profile-email" placeholder="Input Field" type="email" />
              </div>
              <div className="form-field">
                <label htmlFor="profile-password">Password</label>
                <input id="profile-password" placeholder="Input Field" type="password" />
              </div>
              <button className="btn primary" type="button">
                Save Changes
              </button>
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
