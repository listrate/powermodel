<template>
<div class="resultcontainer">
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">PowerModel</a>
    </nav>
    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link active" href="#">
                  Dashboard <span class="sr-only">(current)</span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" v-scroll-to="'#heatmap_a'">
                  Heatmap
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" v-scroll-to="'#weekdayweekend_a'">
                  Weekday/weekend usage comparison
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" v-scroll-to="'#daybreakdown_a'">
                  Energy usage by Day
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" v-scroll-to="'#timeofdaybreakdown_a'">
                  Energy usage by time of day
                </a>
              </li>
            </ul>
          </div>
        </nav>

        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h2 class="h2">Dashboard</h2>
            <div class="btn-toolbar mb-2 mb-md-0">
            </div>
          </div>
          <div class="container mt-2">
            <div class="row">
              <div class="col">
                <h2 class="h2">Your usage at a glance</h2>
                <p>This report was generated for the period begining {{getShortDateString(this.summarydata['startdate'])}} to {{getShortDateString(this.summarydata['enddate'])}}</p>
              </div>
            </div>
            <div class="row">
              <div class="card-deck">
                <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                  <div class="card-body">
                    <h5 class="card-title">{{this.summarydata['collectiondays']}}</h5>
                  </div>
                  <div class="card-header">Collection days</div>
                </div>
                <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                  <div class="card-body">
                    <h5 class="card-title">{{this.summarydata['usageaverage']}} kWh</h5>
                  </div>
                  <div class="card-header">Average daily usage</div>
                </div>
                <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                  <div class="card-body">
                    <h5 class="card-title">{{this.summarydata['usagesum']}} kWh</h5>
                  </div>
                  <div class="card-header">Total usage</div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="card-deck">
                <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                  <div class="card-body">
                    <h5 class="card-title">{{this.summarydata['highestusage']['usage']}} kWh</h5>
                  </div>
                  <div class="card-header">Highest usage - {{getShortDateString(this.summarydata['highestusage']['date'])}}</div>
                </div>
                <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                  <div class="card-body">
                    <h5 class="card-title">{{this.summarydata['lowestusage']['usage']}} kWh</h5>
                  </div>
                  <div class="card-header">Lowest usage - {{getShortDateString(this.summarydata['lowestusage']['date'])}}</div>
                </div>
              </div>
            </div>
          </div>
          <div class="card">
            <div class="card-body">
              <h2 class="h2" id="heatmap_a">Heatmap</h2>
              <div class="card-img-top" id="heatmap"></div>
              <h6 class="card-subtitle mb-2 text-muted mt-2">Each tile reprsents the total usage for that day</h6>
            </div>
          </div>
          <div class="card mt-4">
            <div class="card-body">
              <h2 class="h2" id="weekdayweekend_a">Weekday/weekend usage comparison</h2>
              <div class="card-img-top" id="weekdayweekend"></div>
              <h6 class="card-subtitle mb-2 text-muted mt-2">Average energy usage on weekdays compared to weekeds</h6>
            </div>
          </div>
          <div class="card mt-4">
            <div class="card-body">
              <h2 class="h2" id="daybreakdown_a">Day breakdown</h2>
              <div class="card-img-top" id="daybreakdown"></div>
              <h6 class="card-subtitle mb-2 text-muted mt-2">Average usage by day of week</h6>
            </div>
          </div>
          <div class="card mt-4">
            <div class="card-body">
              <h2 class="h2" id="timeofdaybreakdown_a">Time of day breakdown</h2>
              <div class="card-img-top" id="timeofdaybreakdown"></div>
              <h6 class="card-subtitle mb-2 text-muted mt-2">Average usage by time of day over full months</h6>
              <p class="card-text">Legend - Morning (00:00 to 12:00) Afternoon (12:30 to 18:00) Night (18:30 to 23:30)</p>
            </div>
          </div>
        </main>
      </div>
    </div>
</div>
</template>

