<template>
  <div class="indexcontainer">
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">PowerModel</a>
    </nav>
    <div class="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light">
      <h1>PowerModel</h1>
      <p class="lead font-weight-normal">
        Upload your power usage to see detailed usage information
      </p>
      <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" @vdropzone-success="uploadsuccess"></vue-dropzone>
      </div>
    <div class="container bg-light">
      <div class="row">
        <div class="col">
          <div v-if="fileinvalid" class="alert alert-danger" role="alert">File invalid - only Powercor files are supported</div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <h3 class="h2">FAQ</h3>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <h4>What kinds of files are supported</h4>
          <p>Only Victorian Energy Compare files provided by Powercor / Citipower are supported</p>
          <h4>How do I get my usage data?</h4>
          <p>Visit the consumer portal <a href="https://customermeterdata.portal.powercor.com.au/customermeterdata/CADAccountPage">here</a> and register or sign in to access your usage data</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
export default {
  name: 'Index',
  components: {
    vueDropzone: vue2Dropzone
  },
  data () {
    return {
      dropzoneOptions: {
        url: '/api/upload',
        uploadMultiple: false,
        thumbnailWidth: 150,
        maxFilesize: 2,
        acceptedFiles: '.csv',
        clickable: true,
        maxFiles: 1,
        autoProcessQueue: true
      },
      fileinvalid: false
    }
  },
  methods: {
    uploadsuccess: function (file, response) {
      console.dir(response)
      if (response['status'] === 1000) {
        this.$router.push('/Results')
      } else if (response['status'] === 9999) {
        this.fileinvalid = true
        this.$refs.myVueDropzone.removeAllFiles()
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