<script>
import Plotly from 'plotly.js'
export default {
  data () {
    return {
      invalid_data: false,
      layout: {
        autosize: true,
        width: 4,
        height: 3,
        dimension: 'ratio',
        margin: {
          l: 110,
          r: 110,
          b: 60,
          t: 60,
          pad: 4
        }
      },
      heatmapdata: {
        x: [],
        y: [],
        z: [],
        type: 'heatmap'
      },
      weekdayweekenddata: {
        x: [],
        y: [],
        type: 'bar'
      },
      daybreakdowndata: {
        x: [],
        y: [],
        type: 'bar'
      },
      timeofdaybreakdowndata: [],
      summarydata: {
        collectiondays: 0,
        startdate: null,
        enddate: null,
        highestusage: {
          date: null,
          dayofweek: 0,
          usage: 0,
          weekno: 0
        },
        lowestusage: {
          date: null,
          dayofweek: 0,
          usage: 0,
          weekno: 0
        },
        usageaverage: 0,
        usagesum: 0,
        session_id: null
      }
    }
  },
  mounted: function () {
  },
  created: function () {
    this.getData()
  },
  methods: {
    getData: function () {
      this.$root.axios.get('/api/summary').then((response) => {
        if (this.isvaliddata(response['data'])) {
          this.summarydata = response['data']
          this.summarydata['startdate'] = new Date(this.summarydata['startdate'])
          this.summarydata['enddate'] = new Date(this.summarydata['enddate'])
          this.summarydata['highestusage']['date'] = new Date(this.summarydata['highestusage']['date'])
          this.summarydata['lowestusage']['date'] = new Date(this.summarydata['lowestusage']['date'])
        } else {
          this.redirecttoindex()
        }
      })

      this.$root.axios.get('/api/heatmap').then((response) => {
        if (this.isvaliddata(response['data'])) {
          this.heatmapdata = response['data']
          this.renderheatmap()
        } else {
          this.redirecttoindex()
        }
      })

      this.$root.axios.get('/api/weekdayweekend').then((response) => {
        if (this.isvaliddata(response['data'])) {
          this.weekdayweekenddata = response['data']
          this.renderweekdayweekendchart()
        } else {
          this.redirecttoindex()
        }
      })

      this.$root.axios.get('/api/daybreakdown').then((response) => {
        if (this.isvaliddata(response['data'])) {
          this.daybreakdowndata = response['data']
          this.renderdaybreakdownchart()
        } else {
          this.redirecttoindex()
        }
      })

      this.$root.axios.get('/api/timeofdaybreakdown').then((response) => {
        if (this.isvaliddata(response['data'])) {
          this.timeofdaybreakdowndata = response['data']
          this.rendertimeofdaychart()
        } else {
          this.redirecttoindex()
        }
      })
      window.addEventListener('resize', this.renderallcharts)
    },
    isvaliddata: function (data) {
      if ('status' in data && data['status'] === 9999) {
        return false
      } else {
        return true
      }
    },
    redirecttoindex: function () {
      this.$router.push('/')
    },
    renderheatmap: function () {
      var layout = Object.assign({}, this.layout)
      var data = [this.heatmapdata]
      Plotly.newPlot('heatmap', data, layout)
    },
    renderweekdayweekendchart: function () {
      var layout = Object.assign({}, this.layout)
      var data = [this.weekdayweekenddata]
      Plotly.newPlot('weekdayweekend', data, layout)
    },
    renderdaybreakdownchart: function () {
      var layout = Object.assign({}, this.layout)
      var data = [this.daybreakdowndata]
      Plotly.newPlot('daybreakdown', data, layout)
    },
    rendertimeofdaychart: function () {
      var layout = Object.assign({}, this.layout)
      var data = this.timeofdaybreakdowndata
      Plotly.newPlot('timeofdaybreakdown', data, layout)
    },
    renderallcharts: function () {
      this.renderheatmap()
      this.renderweekdayweekendchart()
      this.renderdaybreakdownchart()
      this.rendertimeofdaychart()
    },
    getShortDateString: function (dateobj) {
      if (dateobj != null) {
        return dateobj.toDateString()
      } else {
        return ''
      }
    }
  }
}
</script>

<style>
/* from https://getbootstrap.com/docs/4.1/examples/dashboard/ */
body {
  font-size: .875rem;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}

/*
 * Sidebar
 */

.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100; /* Behind the navbar */
  padding: 48px 0 0; /* Height of navbar */
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.sidebar-sticky {
  position: relative;
  top: 0;
  height: calc(100vh - 48px);
  padding-top: .5rem;
  overflow-x: hidden;
  overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}

@supports ((position: -webkit-sticky) or (position: sticky)) {
  .sidebar-sticky {
    position: -webkit-sticky;
    position: sticky;
  }
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
}

.sidebar .nav-link .feather {
  margin-right: 4px;
  color: #999;
}

.sidebar .nav-link.active {
  color: #007bff;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.active .feather {
  color: inherit;
}

.sidebar-heading {
  font-size: .75rem;
  text-transform: uppercase;
}

/*
 * Content
 */

[role="main"] {
  padding-top: 48px; /* Space for fixed navbar */
}

/*
 * Navbar
 */

.navbar-brand {
  padding-top: .75rem;
  padding-bottom: .75rem;
  font-size: 1rem;
  background-color: rgba(0, 0, 0, .25);
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .25);
}

.navbar .form-control {
  padding: .75rem 1rem;
  border-width: 0;
  border-radius: 0;
}

.form-control-dark {
  color: #fff;
  background-color: rgba(255, 255, 255, .1);
  border-color: rgba(255, 255, 255, .1);
}

.form-control-dark:focus {
  border-color: transparent;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, .25);
}

/*
 * Utilities
 */

.border-top { border-top: 1px solid #e5e5e5; }
.border-bottom { border-bottom: 1px solid #e5e5e5; }
</style>
